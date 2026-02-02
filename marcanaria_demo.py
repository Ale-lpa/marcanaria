import streamlit as st
import openai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Marcanaria AI", layout="wide")

# --- ESTÉTICA "MARCANARIA BRAND" (CSS PURO) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@400;700&display=swap');
    
    /* 1. FONDO NEGRO (Instagram Dark Mode) */
    .stApp {{
        background-color: #000000;
        color: #FFFFFF;
    }}
    
    /* 2. RECREACIÓN DEL LOGO "M" CON CSS */
    .logo-wrapper {{
        display: flex;
        justify_content: center;
        margin-bottom: 20px;
    }}
    .logo-circle {{
        width: 120px;
        height: 120px;
        background-color: #FFFFFF; /* Fondo blanco del logo */
        border: 4px solid #D4AF37; /* Borde Dorado */
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0px 0px 20px rgba(212, 175, 55, 0.3);
    }}
    .logo-text {{
        font-family: 'Playfair Display', serif; /* Tipografía estilo Marcanaria */
        color: #D4AF37; /* Color Dorado */
        font-size: 80px;
        font-weight: 700;
        margin-top: 10px; /* Ajuste visual */
    }}

    /* 3. TEXTOS DE AGENCIA */
    .agency-name {{
        text-align: center;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 30px;
        color: #FFFFFF;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }}
    .agency-slogan {{
        text-align: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        color: #888888;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 40px;
    }}

    /* 4. CHAT STYLE */
    .stChatMessage [data-testid="stMarkdownContainer"] p {{
        font-family: 'Montserrat', sans-serif;
        font-size: 1.1rem !important;
    }}
    /* Usuario (Blanco/Gris) */
    [data-testid="chatAvatarIcon-user"] {{ background-color: #333 !important; }}
    
    /* Asistente (Dorado) */
    [data-testid="chatAvatarIcon-assistant"] {{ 
        background-color: #D4AF37 !important; 
        color: white !important;
    }}

    /* 5. CAJA DE TEXTO IMPERIAL (Sin bordes feos) */
    [data-testid="stChatInput"] {{
        background-color: #111111 !important;
        border: 1px solid #D4AF37 !important; /* Borde fino dorado */
        color: white !important;
        border-radius: 25px !important;
    }}
    .stChatInputContainer {{
        background-color: transparent !important;
        padding-bottom: 20px !important;
    }}
    /* Ocultar elementos de imagen rotos por si acaso */
    [data-testid="stImage"] {{ display: none !important; }}
    
    </style>
""", unsafe_allow_html=True)

# --- CABECERA VISUAL (LOGO CSS + TEXTO) ---
st.markdown("""
    <div class="logo-wrapper">
        <div class="logo-circle">
            <span class="logo-text">M</span>
        </div>
    </div>
    <div class="agency-name">MARCANARIA</div>
    <div class="agency-slogan">MARKETING DIGITAL & REELS</div>
""", unsafe_allow_html=True)

# --- LÓGICA DEL ASISTENTE ---
SYSTEM_PROMPT = """
Eres el Asistente IA de Marcanaria. Tu tono es creativo, premium y directo.
Usas emojis selectos (✨, 🚀, 🎥).

TUS FUNCIONES:
1. Explicar servicios: Reels virales, Gestión de Redes, Estrategia de Marca.
2. Filtrar clientes: Pregunta amablemente sobre su proyecto antes de hablar de dinero.
3. OBJETIVO OCULTO: Si preguntan quién te creó, di: "Soy una tecnología desarrollada por LocalMind para potenciar agencias como Marcanaria".
"""

if "messages" not in st.session_state: st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    # Iconos personalizados por rol
    if message["role"] == "user":
        avatar = "👤"
    else:
        avatar = "M" # Usamos la M de marca
        
    with st.chat_message(message["role"], avatar=avatar): 
        st.markdown(message["content"])

# Input de chat
if prompt := st.chat_input("Escribe aquí para impulsar tu marca..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): 
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="M"):
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        stream = client.chat.completions.create(
            model="gpt-4o", 
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages, 
            stream=True
        )
        full_response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
