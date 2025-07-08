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

        meses = ["ENE25", "FEB25", "MAR25", "ABR25", "MAY25", "JUN25"]
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
            
            # Acuerdo de pago
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

        # --- Indicador de hábito de pago y advertencia ---
        dias_pago = []
        
        pagos_despues_17 = 0
        pagos_despues_25 = 0

        ficha_serie = ficha.iloc[0]  # Solo una fila (usuario único)

        for mes in meses:
            fecha_pago_raw = str(ficha_serie.get(f"Fecha_pago_{mes}", "")).strip()
            if not fecha_pago_raw or fecha_pago_raw.lower() == "nan":
                continue
            # Puede haber varias fechas separadas por '/', ',' o espacio
            delimitadores = ["/", ",", ";", " "]
            fechas = [fecha_pago_raw]
            for d in delimitadores:
                if d in fecha_pago_raw:
                    fechas = [f.strip() for f in fecha_pago_raw.split(d) if f.strip()]
                    break
            for fecha in fechas:
                # Intentar extraer el día según formato:
                dia = None
                if "-" in fecha:  # Ej: 2025-06-18
                    partes = fecha.split("-")
                    if len(partes) == 3 and partes[2].isdigit():
                        dia = int(partes[2])
                elif fecha.count("/") == 2:  # Ej: 18/06/2025
                    partes = fecha.split("/")
                    if len(partes) == 3 and partes[0].isdigit():
                        dia = int(partes[0])
                elif fecha.isdigit():  # Solo el día
                    dia = int(fecha)
                # Si es un día válido, lo añado al análisis
                if dia and 1 <= dia <= 31:
                    dias_pago.append(dia)
                    if 17 <= dia <= 31:
                        pagos_despues_17 += 1
                    if 25 <= dia <= 31:
                        pagos_despues_25 += 1

        # ADVERTENCIA si paga más de 3 veces tarde (día 25 a 31)
        if pagos_despues_25 > 3:
            st.error(f"⚠️ Este usuario ha pagado tarde (del día 25 al 31) en **{pagos_despues_25} meses**. ¡Requiere seguimiento especial!")

        if dias_pago:
            indicador = ""
            color = "gray"
            if pagos_despues_25 >= len(dias_pago) * 0.5:
                indicador = f"🔴 Suele pagar muy tarde en el mes (después del 25)."
                color = "#FF4B4B"
            elif pagos_despues_17 >= len(dias_pago) * 0.5:
                indicador = f"🟠 Tendencia a pagar del 17 al fin de mes."
                color = "#FFD600"
            else:
                indicador = f"🟢 Suele pagar temprano (antes del día 17)."
                color = "#8BC34A"
            st.markdown(
                f"<div style='background-color:{color};color:black;padding:0.6em;border-radius:8px;font-weight:bold'>"
                f"**Indicador de hábito de pago:** {indicador}"
                f"</div>", unsafe_allow_html=True)
        else:
            st.info("No hay información de pagos registrada para este usuario.")

        # --- Mostrar la ficha con colores ---
        def resaltar_estado(val):
            if "CRÍTICO" in str(val).upper():
                return "background-color: #f51720; color: black"
            elif "RIESGO" in str(val).upper():
                return "background-color: #ffcc00; color: black"
            elif "UN MES" in str(val).upper():
                return "background-color: #90ee90; color: black"
            return "color: black"

        st.dataframe(ficha_df.style.applymap(resaltar_estado, subset=["Estado"]))
