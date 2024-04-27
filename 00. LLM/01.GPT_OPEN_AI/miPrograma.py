import pandas as pd
import os
from dotenv import load_dotenv
import openai
import spacy

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
print(api_key)

openai.api_key=api_key

modelo="text-davinci-002"
prompt="Cual es el himno de Venezuela"


respuesta=openai.Completion.create(engine=modelo,prompt=prompt, n=1,  max_tokens=100)

texto_generado=respuesta.choices[0].text.strip()
#print(texto_generado)

"""
for idx, opcion in enumerate(respuesta.choices):
    texto_generado=opcion.text.strip()
    print(  f"Respuesta {idx + 1} : {texto_generado}\n"       )
"""

print("***")

modelo_spacy=spacy.load("es_core_news_md")

analisis=modelo_spacy(texto_generado)
"""
for token in analisis:
    print(token.text,"->",token.pos_)
"""
print(analisis)
print("_____________________________________")


for ent in analisis.ents:
    print(ent.text,"->",ent.label_)

