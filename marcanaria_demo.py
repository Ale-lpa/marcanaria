import streamlit as st
import openai

# --- IDENTIDAD VISUAL DE MARCANARIA ---
NOMBRE_AGENCIA = "Marcanaria<br>Digital"
ESLOGAN = "Hacemos crecer tu marca"
# Usamos un logo dorado o transparente similar al suyo
LOGO_URL = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" 

st.set_page_config(page_title="Asistente Marcanaria", layout="wide")

# --- ESTÉTICA GOLD & DARK (Premium) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');
    
    .stApp {{
        background-color: #111111; /* Fondo oscuro elegante */
        color: #FFFFFF;
    }}
    
    /* Títulos en Dorado Marcanaria */
    .agency-title {{
        font-family: 'Montserrat', sans-serif;
        color: #D4AF37; 
        font-size: 50px; 
        font-weight: 700;
        text-transform: uppercase;
        text-align: right;
    }}
    .agency-subtitle {{
        color: #FFFFFF;
        font-size: 14px;
        text-align: right;
        letter-spacing: 3px;
        border-top: 1px solid #D4AF37;
    }}

    /* Chat Styling */
    .stChatMessage [data-testid="stMarkdownContainer"] p {{
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
    }}
    
    /* Input Box Styling */
    [data-testid="stChatInput"] {{
        background-color: #222222 !important;
        border: 1px solid #D4AF37 !important;
        color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- CABECERA ---
col1, col2 = st.columns([1, 3])
with col2:
    st.markdown(f'<div class="agency-title">{NOMBRE_AGENCIA}</div><div class="agency-subtitle">{ESLOGAN}</div>', unsafe_allow_html=True)

# --- LÓGICA DE AGENCIA CREATIVA ---
SYSTEM_PROMPT = """Eres el Asistente Creativo de Marcanaria.
TUS SERVICIOS:
1. Producción Audiovisual y Reels.
2. Marketing Digital y Gestión de Redes.
3. Creación de Contenido Estratégico.
OBJETIVO:
- Responde dudas de clientes potenciales sobre precios (da rangos), tiempos de entrega y disponibilidad.
- Usa un tono creativo, joven y profesional.
- Si piden cita, diles que escriban por DM.
"""

if "messages" not in st.session_state: st.session_state.messages = []

# Chat Logic (Simplificada para la demo)
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

if prompt := st.chat_input("Pregunta sobre nuestros servicios..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        # Aquí iría tu conexión a OpenAI
        response = "¡Hola! En Marcanaria nos encanta esa idea. 🚀 Para producciones de Reels solemos trabajar con packs mensuales. ¿Te gustaría que agendemos una llamada?" 
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
