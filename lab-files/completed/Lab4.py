from openai import OpenAI
from pathlib import Path

def main():
  client = OpenAI(api_key="")

  response = get_image_response(client, "A helpful robot with a fun hat.")
  print(response)

  # response = get_moderation_response(client, "Hello, how are you doing today?")
  # print(response)

  # response = get_tts_response(client, "Today is going to be a very productive day!")
  # print(response)

def get_image_response(client, userInput):
  response = client.images.generate(
    model="dall-e-3",
    prompt=userInput,
    size="1024x1024",
    quality="standard",
    n=1,
  )
  return response.data[0].url

def get_moderation_response(client, userInput):
  response = client.moderations.create(input=userInput)

  return response.results[0]

def get_tts_response(client, userInput):
  speech_file_path = Path(__file__).parent / "speech.mp3"
  response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=userInput
  )
  response.stream_to_file(speech_file_path)
    
if __name__ == "__main__":
  main()