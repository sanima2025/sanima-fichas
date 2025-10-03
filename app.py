import streamlit as st
import pandas as pd

@st.cache_data
def cargar_datos():
    url = 'https://docs.google.com/spreadsheets/d/1dVMR7LqY5DvZtvF9D6bmmigsuBzEGwMysLTrgbVZmBY/export?format=csv&gid=0'
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

        meses = ["ENE25", "FEB25", "MAR25", "ABR25", "MAY25", "JUN25", "JUL25","AGO25","SET25"]
        columnas = [
            "Deuda_inicial", "Deuda_final", "Documento", "Estado", "Mora",
            "Seguimiento", "Dias transcurridos", "Metodo de pago",
            "facturado_mensual", "Item_mensual",
            "Fecha_pago", "Negocio_aliado", "Nro_Operación"
        ]

        mapa_negocios = {
            "negociosanima01@gmail.com": "Bodega Madeley",
            "agentecobranza@sanima.pe": "Equipo de Cobranzas - Nicol",
            "yeany.mercado@sanima.pe": "Analista de Facturación",
            "gabriela.castro@sanima.pe": "Analista de Negocios Aliados",
            "agente.cobranza2@sanima.pe": "Equipo de Cobranzas - Wendy",
            "atencionusuario@sanima.pe": "Atención al usuario",
            "negociosanima02@gmail.com": "Bodega Mery",
            "negociosanima03@gmail.com": "La Bodega J.L.A",
            "negociosanima04@gmail.com": "Librería Teresa",
            "negociosanima05@gmail.com": "Bodega Emma",
            "negociosanima06@gmail.com": "Bodega Andreita",
            "negociosanima10@gmail.com": "Centro de fisioterapia Sadit",
            "negociosanima12@gmail.com": "Licorería 56",
            "negociosanima13@gmail.com": "Bodega Martha",
            "negociosanima14@gmail.com": "Bodega Comboni - FIorella",
            "negociosanima15@gmail.com": "Licorería El Desencanto",
            "negociosanima16@gmail.com": "Bodega Sarita",
            "negociosanima18@gmail.com": "Bodega Charada",
            "negociosanima19@gmail.com": "Bodega Cielo",
            "negociosanima21@gmail.com": "Bodega KIN",
            "negociosanima22@gmail.com": "Bodega Toki - Toki",
            "negociosanima26@gmail.com": "Bodega Vicky",
            "negociosanima27@gmail.com": "Bodega San Juan Bautista",
            "negociosanima28@gmail.com": "Bodega Geraldine",
            "negociosanima29@gmail.com": "Bodega Maria",
            "negociosanima30@gmail.com": "Bodega Marisol",
            "negociosanima31@gmail.com": "Bodega Cáceres",
            "negociosanima33@gmail.com": "Bodega Matias",
            "negociosanima34@gmail.com": "Centro de pago Nadine Heredia",
            "negociosanima35@gmail.com": "Bodega Laurita",
            "negociosanima36@gmail.com": "SugarCase",
            "negociosanima38@gmail.com": "Bodega Flor",
            "negociosanima39@gmail.com": "Bodega Balvina",
            "negociosanima40@gmail.com": "Bodega Marina",
            "negociosanima41.2@gmail.com": "Centro de pago Reyna",
            "negociosanima42@gmail.com": "Bodega Carmen",
            "negociosanima43@gmail.com": "Bodega Ana",
            "negociosanima45@gmail.com": "Librería Goyo",
            "negociosanima50@gmail.com": "Bodega Mary",
            "negociosanima47@gmail.com": "Bodega Sonia",
            "negociosanima48@gmail.com": "Bodega Mila",
            "negociosanima49@gmail.com": "Licorería Aspid",
            "negociosanima51@gmail.com": "Bodega Abad",
            "negociosanima52@gmail.com": "Centro de pago Balboa",
            "negociosanima53@gmail.com": "Bodega Nany",
            "negociosanima54@gmail.com": "Bodega David",
            "negociosanima55@gmail.com": "Bodega Lea",
            "negociosanima56@gmail.com": "Bodega Los Ancashinos",
            "negociosanima57@gmail.com": "Bodega Olga",
            "negociosanima58@gmail.com": "Bodega Arteaga",
            "negociosanima59@gmail.com": "Bodega - Bazar Kelly - Amy",
            "negociosanima60@gmail.com": "Bodega Jhustin",
            "negociosanima61@gmail.com": "Bodega Freddy",
            "negociosanima62@gmail.com": "Panadería-Pastelería Adrianito",
            "negociosanima63@gmail.com": "Bodega Soledad",
            "negociosanima64@gmail.com": "Libreria - Bazar Tinka Wasi",
            "negociosanima65@gmail.com": "Bodega Giselle",
            "negociosanima66@gmail.com": "Bodega Paulita",
            "negociosanima67@gmail.com": "Bodega Meiling",
            "negociosanima68@gmail.com": "Bodega Yesica",
            "negociosanima69@gmail.com": "Bodega Erika",
            "negociosanima70@gmail.com": "Bodega restaurante Wicho",
            "negociosanima71@gmail.com": "Bodega Hair y hermanas",
            "negociosanima72@gmail.com": "Bodega J y R",
            "negociosanima74@gmail.com": "Bodega Nicolle",
            "negociosanima76@gmail.com": "Libreria Kael",
            "negociosanima77@gmail.com": "Libreria Bazar Lucy",
            "negociosanima78@gmail.com": "Bodega Valentina",
            "atencion.usuario@sanima.pe": "Atención al Usuario"
        }

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

            col_negocio = f"Negocio_aliado_{mes}"
            correo = str(ficha[col_negocio].iloc[0]).strip().lower() if col_negocio in ficha.columns else ""
            nombre_negocio = mapa_negocios.get(correo, "No identificado")
            fila["Nombre del negocio aliado"] = nombre_negocio

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
