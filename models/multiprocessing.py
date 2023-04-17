from typing import Callable
import multiprocessing


class MultiProcessManager:
    def __init__(self, num_processes: int = multiprocessing.cpu_count()):
        self.num_processes = num_processes

    def run(self, task: Callable, data):
        with multiprocessing.Pool(self.num_processes) as pool:
            results = pool.map(task, data)
        return results
