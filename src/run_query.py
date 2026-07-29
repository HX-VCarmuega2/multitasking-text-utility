from src.openai_client import ask_question
from src.prompt_builder import create_system_prompt
from src.metrics import build_metrics
from src.metrics import save_metrics
import json

def main():
    system_prompt = create_system_prompt()

    question = input("Ingrese su consulta: ")

    completion, latency, timestamp = ask_question(system_prompt, question)

    response_content = completion.choices[0].message.content
    result = json.loads(response_content)

    metrics = build_metrics("gpt-4o-mini", completion, latency, timestamp)

    result["question"] = question
    result["metrics"] = metrics

    save_metrics(result)

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()