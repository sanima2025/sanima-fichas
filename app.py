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
        nombre_col = next((col for col in ficha.columns if "Nombre" in col), "Nombre")
        nombre = ficha[nombre_col].iloc[0]
        st.subheader(f"👤 {nombre}")

        meses = ["ENE25", "FEB25", "MAR25", "ABR25", "MAY25"]
        campos = [
            "Deuda_inicial", "Deuda_final", "Documento", "Estado", "Mora",
            "Seguimiento", "Dias transcurridos", "Metodo de pago",
            "facturado_mensual", "Item_mensual"
        ]

        data = []
        for mes in meses:
            fila_mes = ficha  # Todas las filas del usuario para ese mes
            fila = {"Mes": mes}

            # Sumar deuda inicial y final
            deuda_inicial_col = f"Deuda_inicial_{mes}"
            deuda_final_col = f"Deuda_final_{mes}"

            deuda_inicial = pd.to_numeric(fila_mes[deuda_inicial_col], errors='coerce').sum() if deuda_inicial_col in ficha.columns else ""
            deuda_final = pd.to_numeric(fila_mes[deuda_final_col], errors='coerce').sum() if deuda_final_col in ficha.columns else ""

            fila["Deuda_inicial"] = deuda_inicial if deuda_inicial != 0 else ""
            fila["Deuda_final"] = deuda_final if deuda_final != 0 else ""

            # Otros campos: solo el primero no vacío
            for campo in campos:
                if campo in ["Deuda_inicial", "Deuda_final"]:
                    continue
                col = f"{campo}_{mes}"
                fila[campo] = fila_mes[col].dropna().iloc[0] if col in ficha.columns and not fila_mes[col].dropna().empty else ""

            # Acuerdo de pago: interpretar todos los valores y mostrar el más relevante
            acuerdo_col = f"Acuerdo pago_{mes}"
            acuerdos = fila_mes[acuerdo_col].dropna().astype(str).str.upper() if acuerdo_col in ficha.columns else pd.Series(dtype=str)
            acuerdo_valor = "Sin observación"
            for acuerdo_raw in acuerdos:
                if "AP" in acuerdo_raw:
                    acuerdo_valor = "Solicitó Acuerdo de pago"
                    break
                elif "DES" in acuerdo_raw:
                    acuerdo_valor = "Solicitó desinstalarse"
                elif "DPD" in acuerdo_raw:
                    acuerdo_valor = "Cobranzas solicitó su desinstalación"
                elif "1ER" in acuerdo_raw:
                    acuerdo_valor = "Primer mes en el servicio"
                elif "BOD" in acuerdo_raw:
                    acuerdo_valor = "Es parte de negocios aliados"
            fila["Acuerdo de pago"] = acuerdo_valor

            data.append(fila)

        ficha_vertical = pd.DataFrame(data)
        st.dataframe(ficha_vertical)


