from dotenv import load_dotenv
load_dotenv()  # Lee tu archivo .env y carga las variables

import anthropic


client = anthropic.Anthropic()

# ----------------------------------------------------------------------
# CONVERSATION HISTORY: this empty list is the "completed thread" that I'm creating. Every element will be a dict with "role" (user or assistant) and "content".
# ----------------------------------------------------------------------

conversation_history = []

system_prompt = """I'm a specialized assistant on GTM Engineer for B2B SaaS, fintech and Web3 companies. Your role is to help a GTM Engineer design workflows of outbound, lifecycle and AI automation. 

Rules:
- Always answer in English.
- Be briefly and directly: 3-4 sentences per answer. 
- If you need more info to answer correctly, make ONE clarifying question.
- Don't use bullet points unless it's strictly necessary."""

# ----------------------------------------------------------------------
# 3. NUMERO OF TOKENS (to see the cost increase)
# ----------------------------------------------------------------------
total_input_tokens = 0
total_output_tokens = 0
turn_number = 0

print("=" * 60)
print("  GTM Chatbot — escribí 'quit' para salir")
print("=" * 60)
print()

# ----------------------------------------------------------------------
# 4. MAIN LOOP
# ----------------------------------------------------------------------
while True:
   
    user_input = input("User: ")
    
    if user_input.lower().strip() == "quit":
        print("\n" + "=" * 60)
        print(f"  Conversación terminada después de {turn_number} turnos.")
        print(f"  Total tokens consumidos: {total_input_tokens} input / {total_output_tokens} output")
       # Approximate cost for Haiku (at the time of writing this script,
        # you need to check updated prices at anthropic.com/pricing):
        # Input: $0.25 / 1M tokens
        # Output: $1.25 / 1M tokens
        cost = (total_input_tokens / 1_000_000) * 0.25 + (total_output_tokens / 1_000_000) * 1.25
        print(f"  Costo estimado de esta sesión: ${cost:.6f} USD")
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
    
    print(f"  [Turno {turn_number}] Input: {input_tokens} tokens | Output: {output_tokens} tokens")
    print(f"  [Acumulado] Input: {total_input_tokens} | Output: {total_output_tokens}")
    print()


    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })

