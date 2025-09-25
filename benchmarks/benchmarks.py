import time
from algorithms import bubble, quicksort, mergesort, heapsort, radix

def run_benchmarks(data):
    algorithms = {
        "Bubble Sort": bubble.sort,
        "Quicksort": quicksort.sort,
        "Mergesort": mergesort.sort,
        "Heapsort": heapsort.sort,
        "Radix Sort": radix.sort,
    }

    results = {}
    for name, func in algorithms.items():
        arr = data.copy()
        start = time.perf_counter()
        func(arr)
        end = time.perf_counter()
        results[name] = end - start
    return results