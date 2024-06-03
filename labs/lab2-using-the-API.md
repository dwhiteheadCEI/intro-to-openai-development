# Lab 2: Using the OpenAI API 
Now that we have a better understanding of ChatGPT and what it's capabilities are, let's take a look at the API. In this lab, we're going to be taking a deeper dive into OpenAI by creating a custom app for a bakery that creates a prompt, makes a call to the OpenAI model API and reads the response sent back.

## Prerequisites
* An openAI account with credits available
* _Very_ Basic knowledge of programming in Python
* [VSCode installed](https://code.visualstudio.com/download)

## Setup
First, we'll need to generate a new Project API key. Locate the API key page of your OpenAI account [here](https://platform.openai.com/api-keys)

You'll also want to make sure you have available credits on your account.
You can check your available API credits [here](https://platform.openai.com/usage)
If no credits are available, be sure to add billing and allowance [here](https://platform.openai.com/settings/organization/billing/overview)

In VSCode let's open a terminal and run the following command:
    pip install openai

Now, let's work on our first lab file. Navigate to the "lab-files" folder and select "lab2.py". 

At the top, take note of how we are setting up our OpenAI client, be sure to replace the "YOUR_API_KEY" with the key you just generated. 

When making a call to openAI, the first thing we need to do is set a model. For this lab, we'll be using "gpt-3.5-turbo". 

Let's run our app:
    cd lab-files
    py lab2.py

Great! We're already able to communicate with our bot via the API. It's important to note that all context regarding our session is hardcoded and as such our session will not be persistent across multiple executions of our app. To do this, we'll need to take advantage of a persistent chat store which we will discuss later in the lab series.

## Customizing our Chatbot
Let's take a look at the 'messages' field. Every call we make to OpenAI will have this field as it contains our prompt to the service. Additionally, this is where we can give our model a little bit of context that changes depending on the role we assign to the message.
* User: A user prompt. This role will typically be used to help give the bot a better idea of user info or prepare the chat for upcoming questions and will serve as our prompt that we are getting a response back for.
* Assistant: A simulated bot response. This is a great role to use to try and help format responses. 
* System: Instructions for the bot to keep in mind.

We'd like to add a bit of functionality to our baking app that makes it a little more personalized to our use-case. Remove all of the existing messages in the request and lets add some new messages from scratch.

First, let's add a new _'system'_ message that will help define our bot's personality and intent.
Copy this into the _'content'_ field under for the _'system'_ message:
    "You are a helpful chatbot that specializes in retrieving information regarding receipts for bakery expenses."

Next, let's add another _'system'_ message that will contain some information we want it to have before answering our prompt. Create a new message and paste this in to the content of that message:
    "My most recent expense was for $52.99 and included the purchase of flour, vanilla, sugar, eggs and cocoa powder."

The chatbot will now be able to have that context going forward. 
Let's add a _'user'_ message that will serve as our prompt. Create a new message and paste this in to the content of that message:
    "What was the cost of my most recent expense?"

Let's run our app:
    cd lab-files
    py Lab2.py

Awesome! We now have a chatbot that is able to take some data into account, identify when to use that data and output responses using that data. 

## Customizing our App
There are a number of optional parameters we can add to our call to help make our app fit our use-case a little better.

The first change we'll make is with the _'temperature'_ parameter. 
_'Temperature'_ is how we tell our chatbot how creative we want it to be in its responses. The value of the temperature can be between 0-2, with 0 being the least variety and 2 being the most. Our bakery app right now is for relaying old data, so we really don't want it to be giving a variety of responses for the same question. For this app, let's add the following:
    temperature = 0.2

The next thing that we'll add is the _'presence_penalty'_ parameter.
_'Presence Penalty'_ is a value that controls how often the chatbot should try and change topic or approach based on previous tokens used. The value can be between -2 to 2, with -2 being never likely and 2 being very likely. For this app, let's add the following:
    presence_penalty = -1.5

Similar to Presence Penalty is the _'frequency_penalty'_ parameter.
_'Frequence Penalty'_ is a value that controls how often the same tokens are used. The value can be between -2 and 2, with -2 telling the chabtot that you don't care about redundant tokens or would even prefer to use the same response verbiage over and over, and 2 being that you want variety in the verbiage you want it to respond with. We want our responses to be pretty consistent and our app isn't meant for creative purposes, so let's add the following:
    frequency_penalty = -1.5

Now let's run our chat again and see the result. To see the effect of our most recent changes, try running it a few times. Do the responses seem consistent? Great! If not, try messing with the values for some of the parameters to aid it in getting the values we are looking for.

Check [here](https://platform.openai.com/docs/api-reference/chat/create) for more information on additional optional parameters you can include in your requests.

Now we have a chatbot that is able to remember some information we relay to it and take that into account to answer our prompt with a little added customization that helps the bot decide in what way it should form that response. 

In the next lab, we'll continue this app and extend our functionality even further to allow our bot to be able to run behavior on our behalf using _'tools'_ using _'function calling'_.