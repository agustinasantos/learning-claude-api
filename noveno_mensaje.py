from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

stream = client.messages.create(
    messages=[
        {
            "role": "user",
            "content": "Write me a 3 word sentence, without a preamble.  Just give me 3 words",
        }
    ],
    model="claude-haiku-4-5-20251001",
    max_tokens=100,
    temperature=0,
    stream=True,
)

for event in stream:
    if event.type == "content_block_delta":
        print(event.delta.text, end="", flush=True)

print() 
