from openai import OpenAI


def main():
  client = OpenAI(api_key="")
  messages = [        
    {"role": "system", "content": "You are a helpful chatbot that responds to prompts politely."}
  ]

  while True:
    userInput = input("You: ")
    response = call_openAI(client, messages)
    print("AI: ", response)

def call_openAI(client, messages):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages= messages,
    temperature = 0.5
  )
  return response.choices[0].message.content
    
if __name__ == "__main__":
  main()