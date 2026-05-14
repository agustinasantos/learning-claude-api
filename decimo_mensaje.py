from dotenv import load_dotenv
load_dotenv() 

import anthropic

client = anthropic.Anthropic()


conversation_history = []

system_prompt = """Sos un asistente especializado en GTM (Go-to-Market) 
para empresas B2B SaaS, fintech y Web3. Tu rol es ayudar a un GTM 
Engineer a diseñar workflows de outbound, lifecycle, y AI automation.

Reglas:
- Respondés siempre en español rioplatense (vos, tenés, etc.).
- Sé breve y directo: máximo 3-4 oraciones por respuesta.
- Si necesitás más info para responder bien, hacé UNA pregunta clarificadora.
- No uses bullet points a menos que sea estrictamente necesario."""


total_input_tokens = 0
total_output_tokens = 0
turn_number = 0

print("=" * 60)
print("  GTM Chatbot — escribí 'quit' para salir")
print("=" * 60)
print()


while True:
   
    user_input = input("User: ")
    
    if user_input.lower().strip() == "quit":
        print("\n" + "=" * 60)
        print(f"  Conversación terminada después de {turn_number} turnos.")
        print(f"  Total tokens consumidos: {total_input_tokens} input / {total_output_tokens} output")
 
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
    
    print(f"  [Turn {turn_number}] Input: {input_tokens} tokens | Output: {output_tokens} tokens")
    print(f"  [Acumulated] Input: {total_input_tokens} | Output: {total_output_tokens}")
    print()


    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })

