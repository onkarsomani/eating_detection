from flask import Flask, request, jsonify
import joblib
import numpy as np
import cv2
import os

# Load the saved Random Forest model
model = joblib.load('random_forest_model.pkl')

app = Flask(__name__)

# Define the image size (same as before)
IMG_SIZE = 128

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    # Get the file from the request
    file = request.files['file']

    # Save the file temporarily
    file_path = os.path.join('temp.jpg')
    file.save(file_path)

    # Load and preprocess the image
    img = cv2.imread(file_path)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = np.array(img).reshape(1, -1) / 255.0  # Flatten and normalize the image

    # Predict using the model
    prediction = model.predict(img)

    # Interpret the result (0: no food, 1: food)
    result = "Food" if prediction[0] == 1 else "No Food"

    # Clean up the temporary file
    os.remove(file_path)

    # Return the prediction as JSON
    return jsonify({"prediction": result})

if __name__ == '__main__':
    app.run(debug=True)
