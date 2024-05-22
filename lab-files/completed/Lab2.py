from openai import OpenAI

client = OpenAI(api_key="")

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
      {"role": "system", "content": "You are a helpful chatbot that specializes in retrieving information regarding receipts for bakery expenses."},
      {"role": "system", "content": "The user's most recent expense was for $52.99 and included the purchase of flour, vanilla, sugar, eggs and cocoa powder."},
      {"role": "user", "content": "How much did my last purchase cost?"},
  ],
  temperature = 0.2,
  presence_penalty = -1.5,
  frequency_penalty = -1.5
)

print(response)