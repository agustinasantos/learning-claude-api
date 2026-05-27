from dotenv import load_dotenv
from anthropic import Anthropic

#load environment variable
load_dotenv()

client = Anthropic()

def measure_streaming_ttft():
    start_time = time.time()

    stream = client.messages.create(
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": "Write me a long essay explaining the history of the American Revolution",
            }
        ],
        temperature=0,
        model="claude-3-haiku-20240307",
        stream=True
    )
    have_received_first_token = False
    for event in stream:
        if event.type == "content_block_delta":
            if not have_received_first_token:
                ttft = time.time() - start_time
                have_received_first_token = True
            print(event.delta.text, flush=True, end="")
        elif event.type == "message_delta":
            output_tokens = event.usage.output_tokens
            total_time = time.time() - start_time

    print(f"\nTime to receive first token: {ttft:.3f} seconds", flush=True)
    print(f"Time to recieve complete response: {total_time:.3f} seconds", flush=True)
    print(f"Total tokens generated: {output_tokens}", flush=True)
    
