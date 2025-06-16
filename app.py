import streamlit as st
import pandas as pd

# Cargar CSV procesado desde Drive (público)
@st.cache_data
def cargar_datos():
    url = 'https://drive.google.com/uc?id=1LA45WNkpf8CsQ_NJbHunkhYuWsUEkYGM'
    df = pd.read_csv(url, dtype=str)
    return df

df = cargar_datos()

st.title("📄 Ficha de Usuario - SANIMA")
usuario_id = st.text_input("🔎 Ingresa el DNI del usuario:", "")

if usuario_id:
    ficha = df[df["ID"] == usuario_id.strip()]

    if ficha.empty:
        st.warning("⚠️ Usuario no encontrado.")
    else:
        # Mostrar nombre
        nombre_col = next((col for col in ficha.columns if "Nombre" in col), "Nombre")
        nombre = ficha[nombre_col].iloc[0]
        st.subheader(f"👤 {nombre}")

        # Detectar columnas por mes
        columnas_base = [
            "Deuda_inicial", "Deuda_final", "Documento", "Estado", "Mora",
            "Seguimiento", "Dias transcurridos", "Metodo de pago",
            "facturado_mensual", "Item_mensual", "Acuerdo de pago"
        ]

        meses = ["ENE25", "FEB25", "MAR25", "ABR25", "MAY25"]
        columnas_finales = []

        for mes in meses:
            for base in columnas_base:
                col = f"{base}_{mes}"
                if col in ficha.columns:
                    columnas_finales.append(col)

        # Mostrar ficha ordenada
        columnas_mostrar = ["ID", nombre_col] + columnas_finales
        ficha_ordenada = ficha[columnas_mostrar].T
        ficha_ordenada.columns = ["Valor"]
        ficha_ordenada.index.name = "Campo"
        st.dataframe(ficha_ordenada)



