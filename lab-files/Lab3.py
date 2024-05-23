from openai import OpenAI
import requests

def main():
  client = OpenAI(api_key="")

  while True:
    userInput = input("You: ")
    response = call_openAI_with_tools(client, userInput)
    print("AI: ", response)

def call_openAI_with_tools(client, userInput):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful chatbot that specializes in retrieving information regarding receipts for bakery expenses."},
        {"role": "user", "content": userInput},
    ],
    temperature = 0.2,
    presence_penalty = -1.5,
    frequency_penalty = -1.5,
  )
  return response.choices[0].message.content
    
if __name__ == "__main__":
  main()