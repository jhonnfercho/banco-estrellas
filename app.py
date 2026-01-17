import streamlit as st
import sqlite3
import pandas as pd

# --- CONFIGURACIÓN DE BASE DE DATOS ---
def conectar_db():
    conn = sqlite3.connect('banco_estrellas.db')
    return conn

def crear_tablas():
    conn = conectar_db()
    c = conn.cursor()
    # Tabla de usuarios
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                 (id INTEGER PRIMARY KEY, nombre TEXT, estrellas INTEGER)''')
    # Tabla de transacciones (El historial de seguridad)
    c.execute('''CREATE TABLE IF NOT EXISTS historial 
                 (id INTEGER PRIMARY KEY, nombre TEXT, cantidad INTEGER, motivo TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# --- LÓGICA DE NEGOCIO ---
def agregar_estrellas(nombre, cantidad, motivo):
    conn = conectar_db()
    c = conn.cursor()
    c.execute("UPDATE usuarios SET estrellas = estrellas + ? WHERE nombre = ?", (cantidad, nombre))
    c.execute("INSERT INTO historial (nombre, cantidad, motivo) VALUES (?, ?, ?)", (nombre, cantidad, motivo))
    conn.commit()
    conn.close()

# --- INTERFAZ DE USUARIO (STREAMLIT) ---
st.title("🌟 Banco Escolar de Estrellas")
crear_tablas()

menu = ["Panel del Estudiante", "Panel del Maestro (Admin)"]
choice = st.sidebar.selectbox("Selecciona tu rol", menu)

if choice == "Panel del Estudiante":
    st.header("Consulta tu Saldo")
    nombre_usuario = st.text_input("Ingresa tu nombre exacto")
    if nombre_usuario:
        conn = conectar_db()
        user_data = pd.read_sql_query("SELECT estrellas FROM usuarios WHERE nombre=?", conn, params=(nombre_usuario,))
        conn.close()
        
        if not user_data.empty:
            st.metric(label="Tus Estrellas Actuales", value=f"{user_data.iloc[0]['estrellas']} ⭐")
        else:
            st.error("Usuario no encontrado.")

elif choice == "Panel_del_Maestro (Admin)":
    st.header("Administración de la Clase")
    pwd = st.text_input("Contraseña de Maestro", type="password")
    
    if pwd == "profe123": # Aquí pondrías tu clave secreta
        st.success("Acceso concedido")
        
        # Sección para crear alumnos
        nuevo_alumno = st.text_input("Nombre del nuevo alumno")
        if st.button("Registrar Alumno"):
            conn = conectar_db()
            c = conn.cursor()
            c.execute("INSERT INTO usuarios (nombre, estrellas) VALUES (?, 0)", (nuevo_alumno,))
            conn.commit()
            conn.close()
            st.info(f"Alumno {nuevo_alumno} registrado.")

        # Sección para dar estrellas
        st.divider()
        st.subheader("Asignar Estrellas")
        conn = conectar_db()
        lista_alumnos = pd.read_sql_query("SELECT nombre FROM usuarios", conn)
        conn.close()
        
        target = st.selectbox("Selecciona al alumno", lista_alumnos)
        puntos = st.number_input("Cantidad de estrellas", min_value=1, step=1)
        razon = st.text_input("¿Por qué gana estrellas?")
        
        if st.button("Dar Estrellas"):
            agregar_estrellas(target, puntos, razon)
            st.balloons()
            st.success(f"¡{puntos} estrellas enviadas a {target}!")