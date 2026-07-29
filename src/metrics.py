import csv
from pathlib import Path

MODEL_PRICING = {
    "gpt-4o-mini": {
        "input_per_million": 0.15,
        "output_per_million": 0.60,
    }
}

def calculate_cost(model_name, prompt_tokens, completion_tokens):
    pricing = MODEL_PRICING.get(model_name)

    if pricing is None:
        raise ValueError(f"Pricing is not configured for model: {model_name}")

    input_cost = (
        prompt_tokens / 1_000_000
    ) * pricing["input_per_million"]

    output_cost = (
        completion_tokens / 1_000_000
    ) * pricing["output_per_million"]

    return round(input_cost + output_cost, 6)

def build_metrics(model_name, completion, latency, timestamp):
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    total_tokens = completion.usage.total_tokens

    total_cost = calculate_cost(model_name, prompt_tokens, completion_tokens)

    return {
        "timestamp": timestamp,
        "model": completion.model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "latency_ms": latency,
        "estimated_cost_usd": total_cost
    }

def build_csv_row(result):
    metrics = result["metrics"]

    return {
        "timestamp": metrics["timestamp"],
        "question": result["question"],
        "answer": result["answer"],
        "confidence": result["confidence"],
        "actions": " | ".join(result["actions"]),
        "model": metrics["model"],
        "prompt_tokens": metrics["prompt_tokens"],
        "completion_tokens": metrics["completion_tokens"],
        "total_tokens": metrics["total_tokens"],
        "latency_ms": metrics["latency_ms"],
        "estimated_cost_usd": metrics["estimated_cost_usd"],
    }

def get_csv_path():
    project_root = Path(__file__).resolve().parent.parent
    return project_root / "metrics" / "metrics.csv"

def save_metrics(result):
    csv_row = build_csv_row(result)
    file_path = get_csv_path()

    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = file_path.exists()

    with file_path.open(
        mode="a",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=csv_row.keys(),
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(csv_row)