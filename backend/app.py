# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# WORKAROUND: Force TensorFlow to use legacy Keras (fixes 'Layer dense expects 1 input' error on Render)
os.environ["TF_USE_LEGACY_KERAS"] = "1"

# WORKAROUND: Fix for TensorFlow < 2.10 on Windows with newer NumPy
try:
    import tensorflow.python.framework.dtypes
    import tensorflow.python.framework.tensor_util
except ImportError:
    pass

try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing import image
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not found. Using mock predictions.")
try:
    import numpy as np
    NP_AVAILABLE = True
except ImportError:
    NP_AVAILABLE = False
    print("NumPy not found. Using pure Python mocks.")
import os
import random


app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Enable CORS for frontend-backend communication

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.h5')

# Serve static files
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

# Serve other static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)


# Load pre-trained model or use mock model
model = None
try:
    model = load_model(MODEL_PATH)
    print("Model loaded successfully!")
except FileNotFoundError:
    print(f"Model file '{MODEL_PATH}' not found. Using mock predictions for demonstration.")
except Exception as e:
    print(f"Error loading model: {e}. Using mock predictions for demonstration.")

# Define class labels - must match the order used during training
labels = ["COVID-19", "Normal", "Pneumonia"]  # Match the training order

def preprocess_image(img_path):
    """
    Preprocess the uploaded image to match model input requirements.
    """
    if not TF_AVAILABLE or not NP_AVAILABLE:
        raise ImportError("TensorFlow or NumPy not available")
        
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    # Normalize pixel values to [0, 1] as done during training
    img_array /= 255.0
    return img_array

def mock_predict():

    """
    Generate a mock prediction for demonstration purposes.
    """
    if NP_AVAILABLE:
        # Simulate model prediction with random results using numpy
        prediction = np.random.rand(len(labels))
        prediction = prediction / np.sum(prediction)  # Normalize to probabilities
        class_idx = np.argmax(prediction)
        confidence = float(np.max(prediction))
        return class_idx, confidence
    else:
        # Pure python implementation
        prediction = [random.random() for _ in range(len(labels))]
        total = sum(prediction)
        prediction = [p/total for p in prediction]
        confidence = max(prediction)
        class_idx = prediction.index(confidence)
        return class_idx, confidence

@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint to receive an image and return AI-generated diagnosis in a conversational format.
    """
    if "image" not in request.files:
        return jsonify({"success": False, "error": "Please upload a medical image (X-ray, MRI, CT scan) to get a diagnosis."}), 400
    
    file = request.files["image"]
    img_path = os.path.join("uploads", file.filename)
    file.save(img_path)

    try:
        if TF_AVAILABLE and NP_AVAILABLE and model is not None:
            # Use real model prediction
            processed_img = preprocess_image(img_path)
            prediction = model.predict(processed_img)
            class_idx = np.argmax(prediction[0])
            confidence = float(np.max(prediction[0]))
        else:
            # Use mock prediction
            class_idx, confidence = mock_predict()
        
        # Confidence Threshold to filter non-medical images
        # Apply this check for BOTH real and mock predictions
        if confidence < 0.60:
            diagnosis = "Uncertain"
            response = {
                "success": True,
                "prediction": {
                    "class": "Uncertain",
                    "confidence": confidence,
                    "description": "Low confidence. This may not be a medical image."
                },
                "response": "I am not sure about this image. It does not look like a standard Chest X-ray. Please upload a clear medical image."
            }
            return jsonify(response)

        diagnosis = labels[class_idx]

        # Return response format that frontend expects
        response = {
            "success": True,
            "prediction": {
                "class": diagnosis,
                "confidence": confidence,
                "description": f"AI detected {diagnosis} with {confidence * 100:.2f}% confidence"
            },
            "response": f"Based on the uploaded image, the AI suggests: {diagnosis} (Confidence: {confidence * 100:.2f}%)."
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"success": False, "error": f"An error occurred: {str(e)}"}), 500


# Placeholder for future chatbot/conversation features
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    # For now, just echo the message. Extend this for real chat features.
    return jsonify({"response": f"You said: {user_message}. Chat features coming soon!"})

if __name__ == "__main__":
    # Ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)
    # Run the Flask app
    print("Starting Medical AI Bot...")
    print("Frontend will be available at: http://localhost:5003")
    print("API endpoints:")
    print("   - POST /predict - Upload medical images for diagnosis")
    print("   - POST /chat - Chat with the AI (coming soon)")
    app.run(debug=True, host='0.0.0.0', port=5003)
