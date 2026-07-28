from openai_client import create_cliente, ask_question
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent


def load_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def build_system_prompt(prompt, knowledge):
    return f"""
{prompt}

=========================
KNOWLEDGE BASE
=========================

{knowledge}
"""

prompt = load_prompt(BASE_DIR / "prompts" / "main_prompt.md")
knowledge = load_prompt(BASE_DIR / "data" / "knowledge_base.md")
system_prompt = build_system_prompt(prompt, knowledge)

question = input("Ingrese su consulta: ")

completion, latency, timestamp = ask_question(system_prompt, question)

response_content = completion.choices[0].message.content
response = json.loads(response_content)


prompt_tokens = completion.usage.prompt_tokens
completion_tokens = completion.usage.completion_tokens
total_tokens = completion.usage.total_tokens


input_cost = (prompt_tokens / 1_000_000) * 0.15

output_cost = (completion_tokens / 1_000_000) * 0.60

total_cost = round(input_cost + output_cost, 6)

response["metrics"] = {
    "timestamp": timestamp,
    "model": completion.model,
    "prompt_tokens": completion.usage.prompt_tokens,
    "completion_tokens": completion.usage.completion_tokens,
    "total_tokens": completion.usage.total_tokens,
    "latency_ms": latency,
    "estimated_cost_usd": total_cost
}

print(json.dumps(response, indent=2, ensure_ascii=False))