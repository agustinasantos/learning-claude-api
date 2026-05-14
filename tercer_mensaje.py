from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

def translate(word, language):
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"Translate the word {word} into {language}. Only respond with the translated word, nothing else"}
        ]
    )
    return response.content[0].text

result = translate("dog", "french")
print(result)
