from openai import OpenAI
from pathlib import Path

def main():
  client = OpenAI(api_key="")

  # response = get_image_response(client, "A helpful robot with a fun hat.")
  # print(response)

  # response = get_moderation_response(client, "Hello, how are you doing today?")
  # print(response)

  # response = get_tts_response(client, "Today is going to be a very productive day!")
  # print(response)

def get_image_response(client, userInput):
  return

def get_moderation_response(client, userInput):
  return

def get_tts_response(client, userInput):
  return
    
if __name__ == "__main__":
  main()