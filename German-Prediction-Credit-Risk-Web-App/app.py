from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import joblib
import pickle


# Initialize Flask app
app = Flask(__name__)

# Load your trained model and scaler
model = joblib.load("grid_rf.pkl")   # Ensure this file is in the same directory
scaler = joblib.load("scaler.pkl")   # Ensure this file exists too

@app.route("/")
def home():
    return render_template("index.html")

# API endpoint (for Postman or JSON request)
@app.route("/predict_api", methods=["POST"])
def predict_api():
    data = request.json["data"]
    print("Received data:", data)

    # Convert input to numpy array
    input_data = np.array(list(data.values())).reshape(1, -1)
    print("Transformed data:", input_data)

    # Apply scaling
    new_data = scaler.transform(input_data)

    # Make prediction
    output = model.predict(new_data)
    print("Prediction:", output[0])

    return jsonify({"prediction": str(output[0])})

# Web form endpoint (for HTML form)
@app.route("/predict", methods=["POST"])
def predict():
    data = [float(x) for x in request.form.values()]
    final_input = scaler.transform(np.array(data).reshape(1, -1))
    print(final_input)
    
    output = model.predict(final_input)[0]

    return render_template("index.html", prediction_text=f"The German Prediction Credit Risk is: {output}")

if __name__ == "__main__":
    app.run(debug=True)



