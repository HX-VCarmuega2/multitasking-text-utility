import json

from src.openai_client import MODEL_NAME, ask_question, create_client
from src.prompt_builder import create_system_prompt
from src.metrics import build_metrics, save_metrics
from src.moderation import (
    ModerationMiddleware,
    build_output_text,
    check_moderation,
)

def print_response(result):
    confidence = result["confidence"]
    confidence_percent = round(confidence * 100)

    if confidence >= 0.8:
        confidence_label = "Alta"
        confidence_icon = "🟢"
    elif confidence >= 0.5:
        confidence_label = "Media"
        confidence_icon = "🟡"
    else:
        confidence_label = "Baja"
        confidence_icon = "🔴"

    print("\n" + "=" * 55)
    print("🤖 ASISTENTE DE SOPORTE")
    print("=" * 55)

    print("\n📝 Respuesta")
    print("-" * 55)
    print(result["answer"])

    print("\n📊 Confianza")
    print("-" * 55)
    print(
        f"{confidence_icon} {confidence_label} "
        f"({confidence_percent}%)"
    )

    print("\n💡 Acciones recomendadas")
    print("-" * 55)

    actions = result["actions"]

    if actions:
        for action in actions:
            print(f"• {action}")
    else:
        print("• No se recomendaron acciones adicionales.")

    print("\n" + "=" * 55)


def main():
    client = create_client()

    system_prompt = create_system_prompt()

    moderation = ModerationMiddleware(
        client=client,
        threshold=0.70,
    )

    while True:
        question = input("Ingrese su consulta: ").strip()

        if not question:
            print("La consulta no puede estar vacía.")
            return

        moderation_result = check_moderation(
            moderation,
            question,
            description="consulta",
        )

        if moderation_result is not None and not moderation_result.allowed:
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

        output_text = build_output_text(result)

        output_moderation_result = check_moderation(
            moderation,
            output_text,
            description="respuesta",
        )

        if output_moderation_result is not None and not output_moderation_result.allowed:
            print("La respuesta fue bloqueada por el sistema de moderación.")
            return

        metrics = build_metrics(MODEL_NAME, completion, latency, timestamp)

        result["question"] = question
        result["metrics"] = metrics

        print_response(result)

        try:
            save_metrics(result)
        except OSError as error:
            print(f"Advertencia: no se pudieron guardar las métricas: {error}")

        another_query = input(
            "\n¿Desea realizar otra consulta? (s/n): "
        ).strip().lower()

        if another_query not in ["s", "si", "sí"]:
            print("Programa finalizado.")
            break

if __name__ == "__main__":
    main()