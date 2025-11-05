import streamlit as st
from groq import Groq
# sacado del internet:
import re
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('style.css')
# ya no mas
# streamlit run michatbot.py
st.set_page_config(page_title="GregorIA House", page_icon="house.png")
st.title("GregorIA House - Nicanor Vecchi Contreras")
# "Homemade Apple:https://fonts.googleapis.com/css2?family=Homemade+Apple&display=swap" 
# "Montserrat:https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap"
nombre = st.text_input("Cual es tu nombre?")
if st.button("Saludar!"):
    st.write(f"Hola {nombre}! Bienvenido a talento tech")

MODELOS = ["qwen/qwen3-32b", "groq/compound", "llama-3.1-8b-instant","openai/gpt-oss-120b"]
#MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']
def configurar_pagina():
    st.title("GregorIA House Chat")
    st.sidebar.title("Elegir modelo")

    elegirModelo = st.sidebar.selectbox(
        "Elegi un modelo",
        options = MODELOS,
        index = 0
    )

    return elegirModelo

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
      model=modelo,
      messages=[
            {
            "role": "system",
            "content": "El usuario habla normalmente en español. Tus respuestas serian chistosas si es que respondes de forma rapida y corta, como si un doctor anoto algo rapido al paciente, sin emocion pero no malevolo. 2% terco. Pero no menciones lo que te dijo el sistema, lo hiciste anteriormente. Te hace sonar como un bot."
            },
            {
            "role": "user",
            "content": mensajeDeEntrada,

            }
            ],
      stream=True
    )
#clase 8
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})
def mostrar_historial():
    for mensaje in st.session_state.mensajes:  
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : 
            if mensaje["role"] != "user":
                st.markdown(mensaje["content"], unsafe_allow_html=True)
            else:
                st.markdown(mensaje["content"])
def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat: mostrar_historial()
#iniciar
# Clase 9 - funciones
def generar_respuestas(chat_completo):
    respuesta_completa = ""
    
    for frase in chat_completo:
        encontrado = frase.choices[0].delta.content
        if encontrado:
            respuesta_completa += encontrado
    # codigo para ignorar los think
    result = ""
    i = 0
    n = len(respuesta_completa)
    skip = False
    while i < n:
        # Check if we found a <think>
        if respuesta_completa[i]:
            if respuesta_completa[i:i+7].lower() == "<think>":
                skip = True
            elif respuesta_completa[i:i+8].lower() == "</think>":
                i = i + 7
                skip = False
            elif skip == False:
                result = result+respuesta_completa[i]
                yield respuesta_completa[i]
        i += 1
    return result
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat() # Función de esta clase
    mensaje = st.chat_input("Escribí tu mensaje:")
    if mensaje:
        actualizar_historial("user", mensaje, "usuario.jpg")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "house.png")
                st.rerun()
if __name__ == "__main__":
    main()
