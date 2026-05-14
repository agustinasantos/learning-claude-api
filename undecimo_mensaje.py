# Combine Lesson 2 (history) + Lesson 5 (streaming)

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
system_prompt = """You are a specialized assistant on GTM Engineer for B2B SaaS, fintech and Web3 companies.

Rules:
- Always answer in english.
- Be brief and directly:3-4 sentences max per response.
- If you need more info to answer correctly,make ONE clarified question."""

# List where we are going to store the convo history
conversation_history = []
# ============================================================
# Header visual
# ============================================================

print("=" * 60)
print("  GTM Chatbot with streaming — write 'quit' to exit")
print("=" * 60)
print()

# ============================================================
# Loop: infinite Chat until user writes ‘quit’ 
# ============================================================

while True:
    # 1. Request user’s input
    user_input = input("User: ")
    
    # 2. Exit if the user writes 'quit'
    if user_input.lower().strip() == "quit":
        print("\nConversacion terminada. Chau!")
        break

    # 3. Add the message to the conversation history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    # 4. Call Claude WITH STREAMING activated
    stream = client.messages.create(
        model="claude-haiku-4-5-20251001",
        system=system_prompt,
        messages=conversation_history,
        max_tokens=500,
        stream=True  # ← acá está la magia del streaming
    )

    # 5. Print the prefix "Assistant:" without  jumping line
    print("\nAssistant: ", end="", flush=True)

    # 6. Iteration about the stream events and keep showing 
    assistant_response = ""
    for event in stream:
        if event.type == "content_block_delta":
            text_chunk = event.delta.text
            print(text_chunk, end="", flush=True)  # mostrar
            assistant_response += text_chunk        # acumular

    # 7. Final line jump
    print("\n")

    # 8. Storage the complete Claude answer in the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })
assistant_response = ""
for event in stream:
    if event.type == "content_block_delta":
        text_chunk = event.delta.text
        print(text_chunk, end="", flush=True)
        assistant_response += text_chunk

