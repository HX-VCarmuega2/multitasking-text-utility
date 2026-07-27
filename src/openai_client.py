def create_cliente():
    import os
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key is None:
        raise RuntimeError("OPENAI_API_KEY is missing.")

    client = OpenAI(api_key=api_key)
    
    return client
