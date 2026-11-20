"""Verifica las métricas sin consumir la API generativa."""
import runpy
from pathlib import Path

from ai_support_engine.models import AnalyzeResponse

SCRIPT = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts" / "compare_engines.py"))


def test_reference_cases_are_complete():
    cases = SCRIPT["CASES"]
    assert len(cases) >= 10
    assert sum(case[3] == "adversarial" for case in cases) >= 2
    assert any(case[3] == "ambiguo" for case in cases)
    assert all(category and priority for _, category, priority, _ in cases)


def test_accuracy_uses_all_cases():
    rows = [
        {"traditional": {"format_valid": True, "category_correct": True, "priority_correct": True}},
        {"traditional": {"format_valid": True, "category_correct": False, "priority_correct": True}},
        {"traditional": {"format_valid": False, "category_correct": False, "priority_correct": False}},
    ]
    stats = SCRIPT["summarize"](rows, "traditional")
    assert stats["total_cases"] == 3
    assert stats["valid_responses"] == 2
    assert stats["category_accuracy_percent"] == 33.33
    assert stats["priority_accuracy_percent"] == 66.67


def test_record_validates_category_and_priority():
    result = AnalyzeResponse(
        category="ACCESS", priority="MEDIUM", response="Recupera tu acceso.",
        requiresHumanReview=False, mode="traditional",
    )
    row = SCRIPT["record"](result, "ACCESS", "HIGH")
    assert row["format_valid"] is True
    assert row["category_correct"] is True
    assert row["priority_correct"] is False
