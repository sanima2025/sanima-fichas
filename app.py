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
        nombre = ficha["Nombre del Depositante"].iloc[0]
        st.subheader(f"👤 {nombre}")
        ficha = ficha.sort_values(by="Mes")
        st.dataframe(ficha.set_index("Mes")[[
            "Deuda_inicial", "Deuda_final", "Documento", "Estado", "Mora",
            "Seguimiento", "Dias_transcurridos", "Metodo_de_pago",
            "facturado_mensual", "Item_mensual", "Acuerdo de pago"
        ]])
