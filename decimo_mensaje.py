from dotenv import load_dotenv
load_dotenv() 

import anthropic

client = anthropic.Anthropic()


conversation_history = []

system_prompt = """You are an specialized GTM (Go-to-Market) assistant for B2B, fintech and Web3 companies. Your role is to help a GTM Engineer to design outbound, lifecycle and AI Automation workflows.

Rules:
- You always answer in english.
- Respond brief and directly: 3-4 sentences per answer max. 
- If you need more info in order to answer well, make ONE clarifying question.
- Don't use bullet points unless strictly necessary."""


total_input_tokens = 0
total_output_tokens = 0
turn_number = 0

print("=" * 60)
print("  GTM Chatbot — write 'quit' to exit")
print("=" * 60)
print()


while True:
   
    user_input = input("User: ")
    
    if user_input.lower().strip() == "quit":
        print("\n" + "=" * 60)
        print(f"  Finished conversation after of {turn_number} turns.")
        print(f"  Total tokens consumed: {total_input_tokens} input / {total_output_tokens} output")
 
        cost = (total_input_tokens / 1_000_000) * 0.25 + (total_output_tokens / 1_000_000) * 1.25
        print(f"  Estimated cost of this session: ${cost:.6f} USD")
        print("=" * 60)
        break

    turn_number += 1

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

 
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        system=system_prompt,
        messages=conversation_history,
        max_tokens=500
    )

    assistant_response = response.content[0].text
    
    print(f"\nAssistant: {assistant_response}\n")
    
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    total_input_tokens += input_tokens
    total_output_tokens += output_tokens
    
    print(f"  [Turn {turn_number}] Input: {input_tokens} tokens | Output: {output_tokens} tokens")
    print(f"  [Acumulated] Input: {total_input_tokens} | Output: {total_output_tokens}")
    print()


    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })

