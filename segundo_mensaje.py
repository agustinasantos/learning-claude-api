from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

mensaje = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Hi Claude, tell me a joke about sisterhood"}

    ]
)

print(mensaje.content[0].text)


