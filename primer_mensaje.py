from anthropic import Anthropic
from dotenv import load_dotenv

# Upload the API Key from the .env file
load_dotenv()

# Create the client (finds the key automatically)
client = Anthropic()

# Send a message to Claude
mensaje = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Hi Claude, explain me what is Python in one sentence"}

    ]
)

# Print the response
print(mensaje.content[0].text)

