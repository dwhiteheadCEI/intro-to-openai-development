# Lab 5: Custom App
Let's crate a custom app, bringing together all of the tools we have learned so far to see how they can work together to make a basic game.

## Prerequisites
* An openAI account with credits available
* Basic knowledge of programming in Python
* [VSCode installed](https://code.visualstudio.com/download)
* An understanding of the tools we've used in the previous labs

## Our Custom App
We have a friend that is looking to use OpenAI to make a fun game they can play. What they'd like is to create a mad-lib style version guess-the-thief game where you are able to define some users, talk to them, and figure out which of them committed the crime.

What he would like is an interface where he can define the offense and fill out a description of five possible perpetrators, one of which we'll secretly assign the role of the villain. Then, he'd like to be able to communicate with each one, using his expert detective skills to ask them questions about the offense and see if he can't solve the case. It's a classic 'whodunnit' mystery and we'll have to give him all the tools he needs to be able to solve it.

Thankfully, we already have an interface set up for a game just like this (for some reason)! Let's navigate to it now and give it a quick look.

## Setup
pip install Flask Flask-SocketIO Flask-WTF
cd labfiles/lab6
python app.py

## App Guide
Our app is a classic 'Whodunnit' mystery, only this time, ChatGPT is going to help us by setting the scene and roleplaying our titular characters. 

Run the app and proceed to the setup screen. A default scenario will load that serves as a basic introduction to the game. Feel free to try and run the default, or customize the prompts to your liking.

After the setup page is done loading (note: the call to DallE-3 can take a moment), you'll be presented with images of the suspects as well as chat windows that will allow you to talk to them and ask them questions. The game tends to work best if you 'go along with it' so to speak, but feel free to experiment and have fun! 

Once you feel as though you have a good idea of who did the deed, accuse them and see if your deductive skills paid off!

## Tasks
Our friend is also quite familiar with ChatGPT and has gone ahead and made us some background images to use as well as generated some sample prompts to as character descriptions.

1. (Optional) Your first task is to adjust the existing prompts found in these files:
* 'offense.txt' : The default description for the criminal offense. Can also be changed using the interface while running the app.
* 'suspect1.txt', 'suspect2.txt', 'suspect3.txt': The default descriptions of our suspects. Can also be changed using the interface while running the app.
* 'image-generation': The prompt we're using to help guide DallE-3 into getting a specific image style back.
Remember, we're trying to create a detective game so try to keep it in that style!

2. Next, we'll need to create the call to the chat-completion model to start talking with our app. Edit the 'generate_response' function and add the functionality in. Take note of how we are creating the messages as part of the 'send_message()' route as you'll need to use them as the 'messages' parameter for your call. Remember, our responses should be creative!

Once you're done, try rerunning the application and see if you can start talking with some of our suspects. 

3. Now that we have the chat completion model in, we're going to need to add some image generation so that our game feels a little more 'alive'. Let's update our 'generate_image' function to start using a real model instead of just returning a default image. Use the input we're taking in as the description after it is. 

## Extending our App
Now that our app is up and running, there are a few ways you can challenge yourself if you'd like to take it further. Note, for any testing, it's most likely best to revert the image generation function back to its default state, otherwise your testing may grow to be a little expensive!

1. Proper chat history: Currently, our app only has a very basic chat history implemented. It works okay, but it could definitely be better by utilizing proper storage and things like token summarization and truncation.
2. TTS - Another way to extend the app would be adding text to speech capabilities like what we implemented in Lab3.
3. Better context - There could be a value in adding additional context to our descriptions of the characters via prompting openAI to give us a motive for a crime based off of their description.