from pathlib import Path

from chunk_lab.experiment import run_experiment
from chunk_lab.strategies import by_paragraph, by_sentence, fixed_size

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "samples" / "docs"


def test_strategies_produce_chunks():
    text = (DOCS / "politica_a1.txt").read_text(encoding="utf-8")
    assert fixed_size("politica_a1", text)
    assert by_paragraph("politica_a1", text)
    assert by_sentence("politica_a1", text)


def test_experiment_ranks_strategies():
    report = run_experiment(DOCS)
    assert "best" in report
    assert set(report["strategies"]) == {"fixed", "paragraph", "sentence"}
    assert report["strategies"][report["best"]]["retrieval_score"] >= 0.5
