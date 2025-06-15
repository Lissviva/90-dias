import streamlit as st
import pandas as pd
import os
import random
from datetime import date

# ----------- 1. CONFIGURACIÓN GLOBAL -----------
PASSWORD = "reto2025"
USERS_DIR = "participantes"

if not os.path.exists(USERS_DIR):
    os.makedirs(USERS_DIR)

# ----------- 2. ESTILO VISUAL -----------
# 🌸 Fondo púrpura pastel completo
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #EBDCFB !important;
    }
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------- 3. LOGIN -----------
def login():
    st.title("🌸 Bienvenida al Reto de 90 Días")
    nombre = st.text_input("Ingresa tu nombre", key="nombre_login").strip().lower()
    password = st.text_input("Contraseña", type="password", key="clave_login")

    if nombre and password == PASSWORD:
        st.session_state["logueada"] = True
        st.session_state["nombre"] = nombre
        st.success(f"¡Hola {nombre.title()}! Acceso concedido.")
        st.rerun()()
    elif password and password != PASSWORD:
        st.error("Contraseña incorrecta")

# ----------- 4. PROGRESO Y RESPUESTAS -----------

def obtener_progreso(nombre):
    archivo = os.path.join(USERS_DIR, f"{nombre}_progreso.csv")
    if not os.path.exists(archivo):
        df = pd.DataFrame({'día': range(1, 91), 'completado': [False]*90})
        df.to_csv(archivo, index=False)
    else:
        df = pd.read_csv(archivo)
    return df

def actualizar_progreso(nombre, dia_actual):
    archivo = os.path.join(USERS_DIR, f"{nombre}_progreso.csv")
    df = pd.read_csv(archivo)
    df.loc[dia_actual, "completado"] = True
    df.to_csv(archivo, index=False)

def guardar_respuesta(nombre, dia_actual, texto, patron_emocional=None):
    archivo = os.path.join(USERS_DIR, f"{nombre}_respuestas.csv")
    nueva_fila = {
        "Nombre": nombre.title(),
        "Día": dia_actual + 1,
        "Fecha": date.today().strftime("%Y-%m-%d"),
        "Reflexión": texto,
        "Patrón emocional": patron_emocional if patron_emocional else ""
    }
    if os.path.exists(archivo):
        df = pd.read_csv(archivo)
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    else:
        df = pd.DataFrame([nueva_fila])
    df.to_csv(archivo, index=False)

def guardar_pdf(nombre, dia_actual, archivo_pdf):
    carpeta = os.path.join(USERS_DIR, nombre, f"dia_{dia_actual + 1}")
    os.makedirs(carpeta, exist_ok=True)
    with open(os.path.join(carpeta, archivo_pdf.name), "wb") as f:
        f.write(archivo_pdf.read())

# ----------- 5. RETOS DIARIOS -----------

def reto_dia_1(nombre):
    st.markdown("## 📅 Día 1 – Auto-descubrimiento")
    st.markdown("> **Frase:** “¿Cada vez que alguien se aleja, tu herida habla. ¿La escuchas o la ignoras?”")
    opcion = st.radio("🌀 ¿Qué haces cuando alguien se aleja emocionalmente?", [
        "a) Lo persigo emocionalmente",
        "b) Me lleno de ansiedad y me hago la fría",
        "c) Me convenzo de que es mi culpa",
        "d) Me retiro en silencio pero espero que vuelva"
    ])
    texto = st.text_area("✍️ ¿Qué patrón reconoces en tus relaciones? ¿Puedes dar más detalles?")
    archivo = st.file_uploader("📎 O sube un archivo (PDF)", type=["pdf"])
    if st.button("Enviar actividad"):
        if texto or archivo:
            guardar_respuesta(nombre, 0, f"Respuesta test: {opcion}\n\nReflexión:\n{texto}")
            if archivo:
                guardar_pdf(nombre, 0, archivo)
            actualizar_progreso(nombre, 0)
            st.success("¡Actividad guardada! Mañana se desbloqueará un nuevo reto.")
            st.stop()
        else:
            st.warning("Por favor, escribe algo o sube un archivo.")

