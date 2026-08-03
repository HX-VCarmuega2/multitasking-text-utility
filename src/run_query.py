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
        confidence_label = "High"
        confidence_icon = "🟢"
    elif confidence >= 0.5:
        confidence_label = "Medium"
        confidence_icon = "🟡"
    else:
        confidence_label = "Low"
        confidence_icon = "🔴"

    print("\n" + "=" * 55)
    print("🤖 SUPPORT ASSISTANT")
    print("=" * 55)

    print("\n📝 Answer")
    print("-" * 55)
    print(result["answer"])

    print("\n📊 Confidence")
    print("-" * 55)
    print(
        f"{confidence_icon} {confidence_label} "
        f"({confidence_percent}%)"
    )

    print("\n💡 Recommended actions")
    print("-" * 55)

    actions = result["actions"]

    if actions:
        for action in actions:
            print(f"• {action}")
    else:
        print("• No additional actions were recommended.")

    print("\n" + "=" * 55)


def main():
    client = create_client()

    system_prompt = create_system_prompt()

    moderation = ModerationMiddleware(
        client=client,
        threshold=0.70,
    )

    while True:
        question = input("Enter your query: ").strip()

        if not question:
            print("The query cannot be empty.")
            return

        moderation_result = check_moderation(
            moderation,
            question,
            description="query",
        )

        if moderation_result is not None and not moderation_result.allowed:
            print("The query was blocked by the moderation system.")
            return

        try:
            completion, latency, timestamp = ask_question(client, system_prompt, question)
        except Exception as e:
            print(f"Error while processing the query: {e}")
            return

        if not completion.choices:
            print("Error: the model did not return any response.")
            return

        response_content = completion.choices[0].message.content

        if not response_content:
            print("Error: the model response is empty.")
            return

        try:
            result = json.loads(response_content)
        except json.JSONDecodeError:
            print("Error: the model returned an invalid JSON response.")
            return

        output_text = build_output_text(result)

        output_moderation_result = check_moderation(
            moderation,
            output_text,
            description="response",
        )

        if output_moderation_result is not None and not output_moderation_result.allowed:
            print("The response was blocked by the moderation system.")
            return

        metrics = build_metrics(MODEL_NAME, completion, latency, timestamp)

        result["question"] = question
        result["metrics"] = metrics

        print_response(result)

        try:
            save_metrics(result)
        except OSError as error:
            print(f"Warning: metrics could not be saved: {error}")

        another_query = input(
            "\nWould you like to make another query? (y/n): "
        ).strip().lower()

        if another_query not in ["y", "yes"]:
            print("Program finished.")
            break

if __name__ == "__main__":
    main()