import time
import json
import requests
import streamlit as st
import openai

# Configurar API Key de OpenAI
OPENAI_API_KEY = "TU_OPENAI_API_KEY"  # ⚠️ Reemplaza con tu clave real

# URL de la API en AWS Lambda (RAG)
API_BASE_URL = "https://o4zgf7m5obg4x4kruerabsxg240vchpd.lambda-url.us-east-1.on.aws"

# ✅ Inicializar historial de chat en session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ✅ Respuestas predefinidas para saludos y despedidas
RESPUESTAS_CORTESIA = {
    "hola": "¡Hola! ¿En qué puedo ayudarte hoy? 😊",
    "hello": "Hello! How can I assist you? 🌍",
    "buenos días": "¡Buenos días! Espero que tengas un excelente día. 🌞",
    "buenas tardes": "¡Buenas tardes! ¿En qué puedo ayudarte?",
    "buenas noches": "¡Buenas noches! ¿Necesitas ayuda antes de descansar? 🌙",
    "adiós": "¡Hasta luego! Que tengas un buen día. 👋",
    "bye": "Goodbye! Take care! 👋",
    "chao": "¡Chao! Vuelve cuando quieras. 🚀",
    "gracias": "¡De nada! Siempre aquí para ayudar. 🤖",
    "thanks": "You're welcome! 😊"
}

# ✅ Función para verificar si es un saludo/despedida
def respuesta_cordial(query: str) -> str:
    query_lower = query.lower().strip()
    for key in RESPUESTAS_CORTESIA.keys():
        if key in query_lower:
            return RESPUESTAS_CORTESIA[key]
    return None  # No es un saludo ni despedida

# ✅ Función para consultar la API RAG
def rag_response(query: str) -> str:
    """Consulta la API RAG solo si OpenAI indica que es necesario."""
    rag_endpoint = f"{API_BASE_URL}/submit_query"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    input_query = {"query_text": query}

    try:
        response_rag = requests.post(rag_endpoint, json=input_query, headers=headers)

        if response_rag.status_code == 200:
            response_json = response_rag.json()
            return response_json.get("response_text", "No response text found.")
        else:
            return f"Error {response_rag.status_code}: {response_rag.text}"

    except requests.exceptions.RequestException as e:
        return f"Exception: {str(e)}"

# ✅ Función para efecto de escritura en la respuesta
def response_generator_dynamic(text: str):
    """Genera un texto con efecto de escritura en Streamlit."""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

# ✅ Decidir si se usa RAG o OpenAI
def should_use_rag(query: str) -> bool:
    """Pregunta a OpenAI si la consulta debe ser respondida con la API RAG."""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente que responde solo con información de la base de datos externa. Si la pregunta no tiene información en la base de datos, responde con 'Sí'."},
                {"role": "user", "content": f"¿Esta pregunta está en la base de datos? Responde con 'Sí' o 'No'. Pregunta: {query}"}
            ],
            temperature=0
        )
        return "sí" in response.choices[0].message.content.lower()
    except Exception as e:
        print(f"Error en should_use_rag: {e}")
        return True  # Por defecto, intentar con RAG si OpenAI falla

# ✅ Agregar imagen de fondo
def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background("https://i.ibb.co/cDMTyCr/6191107.jpg")

# ✅ Mensaje de bienvenida al inicio de la aplicación
st.markdown(
    """
    <h2 style='text-align: center; color: white;'>🤖 Welcome to the Financial ChatBot Advisor! 🤖</h2>
    <p style='text-align: center; color: white; font-size: 18px;'>
        I am a specialized chatbot designed to assist you with financial insights, AI-powered trading strategies, and portfolio optimization. 
        Feel free to ask me anything! 🚀
    </p>
    """,
    unsafe_allow_html=True
)

# ✅ Sidebar con imagen y texto de bienvenida
with st.sidebar:
    st.image("https://i.ibb.co/h8VS7xZ/Financial-Chat-Bot-new.png", caption="Welcome to the Best Financial ChatBot Advisory!")
    st.write("I can assist you with a wide range of topics.")

# ✅ Procesar entrada del usuario
if prompt := st.chat_input("Enter your Question"):
    # Guardar mensaje del usuario en historial
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Mostrar mensaje del usuario
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # ✅ Verificar si la entrada es un saludo/despedida
    cordial_response = respuesta_cordial(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        if cordial_response:
            response_text = cordial_response  # Respuesta cordial sin consultar APIs
        else:
            use_rag = should_use_rag(prompt)
            response_text = rag_response(prompt) if use_rag else "No puedo responder esa pregunta sin datos."

        # ✅ Mostrar la respuesta en el chat con efecto de escritura
        response = st.write_stream(response_generator_dynamic(response_text))

    # Guardar respuesta en historial
    st.session_state["messages"].append({"role": "assistant", "content": response_text})
