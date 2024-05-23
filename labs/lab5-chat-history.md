# Lab 5: Chat History
In this lab, we'll go over one of the most common problems to solve when creating any OpenAI-based solution, chat history. We'll discuss the issue as well as potential strategies and implement a basic chat history that can be run locally and persist between sessions.

## Prerequisites
* An openAI account with credits available
* Basic knowledge of programming in Python
* [VSCode installed](https://code.visualstudio.com/download)

## A Brief Summation
When working with different LLM-based solutions, a common issue to run into is managing chat history. Chat history helps our chatbot understand context clues and helps our conversations feel much more organic. If your intended solution requires a back-and-forth dialogue or multi-step question answering, you'll have to adapt some form of chat history management.

## Running our App
Let's run our app:
    cd lab-files
    py lab5.py

## Basic Chat History
Starting with the basics is always easiest, right?

Remember in lab2 when we were using the 'messages' parameter to send our prompt? Well, we lets take this a step further. The chat-completion API is always going to respond to the last 'user' message posted and will use the older 'user' and 'assistant' messages to help it understand the context in which it is responding.

As an example, try replacing your 'messages' parameter with this:
    messages = [
        {"role": "system", "content": "You are a helpful chatbot that responds to questions clearly and politely."},
        {"role": "user", "content": "Who was the first president of the United States?"}, 
        {"role": "assistant", "content": "The first president of the United States was George Washington"},
        {"role": "user", "content": "Who was the president who came after him?"}
    ]

Note how it answers the final prompt, but relies on information from previous messages to fully understand the question. 

This is a great step for setting context for the bot, but still, this is hardcoded memory and not quite what we're looking for. Let's set our 'messages' variable back to the following:
    messages = [        
        {"role": "system", "content": "You are a helpful chatbot that responds to prompts clearly and politely."}
    ]

Next, let's add a new function that will append all of our prompts to our chat history so that we can reuse it:
    def update_history(messages, role, message):
        messages.append({"role": role, "content": message})
        return messages

Now, we'll update our main function. Let's add this line before the call to openAI:
    messages = update_history(messages, "user", userInput)
Then, make sure to add this line after the openAI response is returned so that each response is saved as well:
    messages = update_history(messages, "assistant", response)

Let's run our app again and type multiple prompts. Test out it's accuracy in recalling previous messages. Be sure to ask questions that the chatbot would only be able to answer with the added context.

While in some certain circumstances this may be enough, it comes with some issues:

### Token Usage: 
As you may have been able to guess, our requests are going to get larger and larger, thus taking longer and longer to answer. Eventually, this will become such a large request that we will reach our token limit. 

A common, clever solution to this problem is to introduce an extra step where you take all prompts and responses and reserve a "chunk" of a certain token size dedicated to serving as a summary of the chat history so far. By doing this, you circumvent the issue of ever reaching a maximum token limit. This solution comes at the cost of potentially losing data everytime a summary is made and, depending on your summarization method, increased runtime/cost.
Another common solution to the issue is to truncate the chat history either after a certain amount of messages has passed, after a certain token size is reached, or after a certain timeframe. This solution also suffers from data loss, but in a much more predictable way that may be more manageable depending on the app. 

### Prompt Bloating 
With extensive chat history comes an extensive prompt, providing the opportunity for our chatbot to become distracted away from our prompt's initial intent.

### User Management
Our chatbot currently has no idea how much time has passed between messages or if it is even speaking to the same user. Proper authentication can be set up to help with the later, but it's also important to try and address the issue of non-expiry history as it pertains to your use-case. 

For instance, imagine a scenario where you copy and paste some data you want the chatbot to analyze, then create a prompt asking to find the average of one of the fields. Then, after stepping away from your system for the weekend you return, upload some new numbers and ask the same question. This time, the average is way off because it still thinks you are want it to include all of the data from the previous prompts, bummer!

There are ways to mitigate all of these issues but, no matter what, there is going to be some form of a cost -- be it speed, efficiency, accuracy, or monetary. It's important to decide on the metrics that are most important for the app and plan your implementation of chat history accordingly. 

Another issue presented is that our chat history currently has no way of persisting through sessions, let's take a look at solving that issue now.

## Persistent Chat Storage
There are a number of valid solutions to create and maintain chat history storage across sessions and ultimately it will depend on your use case to identify what fits the criteria of your application. 

Here's some popular choices: 
1. Local File Storage: Really only useful for personal applications and testing, but easy to implement and good for prototypes and PoCs.
2. SQL Database: Integrate SQL database using SQLite, PostgreSQL, MySQL. Allows for much cleaner data management but may require more additional configuration as you add user authentication and scale an application.
3. Azure CosmosDB: Highly scalable, easy to use once it is set up, and great at handling large data sets but costly.
4. NoSQL DB Options: One such example being MongoDB, good for unstructured data and scalable

## Additional Options

The topic of chat history is currently very prevalent in ai-based solutions and as such, there's a lot of great documentation to look at for further development:
[Semantic Kernel chat history and memory](https://learn.microsoft.com/en-us/semantic-kernel/overview/?tabs=Csharp)
[Langchain message history](https://python.langchain.com/v0.1/docs/expression_language/how_to/message_history/)