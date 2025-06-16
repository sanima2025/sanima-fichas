import streamlit as st
import pandas as pd

@st.cache_data
def cargar_datos():
    url = 'https://drive.google.com/uc?id=1LA45WNkpf8CsQ_NJbHunkhYuWsUEkYGM'
    return pd.read_csv(url, dtype=str)

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

        # Definir meses y campos
        meses = ["ENE25", "FEB25", "MAR25", "ABR25", "MAY25"]
        campos = [
            "Deuda_inicial", "Deuda_final", "Documento", "Estado", "Mora",
            "Seguimiento", "Dias transcurridos", "Metodo de pago",
            "facturado_mensual", "Item_mensual", "Acuerdo de pago"
        ]

        # Construir lista de dicts con info por mes
        datos = []
        for mes in meses:
            fila = {"Mes": mes}
            for campo in campos:
                col = f"{campo}_{mes}"
                fila[campo] = ficha[col].iloc[0] if col in ficha.columns else ""
            datos.append(fila)

        ficha_vertical = pd.DataFrame(datos)
        st.dataframe(ficha_vertical)




