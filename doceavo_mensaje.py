"""
======================================================================
 CHATBOT GTM con HISTORIAL — Ejemplo educativo
======================================================================
 Demuestra el concepto central de Lesson 2:
 "Claude no tiene memoria, vos le mandás el thread completo cada vez."

 Cómo correrlo:
 1. Instalar la librería: pip install anthropic
 2. Setear tu API key: export ANTHROPIC_API_KEY="tu_api_key_aca"
 3. Correr: python chatbot_gtm.py
======================================================================
"""
from dotenv import load_dotenv
load_dotenv()  # Lee tu archivo .env y carga las variables

import anthropic

# Inicializar el cliente. Toma la API key de la variable de entorno
# ANTHROPIC_API_KEY automáticamente.
client = anthropic.Anthropic()

# ----------------------------------------------------------------------
# 1. EL HISTORIAL DE CONVERSACIÓN
# ----------------------------------------------------------------------
# Esta lista vacía es el "thread completo" que vamos a ir construyendo.
# Cada elemento será un dict con "role" (user o assistant) y "content".
conversation_history = []

# ----------------------------------------------------------------------
# 2. EL SYSTEM PROMPT
# ----------------------------------------------------------------------
# Define la personalidad y el rol del bot. NO se manda dentro de
# "messages", se manda en el parámetro "system" aparte. Esto le indica
# a Claude su rol, sin contar como un "turno" de la conversación.
system_prompt = """Sos un asistente especializado en GTM (Go-to-Market) 
para empresas B2B SaaS, fintech y Web3. Tu rol es ayudar a un GTM 
Engineer a diseñar workflows de outbound, lifecycle, y AI automation.

Reglas:
- Respondés siempre en español rioplatense (vos, tenés, etc.).
- Sé breve y directo: máximo 3-4 oraciones por respuesta.
- Si necesitás más info para responder bien, hacé UNA pregunta clarificadora.
- No uses bullet points a menos que sea estrictamente necesario."""

# ----------------------------------------------------------------------
# 3. CONTADOR ACUMULADO DE TOKENS (para ver el costo crecer)
# ----------------------------------------------------------------------
total_input_tokens = 0
total_output_tokens = 0
turn_number = 0

print("=" * 60)
print("  GTM Chatbot — escribí 'quit' para salir")
print("=" * 60)
print()

# ----------------------------------------------------------------------
# 4. EL LOOP PRINCIPAL
# ----------------------------------------------------------------------
while True:
    # 4.1 — Pedir input al usuario
    user_input = input("User: ")
    
    # 4.2 — Salida limpia si el usuario escribe "quit"
    if user_input.lower().strip() == "quit":
        print("\n" + "=" * 60)
        print(f"  Conversación terminada después de {turn_number} turnos.")
        print(f"  Total tokens consumidos: {total_input_tokens} input / {total_output_tokens} output")
        # Costo aproximado para Haiku (al momento de escribir este script,
        # verificá precios actualizados en anthropic.com/pricing):
        # Input:  $0.25 / 1M tokens
        # Output: $1.25 / 1M tokens
        cost = (total_input_tokens / 1_000_000) * 0.25 + (total_output_tokens / 1_000_000) * 1.25
        print(f"  Costo estimado de esta sesión: ${cost:.6f} USD")
        print("=" * 60)
        break

    turn_number += 1

    # 4.3 — Agregar el mensaje del usuario al historial
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    # 4.4 — Llamar a Claude con el HISTORIAL COMPLETO
    # Notá: messages=conversation_history (toda la lista, no solo el último)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        system=system_prompt,
        messages=conversation_history,
        max_tokens=500
    )

    # 4.5 — Extraer el texto de la respuesta de Claude
    assistant_response = response.content[0].text
    
    # 4.6 — Imprimir la respuesta para el usuario
    print(f"\nAssistant: {assistant_response}\n")
    
    # 4.7 — Mostrar tokens consumidos en este turno (¡este es el truco
    # didáctico! Vas a ver cómo crecen los input tokens cada turno.)
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    total_input_tokens += input_tokens
    total_output_tokens += output_tokens
    
    print(f"  [Turno {turn_number}] Input: {input_tokens} tokens | Output: {output_tokens} tokens")
    print(f"  [Acumulado] Input: {total_input_tokens} | Output: {total_output_tokens}")
    print()

    # 4.8 — CRÍTICO: agregar la respuesta de Claude al historial.
    # Sin esto, en el próximo turno Claude no sabría qué respondió antes.
    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })

