#!/usr/bin/env python3
"""
Medical AI Flask Backend
Trained model: DenseNet121 (3-class: COVID-19, Normal, Pneumonia)
"""

import os
import sys
import json
from pathlib import Path

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_USE_LEGACY_KERAS'] = '1'

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np

# Try to import TensorFlow
try:
    import tensorflow as tf
    print("✓ TensorFlow loaded")
    TF_AVAILABLE = True
except Exception as e:
    print(f"✗ TensorFlow error: {e}")
    TF_AVAILABLE = False

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
CORS(app)

# Configuration
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / 'model.h5'
UPLOADS_DIR = BASE_DIR / 'uploads'
UPLOADS_DIR.mkdir(exist_ok=True)

# Model classes - must match training order
CLASS_LABELS = ["COVID-19", "Normal", "Pneumonia"]

# Class descriptions
CLASS_DESCRIPTIONS = {
    "COVID-19": "The X-ray shows signs consistent with COVID-19 pneumonia. Please consult a healthcare provider immediately.",
    "Normal": "The X-ray appears normal with no significant findings. However, a medical professional should review for confirmation.",
    "Pneumonia": "The X-ray shows signs consistent with pneumonia. We recommend immediate medical evaluation."
}

# Global model
model = None
model_loaded = False

def load_model():
    """Load the trained model safely"""
    global model, model_loaded
    
    if model_loaded:
        return model
    
    if not TF_AVAILABLE:
        print("⚠️  TensorFlow not available. Using mock mode.")
        model_loaded = True
        return None
    
    print("Loading AI model...")
    try:
        if not MODEL_PATH.exists():
            print(f"⚠️  Model file not found at {MODEL_PATH}")
            raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
        
        # Load model with TensorFlow
        model = tf.keras.models.load_model(
            str(MODEL_PATH),
            compile=False
        )
        print("✓ Model loaded successfully!")
        model_loaded = True
        return model
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        print("⚠️  Falling back to mock predictions")
        model_loaded = True
        return None

def mock_predict():
    """Generate mock prediction for testing"""
    import random
    class_idx = random.randint(0, 2)
    confidence = random.uniform(0.70, 0.98)
    return class_idx, confidence

def preprocess_image(image_path):
    """Preprocess image for model inference"""
    from tensorflow.keras.preprocessing import image
    
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize to [0, 1]
    
    return img_array

# Routes - Static files
@app.route('/')
def index():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except:
        return jsonify({"error": "Frontend not built. Run: npm run build in frontend directory"}), 404

@app.route('/<path:filename>')
def serve_static(filename):
    try:
        return send_from_directory(app.static_folder, filename)
    except:
        return jsonify({"error": f"File not found: {filename}"}), 404

# API Routes
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    loaded_model = load_model()
    return jsonify({
        "status": "healthy",
        "tensorflow_available": TF_AVAILABLE,
        "model_loaded": loaded_model is not None,
        "classes": CLASS_LABELS,
        "mode": "real" if loaded_model else "mock"
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Handle image upload and prediction
    Expected: multipart/form-data with 'image' file
    """
    try:
        # Check if image is provided
        if 'image' not in request.files:
            return jsonify({
                "success": False,
                "error": "No image provided"
            }), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        # Validate file type
        if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return jsonify({
                "success": False,
                "error": "Invalid file type. Please upload an image (JPG, PNG, GIF)"
            }), 400
        
        # Save uploaded file
        filename = file.filename
        filepath = UPLOADS_DIR / filename
        file.save(str(filepath))
        
        # Get model and make prediction
        loaded_model = load_model()
        
        if loaded_model is not None:
            # Real model prediction
            try:
                processed_img = preprocess_image(str(filepath))
                prediction = loaded_model.predict(processed_img, verbose=0)
                class_idx = int(np.argmax(prediction[0]))
                confidence = float(np.max(prediction[0]))
                mode = "real"
            except Exception as e:
                print(f"Prediction error: {e}")
                return jsonify({
                    "success": False,
                    "error": f"Prediction failed: {str(e)}"
                }), 500
        else:
            # Mock prediction for testing
            class_idx, confidence = mock_predict()
            mode = "mock"
        
        # Get class info
        class_name = CLASS_LABELS[class_idx]
        description = CLASS_DESCRIPTIONS.get(class_name, "Diagnosis complete.")
        
        response = {
            "success": True,
            "prediction": {
                "class": class_name,
                "confidence": confidence,
                "description": description,
                "all_predictions": {
                    CLASS_LABELS[i]: float(prediction[0][i]) if loaded_model else None
                    for i in range(len(CLASS_LABELS))
                } if loaded_model else None
            },
            "mode": mode,
            "filename": filename
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in /predict: {e}")
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint for AI health assistant
    Expected: JSON with 'message' field
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "No message provided"
            }), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                "success": False,
                "error": "Message cannot be empty"
            }), 400
        
        # Generate response
        response_text = generate_chat_response(user_message)
        
        return jsonify({
            "success": True,
            "response": response_text,
            "message": user_message
        })
    
    except Exception as e:
        print(f"Error in /chat: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def generate_chat_response(user_message):
    """Generate an AI response to user health questions"""
    message_lower = user_message.lower()
    
    # Simple keyword-based responses (can be replaced with actual AI in future)
    if any(word in message_lower for word in ['covid', 'coronavirus', 'sars']):
        return "COVID-19 is a respiratory illness. Please consult a healthcare provider if you experience symptoms like fever, cough, or difficulty breathing. For diagnosis, chest X-rays can be helpful."
    
    elif any(word in message_lower for word in ['pneumonia', 'lung infection']):
        return "Pneumonia is a lung infection that can be serious. Symptoms include cough, fever, and chest pain. Please seek medical attention if you suspect pneumonia."
    
    elif any(word in message_lower for word in ['fever', 'cough', 'shortness', 'breath']):
        return "These symptoms warrant medical evaluation. Please contact a healthcare provider. In the meantime, stay hydrated and rest."
    
    elif any(word in message_lower for word in ['xray', 'x-ray', 'radiograph', 'chest']):
        return "Chest X-rays are a common diagnostic tool for lung and chest issues. They can help detect infections like pneumonia, COVID-19, and other conditions. Always consult with a radiologist or doctor for interpretation."
    
    else:
        return "Thank you for your question. I'm an AI assistant trained on medical imaging. For personalized medical advice, please consult a qualified healthcare provider. You can also upload a chest X-ray for AI analysis."

if __name__ == '__main__':
    print("\n" + "="*70)
    print("    🏥 Medical AI Diagnosis Assistant - Flask Backend")
    print("="*70)
    print(f"Model path: {MODEL_PATH}")
    print(f"Model exists: {MODEL_PATH.exists()}")
    print(f"TensorFlow available: {TF_AVAILABLE}")
    print(f"Classes: {CLASS_LABELS}")
    print("="*70)
    print("\nAPI Endpoints:")
    print("  GET  /api/health     - Server health check")
    print("  POST /api/predict    - Upload image for diagnosis")
    print("  POST /api/chat       - Chat with AI assistant")
    print("="*70 + "\n")
    
    # Try to load model on startup
    load_model()
    
    # Run Flask app
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5003,
        use_reloader=False,
        threaded=True
    )
