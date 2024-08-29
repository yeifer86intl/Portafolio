import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key=api_key

def crear_contenido(tema, tokens, temperatura, modelo="text-davinci-002"):
    prompt=f"Por favor, escribe un articulo corto sobre el tema: {tema}\n\n"
    respuesta=openai.Completion.create(engine=modelo, prompt=prompt, n=1, max_tokens=tokens, temperature=temperatura)
    return (respuesta.choices[0].text.strip())

def resumir_text(tema, tokens, temperatura, modelo="text-davinci-002"):
    prompt=f"Por favor, resume el siguiente texto en español: {tema}\n\n"
    respuesta=openai.Completion.create(engine=modelo, prompt=prompt, n=1, max_tokens=tokens, temperature=temperatura)
    return (respuesta.choices[0].text.strip())


#tema=input("Elije un tema: ")
#tokens=int(input("Cuantos tokens maximos tendran tu articulo: "))
#temperatura=int(input("Del 1 al 10 que tan creativo quieres que seas tu articulo?: "))/10


#articulo_creado=crear_contenido(tema,  tokens, temperatura)



original=input("Pega ")
tokens=int(input("Cuantos tokens maximos tendran tu articulo: "))
temperatura=int(input("Del 1 al 10 que tan creativo quieres que seas tu articulo?: "))/10


articulo_resumido=resumir_text(original,  tokens, temperatura)

print(articulo_resumido)



