import json

from src.openai_client import MODEL_NAME, ask_question, create_client
from src.prompt_builder import create_system_prompt
from src.metrics import build_metrics, save_metrics
from src.moderation import ModerationMiddleware

def print_response(result):
    console_output = {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "actions": result["actions"],
    }

    print(json.dumps(console_output, indent=2, ensure_ascii=False))

def main():
    client = create_client()

    system_prompt = create_system_prompt()

    moderation = ModerationMiddleware(
        client=client,
        threshold=0.70,
    )

    question = input("Ingrese su consulta: ").strip()

    if not question:
        print("La consulta no puede estar vacía.")
        return

    moderation_result = moderation.check(question)

    if not moderation_result.allowed:
        print("La consulta fue bloqueada por el sistema de moderación.")
        return
        
    try:
        completion, latency, timestamp = ask_question(client, system_prompt, question)
    except Exception as e:
        print(f"Error al realizar la consulta: {e}")
        return

    if not completion.choices:
        print("Error: el modelo no devolvió ninguna respuesta.")
        return

    response_content = completion.choices[0].message.content

    if not response_content:
        print("Error: la respuesta del modelo está vacía.")
        return

    try:
        result = json.loads(response_content)
    except json.JSONDecodeError:
        print("Error: el modelo devolvió una respuesta JSON inválida.")
        return

    metrics = build_metrics(MODEL_NAME, completion, latency, timestamp)

    result["question"] = question
    result["metrics"] = metrics

    print_response(result)

    try:
        save_metrics(result)
    except OSError as error:
        print(f"Advertencia: no se pudieron guardar las métricas: {error}")

if __name__ == "__main__":
    main()