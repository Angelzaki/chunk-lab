from __future__ import annotations

import json
from pathlib import Path

from chunk_lab.metrics import retrieval_hit, strategy_stats
from chunk_lab.strategies import STRATEGIES


QUERIES = [
    ("¿Cuál es el descuento máximo en A1?", "politica_a1"),
    ("¿A2 exige MFA?", "requisitos_a2"),
    ("¿Cuál es el límite comercial mensual?", "limite_comercial"),
]


def load_docs(docs_dir: Path) -> dict[str, str]:
    docs = {}
    for path in sorted(docs_dir.glob("*.txt")):
        docs[path.stem] = path.read_text(encoding="utf-8")
    return docs


def run_experiment(docs_dir: Path) -> dict:
    docs = load_docs(docs_dir)
    report = {"strategies": {}}
    for name, fn in STRATEGIES.items():
        chunks = []
        for doc_id, text in docs.items():
            chunks.extend(fn(doc_id, text))
        hits = sum(1 for q, expected in QUERIES if retrieval_hit(chunks, q, expected))
        report["strategies"][name] = {
            **strategy_stats(chunks),
            "retrieval_hits": hits,
            "retrieval_total": len(QUERIES),
            "retrieval_score": round(hits / len(QUERIES), 4),
        }
    best = max(report["strategies"].items(), key=lambda x: x[1]["retrieval_score"])
    report["best"] = best[0]
    return report


def write_report(report: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "chunk_experiment.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    lines = ["# Chunk Lab", "", f"best: **{report['best']}**", "", "| strategy | chunks | avg_len | retrieval |", "|---|---:|---:|---:|"]
    for name, stats in report["strategies"].items():
        lines.append(
            f"| {name} | {stats['chunks']} | {stats['avg_len']} | {stats['retrieval_score']:.0%} |"
        )
    (out_dir / "chunk_experiment.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
