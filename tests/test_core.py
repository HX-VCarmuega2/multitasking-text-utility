import pytest

from src.metrics import calculate_cost, build_csv_row, build_metrics, calculate_cost, get_csv_path
from types import SimpleNamespace


def test_calculate_cost():
    result = calculate_cost(
        "gpt-4o-mini",
        prompt_tokens=100,
        completion_tokens=50,
    )

    expected = 0.000045

    assert result == expected


def test_build_csv_row():
    result = {
        "question": "¿Cómo restablezco mi contraseña?",
        "answer": "Podés restablecerla desde la pantalla de inicio de sesión.",
        "confidence": 0.95,
        "actions": [
            "Open the login screen",
            "Select forgot password",
        ],
        "metrics": {
            "timestamp": "2026-07-29T18:30:00",
            "model": "gpt-4o-mini-2024-07-18",
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150,
            "latency_ms": 1200.5,
            "estimated_cost_usd": 0.000045,
        },
    }

    csv_row = build_csv_row(result)

    assert csv_row["question"] == "¿Cómo restablezco mi contraseña?"
    assert csv_row["confidence"] == 0.95
    assert csv_row["actions"] == (
        "Open the login screen | Select forgot password"
    )
    assert csv_row["total_tokens"] == 150


def test_build_metrics():
    completion = SimpleNamespace(
        model="gpt-4o-mini-2024-07-18",
        usage=SimpleNamespace(
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
        ),
    )

    metrics = build_metrics(
        "gpt-4o-mini",
        completion,
        latency=1.25,
        timestamp="2026-07-29T18:30:00",
    )

    assert metrics["timestamp"] == "2026-07-29T18:30:00"
    assert metrics["model"] == "gpt-4o-mini-2024-07-18"
    assert metrics["prompt_tokens"] == 100
    assert metrics["completion_tokens"] == 50
    assert metrics["total_tokens"] == 150
    assert metrics["estimated_cost_usd"] == 0.000045

def test_calculate_cost_raises_error_for_unknown_model():
    with pytest.raises(ValueError):
        calculate_cost(
            "unknown-model",
            prompt_tokens=100,
            completion_tokens=50,
        )

def test_get_csv_path():
    path = get_csv_path()

    assert path.name == "metrics.csv"
    assert path.parent.name == "metrics"