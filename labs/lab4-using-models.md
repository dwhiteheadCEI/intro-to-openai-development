# Lab 4: Using OpenAI Models
In this lab, we'll go over calling different models that are offered as part of the OpenAI API. We'll be taking a look at DALL-E as well as the TTS and Moderation models. 

## Prerequisites
* An openAI account with credits available
* Basic knowledge of programming in Python
* [VSCode installed](https://code.visualstudio.com/download)

## Image Creation with DALL-E
Be sure to check the official documentation [here](https://platform.openai.com/docs/guides/images/introduction)
Let's say we want to encorporate some image creation into our custom app. Let's take a look at how to do just that.

Replace the 'return' line in your _'get-image-response'_ function definition with the following:
  response = client.images.generate(
    model="dall-e-3",
    prompt=userInput,
    size="1024x1024",
    quality="standard",
    n=1,
  )
  return response.data[0].url

Note the different parameters we are using. The 'model' is what controls which model of image creation we are using, the 'prompt' is what is defining the image to be created and the 'size' and 'quality' determine the resolution and detail of image we get back.
The _'n'_ parameter is the number of images we want the model to generate.

Now run the following commands:
    cd lab-files
    py lab4.py

Follow the link to see the result! How did the image turn out? Try creating some custom images by editing the prompt. Be sure to comment out the call to _'get-image-response'_ before running the other endpoints to save on token usage.

## Chat Moderation
If your custom has need of proper moderation, we can take advantage of the moderation model to check for content flags and return grades for potential harmful or inappropriate language.

Replace the 'return' line in your _'get-moderation-response'_ function definition with the following:
  response = client.moderations.create(input=userInput)
  return response.results[0]

Now run the following commands:
    cd lab-files
    py lab4.py

Note the extensive response. Check [this page](https://platform.openai.com/docs/guides/moderation/overview) for a full breakdown of all of the different response fields. 

Be sure to comment out the call to _'get-moderation-response'_ before running the other endpoints to save on token usage.

## Text to Speech
Another very common usecase for a chatbot is to have text-to-speech as an accessibility option. Let's take a look at how to implement this functionality.

Replace the 'return' line in your _'get-tts-response'_ function definition with the following:
  speech_file_path = Path(__file__).parent / "speech.mp3"
  response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=userInput
  )
  response.stream_to_file(speech_file_path)

This response is going to return a .mp3 file to our specified folder. Check [this page](https://platform.openai.com/docs/guides/text-to-speech) for supported voices as well as file output types.

Now run the following commands:
    cd lab-files
    py lab4.py

Now, navigate to the file created and give it a listen.

How did the resulting file turn out? If it's not what you expected or would like to hear variations try to edit the prompt or voice being used. 

That does it for this lab. Now that we've walked through how to use some of these models, we'll use what we've learned to create a custom app that leverages different openAI models in the next lab.