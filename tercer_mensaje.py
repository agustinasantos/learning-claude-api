def translate(dog, french):
  response = client.messages.create(
      model="claude-3-opus-20240229",
      max_tokens=1000,
      messages=[
          {"role": "user", "content": f"Translate the word {word} into {language}. Only respond with the translated word, nothing else"}
      ]
  )
  return response.content[0].text
