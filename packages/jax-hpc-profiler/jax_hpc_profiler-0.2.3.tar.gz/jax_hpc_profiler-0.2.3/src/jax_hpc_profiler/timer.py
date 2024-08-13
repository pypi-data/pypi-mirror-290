import os
import time
from functools import partial
from typing import Any, Callable, List, Tuple

import jax
import jax.numpy as jnp
import numpy as np
from jax import make_jaxpr
from jax.experimental import mesh_utils
from jax.experimental.shard_map import shard_map
from jax.sharding import Mesh, NamedSharding
from jax.sharding import PartitionSpec as P
from tabulate import tabulate


class Timer:

    def __init__(self, save_jaxpr=False):
        self.jit_time = None
        self.times = []
        self.profiling_data = {}
        self.compiled_code = {}
        self.save_jaxpr = save_jaxpr

    def _read_cost_analysis(self, cost_analysis: Any) -> str | None:
        if cost_analysis is None:
            return None
        return cost_analysis[0]['flops']

    def _normalize_memory_units(self, memory_analysis) -> str:  
        
        sizes_str = ['B', 'KB', 'MB', 'GB', 'TB' , 'PB']
        factors = [1 , 1024 , 1024**2 , 1024**3 , 1024**4 , 1024**5]
        factor = int(np.log10(memory_analysis) // 3)
        
        return f"{memory_analysis / factors[factor]:.2f} {sizes_str[factor]}"

    
    def _read_memory_analysis(self, memory_analysis: Any) -> Tuple:
        if memory_analysis is None:
            return None, None, None, None
        return (memory_analysis.generated_code_size_in_bytes,
                memory_analysis.argument_size_in_bytes,
                memory_analysis.output_size_in_bytes,
                memory_analysis.temp_size_in_bytes)

    def chrono_jit(self, fun: Callable, *args, ndarray_arg=None) -> np.ndarray:
        start = time.perf_counter()
        out = fun(*args)
        if ndarray_arg is None:
            out.block_until_ready()
        else:
            out[ndarray_arg].block_until_ready()
        end = time.perf_counter()
        self.jit_time = (end - start) * 1e3

        if self.save_jaxpr:
            jaxpr = make_jaxpr(fun)(*args)
            self.compiled_code["JAXPR"] = jaxpr.pretty_print()

        lowered = jax.jit(fun).lower(*args)
        compiled = lowered.compile()
        memory_analysis = self._read_memory_analysis(
            compiled.memory_analysis())
        cost_analysis = self._read_cost_analysis(compiled.cost_analysis())

        self.compiled_code["LOWERED"] = lowered.as_text()
        self.compiled_code["COMPILED"] = compiled.as_text()
        self.profiling_data["FLOPS"] = cost_analysis
        self.profiling_data[
            "generated_code"] = memory_analysis[0]
        self.profiling_data[
            "argument_size"] = memory_analysis[1]
        self.profiling_data[
            "output_size"] = memory_analysis[2]
        self.profiling_data["temp_size"] = memory_analysis[3]
        return out

    def chrono_fun(self, fun: Callable, *args, ndarray_arg=None) -> np.ndarray:
        start = time.perf_counter()
        out = fun(*args)
        if ndarray_arg is None:
            out.block_until_ready()
        else:
            out[ndarray_arg].block_until_ready()
        end = time.perf_counter()
        self.times.append((end - start) * 1e3)
        return out

    def _get_mean_times(self) -> np.ndarray:
        if jax.device_count() == 1:
            return np.array(self.times)

        devices = mesh_utils.create_device_mesh((jax.device_count(), ))
        mesh = Mesh(devices, ('x', ))
        sharding = NamedSharding(mesh, P('x'))

        times_array = jnp.array(self.times)
        global_shape = (jax.device_count(), times_array.shape[0])
        global_times = jax.make_array_from_callback(
            shape=global_shape,
            sharding=sharding,
            data_callback=lambda _: jnp.expand_dims(times_array,axis=0))

        @partial(shard_map,
                 mesh=mesh,
                 in_specs=P('x'),
                 out_specs=P(),
                 check_rep=False)
        def get_mean_times(times):
            return jax.lax.pmean(times, axis_name='x')

        times_array = get_mean_times(global_times)
        times_array.block_until_ready()
        return np.array(times_array.addressable_data(0)[0])

    def report(self,
               csv_filename: str,
               function: str,
               x: int,
               y: int | None = None,
               z: int | None = None,
               precision: str = "float32",
               px: int = 1,
               py: int = 1,
               backend: str = "NCCL",
               nodes: int = 1,
               md_filename: str | None = None,
               extra_info: dict = {}):

        if md_filename is None:
            dirname, filename = os.path.dirname(
                csv_filename), os.path.splitext(
                    os.path.basename(csv_filename))[0]
            report_folder = filename if dirname == "" else f"{dirname}/{filename}"
            os.makedirs(report_folder, exist_ok=True)
            md_filename = f"{report_folder}/{x}_{px}_{py}_{backend}_{precision}_{function}.md"

        y = x if y is None else y
        z = x if z is None else z

        times_array = self._get_mean_times()
        min_time = np.min(times_array)
        max_time = np.max(times_array)
        mean_time = np.mean(times_array)
        std_time = np.std(times_array)
        last_time = times_array[-1]


        flops = self.profiling_data["FLOPS"]
        generated_code = self.profiling_data["generated_code"]
        argument_size = self.profiling_data["argument_size"]
        output_size = self.profiling_data["output_size"]
        temp_size = self.profiling_data["temp_size"]

        csv_line = (
            f"{function},{precision},{x},{y},{z},{px},{py},{backend},{nodes},"
            f"{self.jit_time:.4f},{min_time:.4f},{max_time:.4f},{mean_time:.4f},{std_time:.4f},{last_time:.4f},"
            f"{generated_code},{argument_size},{output_size},{temp_size},{flops}\n"
        )

        with open(csv_filename, 'a') as f:
            f.write(csv_line)

        param_dict = {
            "Function": function,
            "Precision": precision,
            "X": x,
            "Y": y,
            "Z": z,
            "PX": px,
            "PY": py,
            "Backend": backend,
            "Nodes": nodes,
        }
        param_dict.update(extra_info)
        profiling_result = {
            "JIT Time": self.jit_time,
            "Min Time": min_time,
            "Max Time": max_time,
            "Mean Time": mean_time,
            "Std Time": std_time,
            "Last Time": last_time,
            "Generated Code": generated_code,
            "Argument Size": argument_size,
            "Output Size": output_size,
            "Temporary Size": temp_size,
            "FLOPS": self.profiling_data["FLOPS"]
        }
        iteration_runs = {}
        for i in range(len(times_array)):
            iteration_runs[f"Run {i}"] = times_array[i]

        with open(md_filename, 'w') as f:
            f.write(f"# Reporting for {function}\n")
            f.write(f"## Parameters\n")
            f.write(
                tabulate(param_dict.items(),
                         headers=["Parameter", "Value"],
                         tablefmt='github'))
            f.write("\n---\n")
            f.write(f"## Profiling Data\n")
            f.write(
                tabulate(profiling_result.items(),
                         headers=["Parameter", "Value"],
                         tablefmt='github'))
            f.write("\n---\n")
            f.write(f"## Iteration Runs\n")
            f.write(
                tabulate(iteration_runs.items(),
                         headers=["Iteration", "Time"],
                         tablefmt='github'))
            f.write("\n---\n")
            f.write(f"## Compiled Code\n")
            f.write(f"```hlo\n")
            f.write(self.compiled_code["COMPILED"])
            f.write(f"\n```\n")
            f.write("\n---\n")
            f.write(f"## Lowered Code\n")
            f.write(f"```hlo\n")
            f.write(self.compiled_code["LOWERED"])
            f.write(f"\n```\n")
            f.write("\n---\n")
            if self.save_jaxpr:
                f.write(f"## JAXPR\n")
                f.write(f"```haskel\n")
                f.write(self.compiled_code["JAXPR"])
                f.write(f"\n```\n")

