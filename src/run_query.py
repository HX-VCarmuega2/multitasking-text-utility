from src.openai_client import ask_question
from src.prompt_builder import create_system_prompt
from src.metrics import build_metrics
import json

def main():
    system_prompt = create_system_prompt()

    question = input("Ingrese su consulta: ")

    completion, latency, timestamp = ask_question(system_prompt, question)

    response_content = completion.choices[0].message.content
    response = json.loads(response_content)

    metrics = build_metrics("gpt-4o-mini", completion, latency, timestamp)

    response["metrics"] = metrics

    print(json.dumps(response, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()