def reto_dia_2(nombre):
    st.markdown("## 📅 Día 2 – ¿Por qué aceptas menos?")
    st.markdown("> **Frase:** “¿Qué parte de ti teme tanto quedarse sola que acepta menos de lo que merece?”")
    st.markdown("""
    🎯 Hoy vas a reconectar contigo misma. Elige una de estas actividades a solas:
    - 💃 Baila una canción que te haga sentir poderosa.
    - ✍️ Escribe una carta de amor para ti misma.
    - 🌳 Da un paseo sin móvil.
    - 🍵 Prepara tu comida favorita solo para ti.
    """)
    texto = st.text_area("✍️ ¿Qué actividades disfrutas cuando estás sola? ¿Qué sientes al estar contigo? ¿Cuando disfrutas estar sola?")
    archivo = st.file_uploader("📎 O sube un archivo (PDF)", type=["pdf"])
    if st.button("Enviar actividad"):
        if texto or archivo:
            guardar_respuesta(nombre, 1, texto)
            if archivo:
                guardar_pdf(nombre, 1, archivo)
            actualizar_progreso(nombre, 1)
            st.success("¡Actividad guardada! Mañana se desbloqueará un nuevo reto.")
            st.stop()
        else:
            st.warning("Por favor, escribe algo o sube un archivo.")

def reto_dia_3(nombre):
    st.markdown("## 📅 Día 3 – Patrones ocultos")
    st.markdown("> “Sé la mujer que se espera a sí misma en la cima, no la que se pierde esperando amor a medias.”")
    patrones = [
        "Idealización del otro como refugio emocional",
        "Confundir intensidad con amor verdadero",
        "Buscar aprobación como validación personal",
        "Evitar estar sola porque el silencio duele",
        "Creer que mereces poco porque diste mucho"
    ]
    if "patron_dia3" not in st.session_state and st.button("🎯 Girar la rueda"):
        st.session_state["patron_dia3"] = random.choice(patrones)
    if "patron_dia3" in st.session_state:
        st.success(f"🎡 Hoy giraste y te salió: *{st.session_state['patron_dia3']}*")
        st.write("✍️ ¿Cómo lo has vivido tú? ¿Te reconoces?")
    texto = st.text_area("Escribe aquí tu reflexión")
    archivo = st.file_uploader("📎 O sube un archivo (PDF)", type=["pdf"])
    if st.button("Enviar actividad"):
        if texto or archivo:
            guardar_respuesta(nombre, 2, texto, st.session_state.get("patron_dia3", "No giró la rueda"))
            if archivo:
                guardar_pdf(nombre, 2, archivo)
            actualizar_progreso(nombre, 2)
            st.success("¡Actividad guardada! Mañana se desbloqueará un nuevo reto.")
            st.stop()
        else:
            st.warning("Por favor, escribe algo o sube un archivo.")

# ----------- 6. MOSTRAR RETO -----------

def mostrar_reto_por_dia(dia, nombre):
    if dia == 0:
        reto_dia_1(nombre)
    elif dia == 1:
        reto_dia_2(nombre)
    elif dia == 2:
        reto_dia_3(nombre)
    else:
        st.balloons()
        st.success("¡Has completado todos los retos disponibles! 🎉")
        st.write("Gracias por recorrer este camino de amor propio 💜")

# ----------- 7. MAIN APP -----------

def main():
    if "logueada" not in st.session_state:
        login()
    else:
        nombre = st.session_state.get("nombre", "amiga").title()

        st.markdown(f"### 🌷 Hola {nombre}, este es tu espacio seguro")

        st.markdown("""
        Bienvenida a este espacio solo para ti 💜  
        Durante 90 días, harás un viaje de reconexión contigo misma.  
        Cada día encontrarás una frase poderosa, un reto consciente y un momento de reflexión.  

        No tienes que ser perfecta, solo **valiente para mirarte con amor**.  
        Confía en ti, estás reconstruyéndote paso a paso 🌱
        """)

        # 👇 Separador visual entre la bienvenida y el reto
        st.markdown("---")

        df_progreso = obtener_progreso(st.session_state["nombre"])
        dia_actual = df_progreso[df_progreso["completado"] == False].index.min()
        if pd.isna(dia_actual):
            st.balloons()
            st.success("¡Has completado todos los retos! 🎉")
        else:
            mostrar_reto_por_dia(dia_actual, st.session_state["nombre"])

if __name__ == "__main__":
    main()