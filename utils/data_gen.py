import os
import random


def generate_random_dataset(size):
    raw = os.urandom(size * 4)
    nums = [int.from_bytes(raw[i:i+4], "little") for i in range(0, len(raw), 4)]
    return nums[:size]


def generate_dataset(size, case="random"):
    if case == "random":
        data = generate_random_dataset(size)
    elif case == "sorted":
        data = sorted(generate_random_dataset(size))
    elif case == "reversed":
        data = sorted(generate_random_dataset(size), reverse=True)
    else:
        raise ValueError("Unknown case: choose random, sorted, or reversed")
    return data


def size_from_memory_fraction(fraction=0.01, bytes_per_item=4):
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    parts = line.split()
                    kb = int(parts[1])
                    total_bytes = kb * 1024
                    return max(1, int((total_bytes * fraction) // bytes_per_item))
    except FileNotFoundError:
        try:
            import psutil
            return max(1, int((psutil.virtual_memory().total * fraction) // bytes_per_item))
        except Exception:
            return 10000


def size_from_proc_process_count(multiplier=100):
    try:
        entries = os.listdir('/proc')
        pids = [e for e in entries if e.isdigit()]
        return max(1, len(pids) * multiplier)
    except Exception:
        return 1000  
