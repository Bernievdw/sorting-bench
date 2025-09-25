import time
import csv
import json
import statistics
from utils.data_gen import generate_dataset

AVAILABLE_ALGOS = {
    "shell_sort": None,  
    "counting_sort": None,
}


def _single_run(func, arr, measure_memory=False):
    try:
        process = None
        mem_before = None
        if measure_memory:
            import psutil
            process = psutil.Process()
            mem_before = process.memory_info().rss

        start = time.perf_counter()
        func(arr)
        end = time.perf_counter()

        mem_after = process.memory_info().rss if process else None
        mem_used = (mem_after - mem_before) if (process and mem_before is not None) else None

        return {"time": end - start, "mem": mem_used, "error": None}

    except Exception as e:
        return {"time": None, "mem": None, "error": str(e)}


def run_benchmarks(
    sizes,
    case="random",
    algos=None,
    repeats=3,
    measure_memory=False,
):

    if algos is None:
        algos = list(AVAILABLE_ALGOS.keys())

    results = {}
    for name in algos:
        if name not in AVAILABLE_ALGOS:
            raise ValueError(f"Unknown algorithm: {name}")
        results[name] = {"sizes": [], "times": [], "mems": [], "errors": []}

    for size in sizes:
        for name in algos:
            func = AVAILABLE_ALGOS[name]
            times = []
            mems = []
            errors = []

            for _ in range(repeats):
                data = generate_dataset(size, case=case)
                arr = data.copy() 

                r = _single_run(func, arr, measure_memory=measure_memory)

                if r["time"] is not None:
                    times.append(r["time"])
                else:
                    errors.append(r.get("error"))

                if r.get("mem") is not None:
                    mems.append(r.get("mem"))

            avg_time = statistics.mean(times) if times else None
            avg_mem = statistics.mean(mems) if mems else None

            results[name]["sizes"].append(size)
            results[name]["times"].append(avg_time)
            results[name]["mems"].append(avg_mem)
            results[name]["errors"].append(errors or None)

    return results


def save_results_csv(results, path):
    rows = []
    for algo, data in results.items():
        for i, size in enumerate(data["sizes"]):
            rows.append(
                {
                    "algorithm": algo,
                    "size": size,
                    "time_s": data["times"][i],
                    "mem_bytes": data["mems"][i],
                    "errors": data["errors"][i],
                }
            )

    fieldnames = ["algorithm", "size", "time_s", "mem_bytes", "errors"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def save_results_json(results, path):
    with open(path, "w") as f:
        json.dump(results, f, indent=2, default=str)
