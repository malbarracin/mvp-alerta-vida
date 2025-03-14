import os
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Obtener la ruta actual del archivo app.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta para subir un nivel y acceder a los modelos en la carpeta raíz
model_diabetes_path = os.path.join(CURRENT_DIR, "..", "modelo_diabetes.pkl")
model_hipertension_path = os.path.join(CURRENT_DIR, "..", "modelo_hipertension.pkl")

# Cargar ambos modelos entrenados
model_diabetes = joblib.load(model_diabetes_path)
model_hipertension = joblib.load(model_hipertension_path)

@app.route("/")
def index():
    return "API de Alerta Vida: Modelos de Riesgo para Diabetes e Hipertensión"

@app.route("/predict", methods=["POST"])
def predict():
    """
    Recibe un JSON con los siguientes campos:
      - edad
      - imc
      - presion_sistolica
      - glucosa (para el modelo de diabetes)
    Devuelve un JSON con las probabilidades de riesgo para diabetes e hipertensión.
    """
    data = request.get_json()
    edad = data.get("edad", 0)
    imc = data.get("imc", 0)
    presion_sistolica = data.get("presion_sistolica", 120)
    glucosa = data.get("glucosa", 100)  # Usado solo para el modelo de diabetes

    # Preparar vector de características para cada modelo
    X_diabetes = [[edad, imc, presion_sistolica, glucosa]]
    X_hipertension = [[edad, imc, presion_sistolica]]
    
    # Obtener las probabilidades de riesgo
    prob_diabetes = model_diabetes.predict_proba(X_diabetes)[0][1]
    prob_hipertension = model_hipertension.predict_proba(X_hipertension)[0][1]

    return jsonify({
        "prob_diabetes": float(prob_diabetes),
        "prob_hipertension": float(prob_hipertension)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
