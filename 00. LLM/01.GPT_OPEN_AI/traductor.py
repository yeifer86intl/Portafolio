import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key=api_key


def traducir_texto(texto , idioma):

    prompt = f"Traduce el texto '{texto}' al idioma {idioma}."

    respuesta = openai.Completion.create(engine="text-davinci-002", prompt=prompt, n=1, temperature=0.5)
    return (respuesta.choices[0].text.strip())


mi_texto=input("ingrese un texto: ")
mi_idioma=input("ingrese idioma: ")

traduccion=traducir_texto(mi_texto,mi_idioma)

print(traduccion)