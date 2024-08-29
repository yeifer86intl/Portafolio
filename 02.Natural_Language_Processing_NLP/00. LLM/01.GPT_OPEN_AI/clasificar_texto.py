import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key=api_key


def clasificar_texto(texto):

    categorias=["arte"
    ,"ciencia"
    ,"deportes"
    ,"economia"
    ,"educacion"
    ,"entretenimiento"
    ,"medio ambiente"
    ,"politica "
    ,"salud"
    ,"tecnologia"
                    ]

    prompt = f"Por favor, clasifica el sentimiento texto solamente en las categorias que estan en la lista categorias: '{texto}', en una de las categorias: {','.join(categorias)}. La categoria es:  "

    respuesta = openai.Completion.create(engine="text-davinci-002", prompt=prompt, n=1, max_tokens=50, temperature=0.5)
    return (respuesta.choices[0].text.strip())


texto=input("ingrese un texto: ")

clasificacion=clasificar_texto(texto)

print(clasificacion)