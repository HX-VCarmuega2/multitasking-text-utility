import os
from dotenv import load_dotenv
from openai import OpenAI
import time
import datetime


MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.2
MAX_COMPLETION_TOKENS = 250


def create_client():
    
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key is None:
        raise RuntimeError("OPENAI_API_KEY is missing.")

    client = OpenAI(api_key=api_key)
    
    return client

def ask_question(system_prompt, question):

    client = create_client()

    timestamp = datetime.now().isoformat(timespec="seconds")
    start = time.perf_counter()

    completion = client.chat.completions.create(
        model=MODEL_NAME,
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
        temperature = TEMPERATURE,
        max_completion_tokens = MAX_COMPLETION_TOKENS,
        response_format={"type": "json_object"}
    )

    end = time.perf_counter()

    latency = round((end - start) * 1000 ) # Convert to milliseconds

    return completion, latency, timestamp