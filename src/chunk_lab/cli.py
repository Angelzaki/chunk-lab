from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from chunk_lab.experiment import run_experiment, write_report

console = Console()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="chunk-lab")
    parser.add_argument("--docs", default="samples/docs")
    parser.add_argument("--results", default="results")
    args = parser.parse_args(argv)

    report = run_experiment(Path(args.docs))
    write_report(report, Path(args.results))

    table = Table(title="Chunk Lab")
    table.add_column("strategy")
    table.add_column("chunks", justify="right")
    table.add_column("avg_len", justify="right")
    table.add_column("retrieval", justify="right")
    for name, stats in report["strategies"].items():
        table.add_row(
            name,
            str(stats["chunks"]),
            str(stats["avg_len"]),
            f"{stats['retrieval_score']:.0%}",
        )
    console.print(table)
    console.print(f"best: [bold]{report['best']}[/bold]")
    console.print(f"reportes → {args.results}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
