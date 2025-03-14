import streamlit as st
import requests

# URL base de la API Flask
API_URL = "http://localhost:5000"

st.title("Alerta Vida - Demo MVP")

st.write("""
Este es un prototipo para predecir el riesgo de Diabetes e Hipertensión basado en las siguientes variables:
- Edad
- IMC (Índice de Masa Corporal)
- Presión Sistólica
- Glucosa
""")

# Entradas de usuario
edad = st.slider("Edad", min_value=18, max_value=80, value=45)
imc = st.slider("IMC (Índice de Masa Corporal)", min_value=15.0, max_value=40.0, value=25.0)
presion_sistolica = st.slider("Presión Sistólica", min_value=90, max_value=200, value=120)
glucosa = st.slider("Glucosa (mg/dL)", min_value=50, max_value=250, value=100)

if st.button("Calcular Riesgo"):
    # Preparar el payload para la API
    payload = {
        "edad": edad,
        "imc": imc,
        "presion_sistolica": presion_sistolica,
        "glucosa": glucosa
    }
    try:
        response = requests.post(f"{API_URL}/predict", json=payload)
        if response.status_code == 200:
            data = response.json()
            prob_diabetes = data["prob_diabetes"]
            prob_hipertension = data["prob_hipertension"]

            st.write(f"**Probabilidad de Diabetes:** {prob_diabetes:.2f}")
            st.write(f"**Probabilidad de Hipertensión:** {prob_hipertension:.2f}")

            # Mostrar alertas basadas en umbrales
            if prob_diabetes > 0.6:
                st.error("ALERTA: Riesgo Alto de Diabetes. Se recomienda una consulta médica urgente.")
            elif prob_diabetes > 0.3:
                st.warning("Riesgo Medio de Diabetes. Se recomienda seguimiento médico.")
            else:
                st.success("Riesgo Bajo de Diabetes.")

            if prob_hipertension > 0.6:
                st.error("ALERTA: Riesgo Alto de Hipertensión. Se recomienda evaluación médica urgente.")
            elif prob_hipertension > 0.3:
                st.warning("Riesgo Medio de Hipertensión. Se recomienda seguimiento médico.")
            else:
                st.success("Riesgo Bajo de Hipertensión.")
        else:
            st.error("Error en la respuesta del servidor Flask.")
    except Exception as e:
        st.error(f"No se pudo conectar con la API. Detalles: {e}")
