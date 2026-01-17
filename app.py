import streamlit as st
import sqlite3
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Banco de Estrellas", page_icon="⭐")

def conectar_db():
    return sqlite3.connect('banco_escolar.db', check_same_thread=False)

# Crear tablas si no existen
conn = conectar_db()
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT PRIMARY KEY, estrellas INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS tienda (articulo TEXT PRIMARY KEY, costo INTEGER)')
conn.commit()

st.title("🌟 Mi Banco de Estrellas")

# --- MENÚ LATERAL ---
menu = ["Inicio (Saldo)", "Tienda de Premios", "Panel del Maestro"]
opcion = st.sidebar.selectbox("Ir a:", menu)

# --- PANEL DEL ESTUDIANTE ---
if opcion == "Inicio (Saldo)":
    st.header("✨ Consulta tus Estrellas")
    nombre_est = st.text_input("Escribe tu nombre:")
    if nombre_est:
        df = pd.read_sql_query("SELECT estrellas FROM usuarios WHERE nombre=?", conn, params=(nombre_est,))
        if not df.empty:
            st.metric("Saldo Actual", f"{df.iloc[0]['estrellas']} ⭐")
        else:
            st.warning("Nombre no registrado.")

# --- TIENDA ---
elif opcion == "Tienda de Premios":
    st.header("🛒 Canjea tus Estrellas")
    st.info("Próximamente disponible.")

# --- PANEL DEL MAESTRO ---
elif opcion == "Panel del Maestro":
    st.header("🔑 Administración")
    
    # ESTE ES EL CUADRO QUE BUSCAS:
    clave = st.text_input("Introduce la contraseña para ver las opciones:", type="password")
    
    if clave == "profe123":
        st.success("Acceso concedido")
        st.subheader("Registrar Alumno Nuevo")
        nuevo_nombre = st.text_input("Nombre completo del alumno:")
        estrellas_ini = st.number_input("Estrellas iniciales:", min_value=0, value=0)
        
        if st.button("Guardar Alumno"):
            if nuevo_nombre:
                c.execute("INSERT OR REPLACE INTO usuarios (nombre, estrellas) VALUES (?, ?)", (nuevo_nombre, estrellas_ini))
                conn.commit()
                st.success(f"¡{nuevo_nombre} ha sido registrado!")
            else:
                st.error("Por favor escribe un nombre.")
    elif clave != "":
        st.error("Contraseña incorrecta")

conn.close()