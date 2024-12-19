# from fastapi import FastAPI, HTTPException
# import httpx

# app = FastAPI()

# # URL de la API de chistes
# JOKE_API_URL = "https://v2.jokeapi.dev/joke/Programming"

# @app.get("/joke")
# async def get_joke():
#     # Obtener chiste de la API
#     async with httpx.AsyncClient() as client:
#         response = await client.get(JOKE_API_URL)
    
#     if response.status_code != 200:
#         raise HTTPException(status_code=500, detail="Error al obtener el chiste.")
    
#     joke_data = response.json()
    
#     if joke_data["type"] == "twopart":
#         # Si es un chiste de dos partes
#         setup = joke_data["setup"]
#         delivery = joke_data["delivery"]
#         return {
#             "chiste": {
#                 "setup": setup,
#                 "delivery": delivery,
#             },
#             "tipo": "twopart"
#         }
#     elif joke_data["type"] == "single":
#         # Si es un chiste de una sola parte
#         joke = joke_data["joke"]
#         return {
#             "chiste": joke,
#             "tipo": "single"
#         }
#     else:
#         raise HTTPException(status_code=500, detail="Tipo de chiste no soportado.")

from fastapi import FastAPI, HTTPException
import httpx
from googletrans import Translator

app = FastAPI()

# URL de la API de chistes
JOKE_API_URL = "https://v2.jokeapi.dev/joke/Programming"

# Inicializar el traductor
translator = Translator()

@app.get("/joke")
async def get_joke():
    # Obtener chiste de la API
    async with httpx.AsyncClient() as client:
        response = await client.get(JOKE_API_URL)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al obtener el chiste.")
    
    joke_data = response.json()
    
    # Traducir el chiste
    def translate(text):
        return translator.translate(text, src='en', dest='es').text
    
    if joke_data["type"] == "twopart":
        # Si es un chiste de dos partes
        setup = translate(joke_data["setup"])
        delivery = translate(joke_data["delivery"])
        return {
            "chiste": {
                "setup": setup,
                "delivery": delivery,
            },
            "tipo": "twopart"
        }
    elif joke_data["type"] == "single":
        # Si es un chiste de una sola parte
        joke = translate(joke_data["joke"])
        return {
            "chiste": joke,
            "tipo": "single"
        }
    else:
        raise HTTPException(status_code=500, detail="Tipo de chiste no soportado.")
