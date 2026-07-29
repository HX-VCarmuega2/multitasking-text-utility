from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_DIR / "prompts" / "main_prompt.md"
KNOWLEDGE_PATH = BASE_DIR / "data" / "knowledge_base.md"


def load_file(file_path):
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


def create_system_prompt():
    prompt = load_file(PROMPT_PATH)
    knowledge = load_file(KNOWLEDGE_PATH)

    return build_system_prompt(prompt, knowledge)