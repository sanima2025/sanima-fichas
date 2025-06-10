import streamlit as st
import pandas as pd

# Cargar el historial ya procesado desde un archivo en línea o local
@st.cache_data
def cargar_datos():
    url = 'https://drive.google.com/uc?id=1LA45WNkpf8CsQ_NJbHunkhYuWsUEkYGM'  # Reemplaza con tu enlace CSV PÚBLICO
    return pd.read_csv(url, dtype=str)

df = cargar_datos()

st.title("📄 Ficha de Usuario - SANIMA")

# Entrada de DNI/ID
usuario_id = st.text_input("🔎 Ingresa el DNI del usuario:", "")

if usuario_id:
    ficha = df[df["ID"] == usuario_id.strip()]
    if ficha.empty:
        st.warning("⚠️ Usuario no encontrado.")
    else:
        nombre = ficha["nombre_del_depositante"].iloc[0]
        st.subheader(f"👤 {nombre}")
        ficha = ficha.sort_values(by="mes")

        columnas_a_mostrar = [
            "deuda_inicial", "deuda_final", "documento", "estado", "mora",
            "seguimiento", "dias_transcurridos", "metodo_de_pago",
            "facturado_mensual", "item_mensual", "acuerdo_de_pago"
        ]
        # Filtrar solo las columnas que existen en el DataFrame 'ficha'
        columnas_disponibles = [col for col in columnas_a_mostrar if col in ficha.columns]

        st.dataframe(ficha.set_index("mes")[columnas_disponibles])
