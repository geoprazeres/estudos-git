import streamlit as st
from google import genai
from google.genai import types

# Configurando a página do navegador
st.set_page_config(page_title="Gege Chat", page_icon="🤖")
st.title("Conversando com a Gege 🤖")

# Define a personalidade da Gege
PERSONALIDADE = """
Você é Gege, uma assistente virtual super inteligente, bem-humorada, prestativa e amigável.
Você gosta de usar emojis e dar respostas claras, direto ao ponto.
"""

# Inicializa o cliente e o chat APENAS UMA VEZ na memória segura do Streamlit
if "client" not in st.session_state:
    # O Streamlit Cloud vai ler a chave direto do "Advanced Settings" que configuramos
    st.session_state.client = genai.Client()
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=PERSONALIDADE, temperature=0.7)
    )

# Cria o histórico de mensagens visual se ele não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra as mensagens antigas na tela (estilo balão de chat)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de texto estilo chat lá embaixo na tela
if prompt := st.chat_input("Digite sua mensagem para a Gege..."):
    # Mostra a mensagem do usuário na tela
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Envia para o Gemini usando a conexão guardada na memória de forma segura
    response = st.session_state.chat.send_message(prompt)

    # Mostra a resposta da Gege na tela
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
