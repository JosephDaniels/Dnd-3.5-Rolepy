import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Say hi in a pirate voice."}
    ]
)

print(response.choices[0].message['content'])
