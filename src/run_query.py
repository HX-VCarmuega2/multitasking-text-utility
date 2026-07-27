from openai_client import create_cliente
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()



client = create_cliente()

system_prompt = load_prompt(BASE_DIR / "prompts" / "main_prompt.md")

question = input("Ingrese su consulta: ")

completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature = 0.2,
        max_completion_tokens = 250
    )

response = completion.choices[0].message.content

print(response)