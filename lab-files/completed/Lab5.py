from openai import OpenAI
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('chat_history.db')
c = conn.cursor()

# Create a table to store messages
c.execute('''CREATE TABLE IF NOT EXISTS history (role TEXT, content TEXT)''')
conn.commit()

def main():
  client = OpenAI(api_key="")
  messages = [        
    {"role": "system", "content": "You are a helpful chatbot that responds to prompts politely."}
  ]

  while True:
    userInput = input("You: ")
    messages = update_history(messages, "user", userInput)
    response = call_openAI(client, messages)
    messages = update_history(messages, "assistant", response)
    print("AI: ", response)

def call_openAI(client, messages):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages= messages,
    temperature = 0.5
  )
  return response.choices[0].message.content

def update_history(messages, role, message):
  messages.append({"role": role, "content": message})
  return messages

def save_message(role, content):
  c.execute("INSERT INTO history (role, content) VALUES (?, ?)", (role, content))
  conn.commit()

def load_history():
  c.execute("SELECT role, content FROM history")
  return c.fetchall()
    
if __name__ == "__main__":
  main()