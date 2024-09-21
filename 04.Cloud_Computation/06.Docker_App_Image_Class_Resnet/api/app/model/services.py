import json
import time
from uuid import uuid4

import redis

from .. import settings

# Conexión a Redis usando las configuraciones en settings.py
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID
)

async def model_predict(image_name):
    print(f"Processing image {image_name}...")
    """
    Recibe un nombre de imagen y envía el trabajo a Redis.
    Loop hasta obtener la respuesta del servicio ML.

    Parameters
    ----------
    image_name : str
        Nombre de la imagen cargada por el usuario.

    Returns
    -------
    prediction, score : tuple(str, float)
        Predicción del modelo y la confianza en la predicción.
    """
    prediction = None
    score = None

    # Asignamos un ID único para este trabajo
    job_id = str(uuid4())

    # Creamos un diccionario con los datos del trabajo
    job_data = {"id": job_id, "image_name": image_name}

    # Enviamos el trabajo a la cola en Redis
    db.lpush(settings.REDIS_QUEUE, json.dumps(job_data))

    # Loop hasta recibir la respuesta de nuestro modelo ML
    while True:
        # Intentamos obtener las predicciones del modelo usando el job_id
        output = db.get(job_id)

        # Si obtenemos un resultado, procesamos la respuesta
        if output is not None:
            output = json.loads(output.decode("utf-8"))
            prediction = output["prediction"]
            score = output["score"]

            db.delete(job_id)
            break

        # Esperamos un poco antes de verificar nuevamente
        time.sleep(settings.API_SLEEP)

    return prediction, score
























'''
import json
import time
from uuid import uuid4

import redis

from .. import settings

# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = None


async def model_predict(image_name):
    print(f"Processing image {image_name}...")
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    prediction = None
    score = None

    # Assign an unique ID for this job and add it to the queue.
    # We need to assing this ID because we must be able to keep track
    # of this particular job across all the services
    # TODO
    job_id = None

    # Create a dict with the job data we will send through Redis having the
    # following shape:
    # {
    #    "id": str,
    #    "image_name": str,
    # }
    # TODO
    job_data = {"id": None, "image_name": None}

    # Send the job to the model service using Redis
    # Hint: Using Redis `lpush()` function should be enough to accomplish this.
    # TODO

    # Loop until we received the response from our ML model
    while True:
        # Attempt to get model predictions using job_id
        # Hint: Investigate how can we get a value using a key from Redis
        # TODO
        output = None

        # Check if the text was correctly processed by our ML model
        # Don't modify the code below, it should work as expected
        if output is not None:
            output = json.loads(output.decode("utf-8"))
            prediction = output["prediction"]
            score = output["score"]

            db.delete(job_id)
            break

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return prediction, score
'''
