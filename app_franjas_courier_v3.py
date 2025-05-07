
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Franjas Horarias por Courier", layout="wide")

st.title("📦 Franjas Horarias Consolidadas por Courier")

# Subir archivo
uploaded_file = st.file_uploader("📁 Sube el archivo de franjas consolidadas (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Convertir columnas de texto a datetime (hora)
    df["Franjas_Horario.inicio"] = pd.to_datetime(df["Franjas_Horario.inicio"], errors="coerce")
    df["Franjas_Horario.final"] = pd.to_datetime(df["Franjas_Horario.final"], errors="coerce")

    # Columnas exactas esperadas
    required_cols = ["courier_ID", "codigo_ciudad", "dia", "Franjas_Horario.inicio", "Franjas_Horario.final"]
    if all(col in df.columns for col in required_cols):
        ciudad = st.selectbox("📍 Selecciona ciudad", sorted(df["codigo_ciudad"].dropna().unique()))
        courier = st.selectbox("🧍 Selecciona courier", sorted(df[df["codigo_ciudad"] == ciudad]["courier_ID"].dropna().unique()))

        filtered = df[(df["codigo_ciudad"] == ciudad) & (df["courier_ID"] == courier)]

        st.write(f"### 📅 Horarios para el courier {courier} en {ciudad}")
        st.dataframe(filtered, use_container_width=True)

        # Descargar resultados filtrados
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Descargar como CSV", csv, f"franjas_{courier}_{ciudad}.csv", "text/csv")
    else:
        st.error(f"El archivo debe contener las columnas: {', '.join(required_cols)}")
else:
    st.info("Sube un archivo para comenzar.")
