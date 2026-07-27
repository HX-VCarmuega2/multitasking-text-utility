from openai_client import create_cliente

client = create_cliente()



completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {
                "role": "user",
                "content": "Hola, ¿quién sos?"
            }
        ]
    )

response = completion.choices[0].message.content

print(response)