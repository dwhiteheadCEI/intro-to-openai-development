from openai import OpenAI

client = OpenAI(api_key="")

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
      {"role": "system", "content": "You are a helpful chatbot who answers questions in a polite manner."},
      {"role": "user", "content": "Hello! Who are you?"},
  ]
)

print(response)