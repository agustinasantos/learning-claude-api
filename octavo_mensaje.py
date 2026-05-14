from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

response = client.messages.create(
    messages=[
        {
            "role": "user",
            "content": "Write me an essay about macaws and clay licks in the Amazon",
        }
    ],
    model="claude-haiku-4-5-20251001",
    max_tokens=800,
    temperature=0,
)
print("We have a response back!")
print("========================")
print(response.content[0].text)
