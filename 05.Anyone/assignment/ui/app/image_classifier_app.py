from typing import Optional

import requests
import streamlit as st
from app.settings import API_BASE_URL
from PIL import Image


def login(username: str, password: str) -> Optional[str]:
    """This function calls the login endpoint of the API to authenticate the user
    and get a token.

    Args:
        username (str): email of the user
        password (str): password of the user

    Returns:
        Optional[str]: token if login is successful, None otherwise
    """
    # Construye la URL del endpoint de login
    url = f"{API_BASE_URL}/login"
    
    # Configura los headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Prepara los datos del payload
    data = {
        "grant_type": "",  # Tipo de autorización
        "username": username,      # Nombre de usuario (email)
        "password": password,      # Contraseña del usuario
        "scope": "",               # Ámbito (opcional)
        "client_id": "",           # ID del cliente (si lo requiere la API)
        "client_secret": ""        # Secreto del cliente (si lo requiere la API)
    }

    # Realiza la solicitud POST a la API
    response = requests.post(url, headers=headers, data=data)

    # Verifica si la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        # Extrae el token de la respuesta JSON
        token = response.json().get("access_token")
        return token
    else:
        # Si el login falla, retorna None
        return None


def predict(token: str, uploaded_file) -> Optional[requests.Response]:
    """This function calls the predict endpoint of the API to classify the uploaded
    image.

    Args:
        token (str): token to authenticate the user
        uploaded_file: file to classify (file-like object)

    Returns:
        Optional[requests.Response]: response from the API or None if the request fails
    """
    # Construir la URL del endpoint
    url = f"{API_BASE_URL}/model/predict"
    
    # Agregar el token a los headers
    headers = {
        "Authorization": f"Bearer {token}"
     
    }
    
    # Preparar el archivo para el formulario
    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue())
    }

    try:
        # Enviar la solicitud POST
        response = requests.post(url, headers=headers, files=files)
        #response.raise_for_status()  # Verificar si hubo algún error HTTP
        return response
    except requests.RequestException as e:
        print(f"Error during prediction: {e}")
        return None

def send_feedback(
    token: str, feedback: str, score: float, prediction: str, image_file_name: str
) -> requests.Response:
    """This function calls the feedback endpoint of the API to send feedback about
    the classification.

    Args:
        token (str): token to authenticate the user
        feedback (str): string with feedback
        score (float): confidence score of the prediction
        prediction (str): predicted class
        image_file_name (str): name of the image file

    Returns:
        requests.Response: response from the API
    """
    # 1. Create a dictionary with the feedback data
    data = {
        "feedback": feedback,
        "score": score,
        "predicted_class": prediction,
        "image_file_name": image_file_name
    }
    
    # 2. Set up the request headers with the token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 3. Construct the URL for the feedback endpoint
    url = f"{API_BASE_URL}/feedback"
    
    # 4. Make a POST request to the feedback endpoint
    response = requests.post(url, json=data, headers=headers)
    
    # 5. Return the response
    return response











# Interfaz de usuario
st.set_page_config(page_title="Image Classifier", page_icon="📷")
st.markdown(
    "<h1 style='text-align: center; color: #4B89DC;'>Image Classifier</h1>",
    unsafe_allow_html=True,
)

# Formulario de login
if "token" not in st.session_state:
    st.markdown("## Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        token = login(username, password)
        if token:
            st.session_state.token = token
            st.success("Login successful!")
        else:
            st.error("Login failed. Please check your credentials.")
else:
    st.success("You are logged in!")


if "token" in st.session_state:
    token = st.session_state.token

    # Cargar imagen
    uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    print(type(uploaded_file))

    # Mostrar imagen escalada si se ha cargado
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen subida", width=300)

    if "classification_done" not in st.session_state:
        st.session_state.classification_done = False

    # Botón de clasificación
    if st.button("Classify"):
        if uploaded_file is not None:
            response = predict(token, uploaded_file)
            if response.status_code == 200:
                result = response.json()
                st.write(f"**Prediction:** {result['prediction']}")
                st.write(f"**Score:** {result['score']}")
                st.session_state.classification_done = True
                st.session_state.result = result
            else:
                st.error("Error classifying image. Please try again.")
        else:
            st.warning("Please upload an image before classifying.")

    # Mostrar campo de feedback solo si se ha clasificado la imagen
    if st.session_state.classification_done:
        st.markdown("## Feedback")
        feedback = st.text_area("If the prediction was wrong, please provide feedback.")
        if st.button("Send Feedback"):
            if feedback:
                token = st.session_state.token
                result = st.session_state.result
                score = result["score"]
                prediction = result["prediction"]
                image_file_name = result.get("image_file_name", "uploaded_image")
                response = send_feedback(
                    token, feedback, score, prediction, image_file_name
                )
                if response.status_code == 201:
                    st.success("Thanks for your feedback!")
                else:
                    st.error("Error sending feedback. Please try again.")
            else:
                st.warning("Please provide feedback before sending.")
                st.warning("Please provide feedback before sending.")

    # Pie de página
    st.markdown("<hr style='border:2px solid #4B89DC;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #4B89DC;'>2024 Image Classifier App</p>",
        unsafe_allow_html=True,
    )
