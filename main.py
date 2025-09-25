import argparse
from benchmarks.benchmarks import run_benchmarks
from utils.data_gen import generate_dataset
from rich.console import Console

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Sorting Algorithm Benchmark Tool")
    parser.add_argument("--size", type=int, default=10000, help="Dataset size")
    parser.add_argument("--chart", action="store_true", help="Plot results with matplotlib")
    args = parser.parse_args()

    console.print(f"[bold green]Generating dataset of {args.size} elements...[/bold green]")
    data = generate_dataset(args.size)

    console.print("[bold blue]Running benchmarks...[/bold blue]")
    results = run_benchmarks(data)

    if args.chart:
        import matplotlib.pyplot as plt
        names = list(results.keys())
        times = list(results.values())
        plt.bar(names, times)
        plt.title("Sorting Algorithm Benchmark")
        plt.ylabel("Time (s)")
        plt.show()
    else:
        from rich.table import Table
        table = Table(title="Benchmark Results")
        table.add_column("Algorithm")
        table.add_column("Time (s)")
        for algo, t in results.items():
            table.add_row(algo, f"{t:.6f}")
        console.print(table)

if __name__ == "__main__":
    main()
