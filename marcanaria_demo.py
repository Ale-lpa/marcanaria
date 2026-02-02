import streamlit as st
import openai

# --- 1. CONFIGURACIÓN DE IDENTIDAD ---
NOMBRE_AGENCIA = "Marcanaria<br>"
ESLOGAN = "IMPULSAMOS TU MARCA"
# Logo transparente (fantasma) para limpieza visual
LOGO_URL = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" 

st.set_page_config(page_title="Asistente Marcanaria", layout="wide")

# --- 2. ESTÉTICA "DARK MODE" (Agencia Creativa) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800&display=swap');
    
    .stApp {{
        background-color: #0E0E0E; /* Negro casi puro */
        color: #FFFFFF;
    }}
    
    /* Título Impactante */
    .agency-title {{
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF; 
        font-size: 55px; 
        font-weight: 800;
        text-transform: uppercase;
        line-height: 0.9;
        text-align: left;
    }}
    
    /* Subtítulo en Gradiente o Color de Acento */
    .agency-subtitle {{
        background: -webkit-linear-gradient(45deg, #FF512F, #DD2476); /* Gradiente rojizo/creativo */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-top: 10px;
    }}

    /* Chat Styling */
    .stChatMessage [data-testid="stMarkdownContainer"] p {{
        color: #E0E0E0 !important;
        font-size: 1.1rem !important;
        font-family: sans-serif;
    }}
    
    /* Input Box Minimalista */
    [data-testid="stChatInput"] {{
        background-color: #1A1A1A !important;
        border: 1px solid #333333 !important;
        color: white !important;
        border-radius: 20px !important;
    }}
    
    /* Ocultar elementos extra */
    [data-testid="stImage"] {{ display: none !important; }}
    .stChatInputContainer {{ padding-bottom: 30px !important; }}
    
    </style>
""", unsafe_allow_html=True)

# --- 3. CABECERA ---
col1, col2 = st.columns([0.1, 0.9])
with col2:
    st.markdown(f'<div class="agency-title">{NOMBRE_AGENCIA}</div><div class="agency-subtitle">{ESLOGAN}</div>', unsafe_allow_html=True)
st.markdown("---")

# --- 4. LÓGICA DE AGENCIA (SYSTEM PROMPT) ---
SYSTEM_PROMPT = """
Eres el Asistente Virtual de Marcanaria (Agencia de Marketing y Producción).
TONO: Creativo, directo, joven, profesional. Usa emojis (🚀, 🔥, 📸).

TUS OBJETIVOS:
1. Filtrar clientes: Pregunta qué tipo de negocio tienen antes de dar precios.
2. Servicios: Explica que sois expertos en Reels, Gestión de Redes y Producción Audiovisual.
3. Precios: No des precios exactos. Di "Nuestros packs de gestión empiezan desde X€, pero depende de tu proyecto".
4. Cierre: Para contratar, diles que escriban un DM en Instagram a @marcanaria.
"""

if "messages" not in st.session_state: st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    icon = "👤" if message["role"] == "user" else "⚡" # Icono de rayo para la agencia
    with st.chat_message(message["role"], avatar=icon): st.markdown(message["content"])

# Input y Respuesta
if prompt := st.chat_input("Pregúntame sobre gestión de redes, reels..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        stream = client.chat.completions.create(
            model="gpt-4o", 
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages, 
            stream=True
        )
        full_response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
