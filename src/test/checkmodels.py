from openai import OpenAI

client = OpenAI()

response = client.models.list()

for model in response.data:
    print(model.id)
