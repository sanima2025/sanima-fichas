import streamlit as st
import pandas as pd

# Cargar el historial desde Google Drive
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
        nombre = ficha["Nombre del Depositante"].iloc[0]
        st.subheader(f"👤 {nombre}")
        
        meses = ["ENE25", "FEB25", "MAR25", "ABR25", "MAY25"]
        columnas = [
            "Deuda_inicial", "Deuda_final", "Documento", "Estado", "Mora",
            "Seguimiento", "Dias transcurridos", "Metodo de pago",
            "facturado_mensual", "Item_mensual"
        ]
        
        data = []
        for mes in meses:
            fila = {"Mes": mes}
            for col in columnas:
                col_name = f"{col}_{mes}"
                if col_name in ficha.columns:
                    valor = ficha[col_name].dropna().astype(str).replace("-", "").replace("nan", "")
                    if valor.empty or valor.iloc[0] == "":
                    # Buscar el primer valor válido en el resto de las columnas del mismo tipo
                        col_alt = [c for c in ficha.columns if c.startswith(col + "_") and c != col_name]
                        for c_alt in col_alt:
                            val_alt = ficha[c_alt].dropna().astype(str).replace("-", "").replace("nan", "")
                            if not val_alt.empty and val_alt.iloc[0] != "":
                                fila[col] = val_alt.iloc[0]
                            break
                        else:
                            fila[col] = ""
                    else:
                        fila[col] = valor.iloc[0]
                else:
                    fila[col] = ""

            
            acuerdo_raw = str(ficha[f"Acuerdo pago_{mes}"].iloc[0] if f"Acuerdo pago_{mes}" in ficha.columns else "").upper()
            if "AP" in acuerdo_raw:
                fila["Acuerdo de pago"] = "Solicitó Acuerdo de pago"
            elif "DES" in acuerdo_raw:
                fila["Acuerdo de pago"] = "Solicitó desinstalarse"
            elif "DPD" in acuerdo_raw:
                fila["Acuerdo de pago"] = "Cobranzas solicitó su desinstalación"
            elif "1ER" in acuerdo_raw:
                fila["Acuerdo de pago"] = "Primer mes en el servicio"
            elif "BOD" in acuerdo_raw:
                fila["Acuerdo de pago"] = "Es parte de negocios aliados"
            else:
                fila["Acuerdo de pago"] = "Sin observación"
            
            data.append(fila)

        ficha_df = pd.DataFrame(data)

        # Mostrar con colores
    def resaltar_estado(val):
        if "CRÍTICO" in str(val).upper():
            return "background-color: #f51720; color: black"
        elif "RIESGO" in str(val).upper():
            return "background-color: #ffcc00; color: black"
        elif "UN MES" in str(val).upper():
            return "background-color: #90ee90; color: black"
        return "color: black"


    st.dataframe(ficha_df.style.applymap(resaltar_estado, subset=["Estado"]))

