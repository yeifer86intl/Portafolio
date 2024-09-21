import json
import os
import time
import numpy as np
import redis
import settings
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import ResNet50

# Conectar a Redis
try:
    db = redis.StrictRedis(host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID)
    print(f"Conexión a Redis establecida en {settings.REDIS_IP}:{settings.REDIS_PORT}")
except Exception as e:
    print(f"Error al conectar a Redis: {e}")
    raise e

# Cargar el modelo preentrenado ResNet50
try:
    model = ResNet50(include_top=True, weights="imagenet")
    print("Modelo ResNet50 cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    raise e

def predict(image_name):
    """
    Cargar imagen y ejecutar el modelo ML para obtener predicciones.

    Parámetros
    ----------
    image_name : str
        Nombre del archivo de imagen.

    Retorna
    -------
    class_name, pred_probability : tuple(str, float)
        Clase predicha por el modelo y el puntaje de confianza.
    """
    try:
        # Cargar imagen desde la carpeta de cargas
        img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
        img = image.load_img(img_path, target_size=(224, 224))
    except FileNotFoundError:
        print(f"Error: {image_name} no encontrado en {settings.UPLOAD_FOLDER}")
        return None, None

    # Preprocesar la imagen
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Obtener predicciones
    preds = model.predict(img_array)
    decoded_preds = decode_predictions(preds, top=1)[0][0]

    # Extraer clase y probabilidad
    class_name = decoded_preds[1]
    pred_probability = round(float(decoded_preds[2]), 4)

    print("Predicción realizada:")
    print(f"Clase: {class_name}, Probabilidad: {pred_probability}")

    return class_name, pred_probability

def classify_process():
    """
    Bucle indefinido que pide a Redis nuevos trabajos.
    """
    while True:
        try:
            # Tomar un nuevo trabajo de Redis
            job = db.brpop(settings.REDIS_QUEUE)
            if job:
                job_data = json.loads(job[1].decode("utf-8"))

                # Obtener el ID del trabajo original y el nombre de la imagen
                job_id = job_data["id"]
                image_name = job_data["image_name"]

                print(f"Procesando imagen: {image_name} (Job ID: {job_id})")

                # Ejecutar el modelo de ML para obtener predicciones
                class_name, score = predict(image_name)

                if class_name is not None:
                    # Preparar los resultados
                    output = {
                        "prediction": class_name,
                        "score": score,
                    }

                    # Guardar los resultados en Redis usando el ID original del trabajo
                    db.set(job_id, json.dumps(output))
                    print(f"Resultados guardados en Redis para Job ID: {job_id}")
                else:
                    print(f"No se pudo procesar la imagen: {image_name}")

            # Dormir por un pequeño intervalo
            time.sleep(settings.SERVER_SLEEP)
        
        except Exception as e:
            print(f"Error en classify_process: {e}")
            time.sleep(settings.SERVER_SLEEP)  # Evitar que el bucle entre en un ciclo rápido en caso de error

if __name__ == "__main__":
    print("Lanzando servicio de ML...")
    classify_process()
