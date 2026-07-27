from openai_client import create_cliente
from pathlib import Path

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


client = create_cliente()

prompt = load_prompt(BASE_DIR / "prompts" / "main_prompt.md")
knowledge = load_prompt(BASE_DIR / "data" / "knowledge_base.md")
system_prompt = build_system_prompt(prompt, knowledge)

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