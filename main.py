import argparse
import sys
from rich.console import Console
from rich.table import Table

from benchmarks.benchmark import run_benchmarks, save_results_csv, save_results_json
from utils.data_gen import size_from_memory_fraction, size_from_proc_process_count

console = Console()


def parse_sizes(sizes_arg, multi=False):
    if sizes_arg:
        parts = [p.strip() for p in sizes_arg.split(",") if p.strip()]
        sizes = [int(x) for x in parts]
    else:
        if multi:
            sizes = [1000, 5000, 10000, 50000, 100000]
        else:
            sizes = [10000]
    return sizes


def pretty_print_single(results, case, repeats, measure_memory):
    table = Table(title="Benchmark Results")
    table.add_column("Algorithm")
    table.add_column("Size")
    table.add_column("Time (s)")
    if measure_memory:
        table.add_column("Mem (KB)")
    table.add_column("Errors")

    for algo, data in results.items():
        for i, size in enumerate(data["sizes"]):
            t = data["times"][i]
            mem = data["mems"][i]
            err = data["errors"][i]
            mem_kb = f"{int(mem/1024)}" if (mem is not None) else "-"
            table.add_row(
                algo,
                str(size),
                f"{t:.6f}" if t else "-",
                mem_kb if measure_memory else "-",
                str(err) if err else "-"
            )
    console.print(table)


def plot_results(results, sizes, chart_path=None):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    for algo, data in results.items():
        times = data["times"]
        plt.plot(sizes, times, marker="o", label=algo)

    plt.xlabel("Dataset size")
    plt.ylabel("Time (s)")
    plt.title("Sorting Algorithm Benchmark")
    plt.legend()
    plt.grid(True)
    if chart_path:
        plt.savefig(chart_path)
        console.print(f"Chart saved to {chart_path}")
    else:
        plt.show()


def interactive_mode():
    console.print("[bold green]Interactive mode[/bold green]")
    sizes_text = input("Enter comma-separated sizes (or leave blank for defaults): ")
    multi = input("Run multiple sizes? [y/N]: ").lower().startswith("y")
    cases_text = input("Cases (random,sorted,reversed) comma-separated (default: random): ")
    algos_text = input("Algorithms (comma-separated names or 'all') (default: all): ")
    repeats = int(input("Repeats per test (default 3): ") or 3)
    mem_y = input("Measure memory? [y/N]: ").lower().startswith("y")
    chart_y = input("Show chart after run? [y/N]: ").lower().startswith("y")
    out = input("Output CSV path (or leave blank): ")

    sizes = parse_sizes(sizes_text, multi=multi)
    cases = [c.strip() for c in cases_text.split(",") if c.strip()] or ["random"]
    algos = None if not algos_text or algos_text.strip().lower() == "all" else [
        a.strip() for a in algos_text.split(",")
    ]

    results = run_benchmarks(
        sizes,
        case=cases[0],
        algos=algos,
        repeats=repeats,
        measure_memory=mem_y
    )
    pretty_print_single(results, cases[0], repeats, mem_y)
    if chart_y:
        plot_results(results, sizes)
    if out:
        save_results_csv(results, out)
        console.print(f"Results saved to {out}")


def main():
    parser = argparse.ArgumentParser(description="Sorting Algorithm Benchmark Tool — extended")
    parser.add_argument("--sizes", type=str, help="Comma-separated dataset sizes (e.g. 1000,5000,10000)")
    parser.add_argument("--multi", action="store_true", help="Use multi default sizes if --sizes is omitted")
    parser.add_argument("--cases", type=str, default="random", help="Dataset case(s): random,sorted,reversed (comma-separated)")
    parser.add_argument("--algos", type=str, default="all", help="Comma-separated list of algorithm names or 'all'")
    parser.add_argument("--repeats", type=int, default=3, help="Repeats per test")
    parser.add_argument("--memory", action="store_true", help="Measure memory (RSS) delta")
    parser.add_argument("--output", type=str, help="CSV (or .json) output path")
    parser.add_argument("--chart", action="store_true", help="Show matplotlib chart")
    parser.add_argument("--interactive", action="store_true", help="Interactive prompt mode")
    parser.add_argument("--from-ram-fraction", type=float, help="Set an automatic size using fraction of RAM (e.g. 0.01)")
    parser.add_argument("--from-proc-multiplier", type=int, help="Set an automatic size using /proc process count * multiplier")

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
        sys.exit(0)

    if args.from_ram_fraction:
        size = size_from_memory_fraction(args.from_ram_fraction)
        sizes = [size]
    elif args.from_proc_multiplier:
        size = size_from_proc_process_count(args.from_proc_multiplier)
        sizes = [size]
    else:
        sizes = parse_sizes(args.sizes, multi=args.multi)

    cases = [c.strip() for c in args.cases.split(",") if c.strip()]
    algos = None if args.algos.strip().lower() == "all" else [a.strip() for a in args.algos.split(",")]

    case = cases[0]

    console.print(f"[bold green]Generating and running benchmarks for case={case}, sizes={sizes}[/bold green]")
    results = run_benchmarks(
        sizes,
        case=case,
        algos=algos,
        repeats=args.repeats,
        measure_memory=args.memory
    )

    pretty_print_single(results, case, args.repeats, args.memory)

    if args.output:
        if args.output.lower().endswith(".json"):
            save_results_json(results, args.output)
        else:
            save_results_csv(results, args.output)
        console.print(f"Results exported to {args.output}")

    if args.chart:
        plot_results(results, sizes)


if __name__ == "__main__":
    main()
