import streamlit as st
import pandas as pd

# Cargar el historial ya procesado desde un archivo en línea o local
@st.cache_data
def cargar_datos():
    # Asegúrate de que este enlace de Google Drive esté configurado
    # para compartir 'Cualquier persona con el enlace' como 'Lector'.
    # La URL debe ser el enlace de descarga directa.
    # Puedes obtenerla desde el enlace 'Compartir' de Google Drive,
    # pero necesitas modificarla para que sea de descarga.
    # Una URL de descarga directa típica se ve así:
    # 'https://drive.google.com/uc?export=download&id=ID_DEL_ARCHIVO'
    url = 'https://drive.google.com/uc?id=1LA45WNkpf8CsQ_NJbHunkhYuWsUEkYGM&export=download' # Añadido &export=download
    try:
        df = pd.read_csv(url, dtype=str)
        # Opcional: Limpiar nombres de columna aquí también
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame() # Retorna un DataFrame vacío en caso de error


# --- Interfaz de Usuario de Streamlit ---

st.title("📄 Ficha de Usuario - SANIMA")

# Cargar los datos usando la función cacheada
df = cargar_datos()

# Verificar si los datos se cargaron correctamente
if not df.empty:
    # Widget de entrada de texto para el ID del usuario
    usuario_id = st.text_input("🔎 Ingresa el DNI del usuario:", "").strip() # Añadido .strip() para limpiar espacios

    if usuario_id:
        # Filtrar el DataFrame por el ID ingresado
        # Usamos .copy() para evitar SettingWithCopyWarning si modificamos el sub-DataFrame más adelante
        ficha = df[df["ID"] == usuario_id].copy()

        if ficha.empty:
            st.warning(f"⚠️ Usuario con DNI/ID '{usuario_id}' no encontrado.")
        else:
            # Mostrar información básica del usuario
            nombre = ficha["Nombre del Depositante"].iloc[0] # .iloc[0] porque esperamos una sola fila por ID principal
            st.subheader(f"👤 {nombre}")

            # Ordenar por mes para una mejor visualización del historial
            # Esto requiere que la columna 'Mes' tenga un formato ordenable,
            # o que mapees los meses a un orden numérico antes de ordenar.
            # Si "Mes" es "ENE25", "FEB25", etc., la ordenación alfabética
            # debería funcionar para el rango que tienes.
            ficha = ficha.sort_values(by="Mes")

            # Definir las columnas que quieres mostrar en la tabla de historial
            columnas_a_mostrar = [
                "Mes", # Incluir el mes para que sea el índice de la tabla
                "Deuda_inicial", "Deuda_final", "Documento", "Estado", "Mora",
                "Seguimiento", "Dias transcurridos", "Metodo de pago",
                "facturado_mensual", "item_mensual", "Acuerdo de pago"
            ]

            # Asegurarse de que solo seleccionamos columnas que realmente existen
            columnas_disponibles = [col for col in columnas_a_mostrar if col in ficha.columns]

            # Mostrar la tabla de historial
            # Usamos set_index("Mes") para que la columna "Mes" se convierta en el índice de la tabla en Streamlit
            st.dataframe(ficha[columnas_disponibles].set_index("Mes"))

else:
    st.error("Hubo un problema al cargar los datos. Por favor, verifica el enlace del archivo CSV.")
