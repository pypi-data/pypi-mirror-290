"""
This module has functionality for performance profiling
"""

import time
from pathlib import Path

from torch.profiler import profile, ProfilerActivity


class Profiler:
    def __init__(self, with_torch: bool, result_dir: Path):
        self.torch_profiler = None
        self.result_dir = result_dir
        self.start_time = 0
        self.end_time = 0
        if with_torch:
            self.torch_profiler = profile(
                activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
                profile_memory=True,
                record_shapes=True,
            )

    def get_runtime(self):
        return self.end_time - self.start_time

    def start(self):
        self.start_time = time.time()
        if self.torch_profiler:
            self.torch_profiler.start()

    def stop(self):
        self.end_time = time.time()

        if self.torch_profiler:
            self.torch_profiler.stop()
