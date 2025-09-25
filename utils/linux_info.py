import os

def mem_total_kb():
    try:
        with open('/proc/meminfo') as f:
            for line in f:
                if line.startswith('MemTotal:'):
                    return int(line.split()[1])
    except Exception:
        return None


def cpu_count_from_proc():
    try:
        with open('/proc/cpuinfo') as f:
            return sum(1 for line in f if line.startswith('processor'))
    except Exception:
        return os.cpu_count()