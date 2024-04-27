import os
import openai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key=api_key



#openai.api_key=os.getenv('OPENAI_API_KEY')

user_prompt=input("write your prompt: ")


response=openai.Image.create(prompt=user_prompt, n=1, size="1024x1024")

image_url=response["data"][0]["url"]

print(image_url)

