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
    tools=[
      {
        "type": "function",
        "function": {
          "name": "get_latest_receipt",
          "description": "Get the most recent receipt for a supply purchase. Information stored in the receipt includes total cost and individual costs per item.",
        }
      },
      {
        "type": "function",
        "function": {
          "name": "get_random_recipe",
          "description": "Get a random recipe. Best used when somebody is looking for inspiration on what food to cook.",
        }
      }
    ],
    tool_choice="auto"
  )

  if(response.choices[0].finish_reason == "tool_calls"):
    if(response.choices[0].message.tool_calls[0].function.name == "get_latest_receipt"):
      return "Sure, here is your latest receipt: " + get_latest_receipt()
    elif(response.choices[0].message.tool_calls[0].function.name == "get_random_recipe"):
      recipe_response = get_random_recipe()
      recipe_json = recipe_response.json()
      recipe = recipe_json['meals'][0]
      return f"Here's a random recipe I found: {recipe['strMeal']} -- {recipe['strInstructions']}"
  else:
    return response.choices[0].message.content

def get_latest_receipt():
  with open("../documents/bakeryReceipt.txt") as file:
    data = file.read()
  return data

def get_random_recipe():
  url = "https://www.themealdb.com/api/json/v1/1/random.php"
  response = requests.get(url)
  return response
    
if __name__ == "__main__":
  main()