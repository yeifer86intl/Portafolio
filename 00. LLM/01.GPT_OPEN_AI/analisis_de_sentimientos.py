import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key=api_key


def analizar_sentimientos(texto):
    prompt=f"Por favor, analiza el sentimiento predominante en el texto indicando si es positivo o negativo y explica el porque de la decision: '{texto}', El sentimiento es: "
    respuesta=openai.Completion.create(engine="text-davinci-002", prompt=prompt, n=1, max_tokens=100, temperature=0.5)
    return (respuesta.choices[0].text.strip())


texto_analizar=input("ingresa un texto: ")

sentimiento=analizar_sentimientos(texto_analizar)

print(sentimiento)