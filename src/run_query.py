import json

from src.openai_client import MODEL_NAME, ask_question
from src.prompt_builder import create_system_prompt
from src.metrics import build_metrics, save_metrics

def print_response(result):
    console_output = {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "actions": result["actions"],
    }

    print(json.dumps(console_output, indent=2, ensure_ascii=False))

def main():
    system_prompt = create_system_prompt()

    question = input("Ingrese su consulta: ")

    if not question:
        print("La consulta no puede estar vacía.")
        return

    completion, latency, timestamp = ask_question(system_prompt, question)

    response_content = completion.choices[0].message.content
    result = json.loads(response_content)

    metrics = build_metrics(MODEL_NAME, completion, latency, timestamp)

    result["question"] = question
    result["metrics"] = metrics

    save_metrics(result)
    print_response(result)

if __name__ == "__main__":
    main()