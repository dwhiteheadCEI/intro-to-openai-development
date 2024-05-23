# Lab 3: OpenAI Actions
In this lab we'll continue where we left off in _'Lab 2: Using the API'_. If you have not completed Lab 2, its recommended to complete it before continuing. This lab will cover the optional _'tools'_ parameter in the OpenAI chat completion API call to help us leverage some additional functionality for our Bakery Chatbot app. 

## Prerequisites
* An openAI account with credits available
* Basic knowledge of programming in Python
* [VSCode installed](https://code.visualstudio.com/download)

## Running our App
In the last lab, we created a bakery chatbot that is able to communicate with a little more focus on our use-case. Still, this is not a real application we can use for our intended purpose. Now that we understand the basics, let's build out our app to start behaving in a way thats a lot more user friendly. Navigate to 'Lab3.py' and run the application.

Our new app runs until closed, and data is streamed to and from the chatbot to the terminal, much closer to what we expect a chatbot to behave like.

Now that we have a real application that we can use to communicate with our bot, we are noticing a problem. All of our receipt data is hardcoded. What we'd like is to retrieve data from a source and use that data to answer our prompts whenever appropriate. One way to do that with OpenAI is with _'function calling'_ via the _'tools'_ parameter.

## Adding our First Tool
Be sure to check out the official documentation [here](https://platform.openai.com/docs/guides/function-calling)

Let's create a new tool that retrieves a file from our 'documents' folder. 
Add these parameters to the _'client.chat.completions.create'_ function call:
    tools=[
      {
        "type": "function",
        "function": {
          "name": "get_latest_receipt",
          "description": "Get the most recent receipt for a supply purchase. Information stored in the receipt includes total cost and individual costs per item.",
        }
      }
    ],
    tool_choice="auto"

The _'tools'_ parameter holds all of our extended functionality we want OpenAI to know about. We give it a name of a function as well as a description of when to use it. Setting the _'tool choice'_ parameter to 'auto' in this case is telling OpenAI that we want it to decide on its own when a function is relevant to answer a question.

Next, we'll have to define the actual function code we want to run. Paste this function at the top level:
    def get_latest_receipt():
    with open("../documents/bakeryReceipt.txt") as file:
        data = file.read()
    return data

If you try to run it at this point, you may notice that it runs as before, but whenever asked about receipts or expenses, it tends to return nothing at all. Don't worry, that's because it has found the use case for our tool based off of our description! If we look at the full response, we'll see that all tool calls will be placed in their own return value that we will need to check separately. 

Replace this line:
    return response.choices[0].message.content

With this:
    if(response.choices[0].finish_reason == "tool_calls"):
        if(response.choices[0].message.tool_calls[0].function.name == "get_latest_receipt"):
            return "Sure, here is your latest receipt: " + get_latest_receipt()
    else:
        return response.choices[0].message.content


## Extension 
As our tools grow in complexity, we can introduce further and further calls to OpenAI to help us in generating the appropriate context data. For instance, we could call our chat completion endpoint with a set of available tools, then if our response shows tools used we can run those tools, add the data from those tools to another chat completion prompt and call OpenAI again.

This can quickly grow in complexity and cost, and so it's important to remember that all these tools amount to is a string that we send the API. Any tool we create, or advanced library we use is ultimately just going to append something to our text. For that reason, it's important to evaluate early on which tools are actually necessary and what can just be introduced into the prompt manually. 