import sqlite3
import streamlit as st
import json

# ======================== Funciones de Base de Datos =========================
def inicializar_bd():
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada INTEGER DEFAULT 0
        )
    """)
    conexion.commit()
    conexion.close()

def agregar_tarea(titulo, descripcion):
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)", (titulo, descripcion))
    conexion.commit()
    conexion.close()

def listar_tareas():
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, titulo, descripcion, completada FROM tareas")
    tareas = cursor.fetchall()
    conexion.close()
    return tareas

def marcar_completada(id_tarea):
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE tareas SET completada = 1 WHERE id = ?", (id_tarea,))
    conexion.commit()
    conexion.close()

def eliminar_completadas():
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM tareas WHERE completada = 1")
    conexion.commit()
    conexion.close()

def guardar_tareas_a_archivo(nombre_archivo):
    tareas = listar_tareas()
    datos = [{"id": t[0], "titulo": t[1], "descripcion": t[2], "completada": bool(t[3])} for t in tareas]
    with open(nombre_archivo, 'w') as archivo:
        json.dump(datos, archivo)

def cargar_tareas_desde_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        datos = json.load(archivo)
        conexion = sqlite3.connect("tareas.db")
        cursor = conexion.cursor()
        for tarea in datos:
            cursor.execute(
                "INSERT INTO tareas (titulo, descripcion, completada) VALUES (?, ?, ?)",
                (tarea['titulo'], tarea['descripcion'], int(tarea['completada']))
            )
        conexion.commit()
        conexion.close()

# ======================== Interfaz Streamlit =========================
def main():
    st.title("Gestión de Tareas")
    menu = ["Agregar Tarea", "Listar Tareas", "Marcar Completada", "Eliminar Completadas", 
            "Guardar Tareas", "Cargar Tareas"]
    opcion = st.sidebar.selectbox("Menú", menu)

    if opcion == "Agregar Tarea":
        st.subheader("Agregar Nueva Tarea")
        titulo = st.text_input("Título")
        descripcion = st.text_area("Descripción")
        if st.button("Agregar"):
            if titulo.strip():
                agregar_tarea(titulo, descripcion)
                st.success("Tarea agregada correctamente.")
            else:
                st.error("El título no puede estar vacío.")

    elif opcion == "Listar Tareas":
        st.subheader("Lista de Tareas")
        tareas = listar_tareas()
        if tareas:
            for tarea in tareas:
                estado = "✔️ Completada" if tarea[3] else "❌ Pendiente"
                st.write(f"**ID:** {tarea[0]} | **Título:** {tarea[1]} | **Estado:** {estado}")
                st.write(f"**Descripción:** {tarea[2]}")
                st.write("---")
        else:
            st.info("No hay tareas registradas.")

    elif opcion == "Marcar Completada":
        st.subheader("Marcar Tarea como Completada")
        id_tarea = st.number_input("ID de la tarea", min_value=1, step=1)
        if st.button("Marcar como Completada"):
            marcar_completada(id_tarea)
            st.success(f"Tarea con ID {id_tarea} marcada como completada.")

    elif opcion == "Eliminar Completadas":
        st.subheader("Eliminar Tareas Completadas")
        if st.button("Eliminar Tareas Completadas"):
            eliminar_completadas()
            st.success("Tareas completadas eliminadas correctamente.")

    elif opcion == "Guardar Tareas":
        st.subheader("Guardar Tareas en Archivo JSON")
        nombre_archivo = st.text_input("Nombre del archivo (ejemplo: tareas.json)")
        if st.button("Guardar"):
            if nombre_archivo.strip():
                guardar_tareas_a_archivo(nombre_archivo)
                st.success(f"Tareas guardadas en {nombre_archivo}.")
            else:
                st.error("El nombre del archivo no puede estar vacío.")

    elif opcion == "Cargar Tareas":
        st.subheader("Cargar Tareas desde Archivo JSON")
        nombre_archivo = st.text_input("Nombre del archivo (ejemplo: tareas.json)")
        if st.button("Cargar"):
            try:
                cargar_tareas_desde_archivo(nombre_archivo)
                st.success(f"Tareas cargadas desde {nombre_archivo}.")
            except FileNotFoundError:
                st.error("El archivo no existe. Verifica el nombre.")

# ======================== Inicialización =========================
if __name__ == "__main__":
    inicializar_bd()
    main()
