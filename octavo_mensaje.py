from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

stream = client.messages.create(
    messages=[
        {
            "role": "user",
            "content": "How do large language models work?",
        }
    ],
    model="claude-haiku-4-5-20251001",
    max_tokens=1000,
    temperature=0,
    stream=True,
)
for event in stream:
    if event.type == "message_start":
        input_tokens = event.message.usage.input_tokens
        print("MESSAGE START EVENT", flush=True)
        print(f"Input tokens used: {input_tokens}", flush=True)
        print("========================")
    elif event.type == "content_block_delta":
        print(event.delta.text, flush=True, end="")
    elif event.type == "message_delta":
        output_tokens = event.usage.output_tokens
        print("\n========================", flush=True)
        print("MESSAGE DELTA EVENT", flush=True)
        print(f"Output tokens used: {output_tokens}", flush=True)
