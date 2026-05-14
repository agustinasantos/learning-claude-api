from anthropic import Anthropic
from dotenv import load_dotenv

# Carga la API Key desde el archivo .env
load_dotenv()

# Crea el cliente (encuentra la key automáticamente)
client = Anthropic()

# Envía un mensaje a Claude
mensaje = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Hola Claude, cuentame un chiste sobre hermanos"}

    ]
)

# Imprime la respuesta
print(mensaje.content[0].text)


