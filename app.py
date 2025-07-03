import streamlit as st
import pandas as pd

@st.cache_data
def cargar_datos():
    url = 'https://docs.google.com/spreadsheets/d/1E7OJ88XWBNENMfI2uX8QPpP6pkxGH6gELbgIlQSnja4/export?format=csv'
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
        
        meses = ["ENE25", "FEB25", "MAR25", "ABR25", "MAY25","JUN25"]
        columnas = [
            "Deuda_inicial", "Deuda_final", "Documento", "Estado", "Mora",
            "Seguimiento", "Dias transcurridos", "Metodo de pago",
            "facturado_mensual", "Item_mensual",
            "Fecha_pago", "Negocio_aliado", "Nro_Operación"
        ]
        
        data = []
        for mes in meses:
            fila = {"Mes": mes}
            for col in columnas:
                col_name = f"{col}_{mes}"
                if col_name in ficha.columns:
                    valores = ficha[col_name].dropna().astype(str)
                    valores = valores.replace("-", "").replace("nan", "").tolist()
                    valores_limpios = list({v.strip() for v in valores if v.strip()})
                    fila[col] = " / ".join(valores_limpios) if valores_limpios else ""
                else:
                    fila[col] = ""
            
            # Acuerdo de pago (solo aplica la lógica sobre todas las filas del mes)
            acuerdo_col = f"Acuerdo pago_{mes}"
            acuerdos = ficha[acuerdo_col].dropna().astype(str).str.upper() if acuerdo_col in ficha.columns else []
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





