#!/usr/bin/env python3
"""
Medical AI Flask Backend
Trained model: DenseNet121 (3-class: COVID-19, Normal, Pneumonia)
Integrated with Gemini API for enhanced chat capabilities
"""

import os
import sys
import json
import random
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables for Gemini API
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    import google.generativeai as genai
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        print("✓ Gemini API configured")
    else:
        print("⚠️  GEMINI_API_KEY not found in environment")
except ImportError:
    print("⚠️  google-generativeai not installed. Chat features will be limited.")
except Exception as e:
    print(f"⚠️  Gemini API error: {e}")

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_USE_LEGACY_KERAS'] = '1'

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np

# WORKAROUND: Fix for TensorFlow < 2.10 on Windows with newer NumPy
try:
    import tensorflow.python.framework.dtypes
    import tensorflow.python.framework.tensor_util
except ImportError:
    pass

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

def sanitize_filename(filename):
    """Sanitize filename for cross-platform compatibility"""
    # Remove invalid characters for Windows
    import re
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, '_', filename)

# Routes - Static files
@app.route('/')
def index():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except:
        return jsonify({"error": "Frontend not built. Run: npm run build in frontend directory"}), 404

@app.route('/assets/<path:path>')
def serve_assets(path):
    """Serve static assets from dist/assets"""
    try:
        return send_from_directory(os.path.join(app.static_folder, 'assets'), path)
    except:
        return jsonify({"error": f"Asset not found: {path}"}), 404

@app.route('/<path:filename>')
def serve_static(filename):
    try:
        return send_from_directory(app.static_folder, filename)
    except:
        # SPA fallback - serve index.html for client-side routing
        try:
            return send_from_directory(app.static_folder, 'index.html')
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
        "mode": "real" if loaded_model else "mock",
        "gemini_available": GEMINI_API_KEY is not None
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Endpoint to receive an image and return AI-generated diagnosis
    """
    print("DEBUG: /api/predict endpoint called")
    if "image" not in request.files:
        print("DEBUG: No image in request files")
        return jsonify({"success": False, "error": "Please upload a medical image (X-ray, MRI, CT scan) to get a diagnosis."}), 400
    
    file = request.files["image"]
    print(f"DEBUG: Received file: {file.filename}")
    
    # Sanitize filename
    safe_filename = sanitize_filename(file.filename)
    img_path = os.path.join(UPLOADS_DIR, safe_filename)
    file.save(img_path)

    try:
        loaded_model = load_model()
        print(f"DEBUG: Processing image. Model loaded? {loaded_model is not None}")
        
        if TF_AVAILABLE and loaded_model is not None:
            # Use real model prediction
            processed_img = preprocess_image(img_path)
            prediction = loaded_model.predict(processed_img)
            class_idx = np.argmax(prediction[0])
            confidence = float(np.max(prediction[0]))
            
            response = {
                "success": True,
                "prediction": {
                    "class": CLASS_LABELS[class_idx],
                    "confidence": confidence,
                    "description": CLASS_DESCRIPTIONS[CLASS_LABELS[class_idx]],
                    "all_predictions": {
                        CLASS_LABELS[i]: float(prediction[0][i])
                        for i in range(len(CLASS_LABELS))
                    }
                },
                "mode": "real",
                "filename": safe_filename
            }
        else:
            # Mock prediction for testing
            class_idx, confidence = mock_predict()
            response = {
                "success": True,
                "prediction": {
                    "class": CLASS_LABELS[class_idx],
                    "confidence": confidence,
                    "description": CLASS_DESCRIPTIONS[CLASS_LABELS[class_idx]],
                    "all_predictions": {
                        CLASS_LABELS[i]: random.uniform(0, 1)
                        for i in range(len(CLASS_LABELS))
                    }
                },
                "mode": "mock",
                "filename": safe_filename
            }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in /api/predict: {e}")
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500
    finally:
        # Clean up uploaded file
        if os.path.exists(img_path):
            try:
                os.remove(img_path)
            except:
                pass


# Authentication endpoints
users_db = {}  # Mock in-memory user database {email: {password_hash, fullName, phone}}
tokens_db = {}  # Mock token database {token: {email, expiry}}

def hash_password(password):
    """Simple password hashing (use bcrypt in production)"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    """Generate a simple token (use JWT in production)"""
    import uuid
    return str(uuid.uuid4())

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    try:
        data = request.get_json()
        email = data.get('email', '').lower()
        password = data.get('password', '')
        fullName = data.get('fullName', '')
        phone = data.get('phone', '')
        
        # Validation
        if not email or not password or not fullName:
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        if len(password) < 8:
            return jsonify({"success": False, "error": "Password must be at least 8 characters"}), 400
        
        if email in users_db:
            return jsonify({"success": False, "error": "Email already registered"}), 400
        
        # Create user
        import uuid
        user_id = str(uuid.uuid4())
        users_db[email] = {
            "id": user_id,
            "password_hash": hash_password(password),
            "fullName": fullName,
            "phone": phone,
            "email": email
        }
        
        return jsonify({
            "success": True,
            "message": "Account created successfully",
            "user": {
                "id": user_id,
                "email": email,
                "fullName": fullName
            }
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email', '').lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"success": False, "error": "Email and password required"}), 400
        
        if email not in users_db:
            return jsonify({"success": False, "error": "Invalid email or password"}), 401
        
        user = users_db[email]
        if user['password_hash'] != hash_password(password):
            return jsonify({"success": False, "error": "Invalid email or password"}), 401
        
        # Generate token
        import uuid
        from datetime import datetime, timedelta
        token = str(uuid.uuid4())
        tokens_db[token] = {
            "email": email,
            "expiry": (datetime.now() + timedelta(days=7)).isoformat()
        }
        
        return jsonify({
            "success": True,
            "token": token,
            "user": {
                "id": user['id'],
                "email": user['email'],
                "fullName": user['fullName']
            }
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            if token in tokens_db:
                del tokens_db[token]
        
        return jsonify({"success": True, "message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/auth/verify', methods=['GET'])
def verify_auth():
    """Verify authentication token"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        token = auth_header[7:]
        if token not in tokens_db:
            return jsonify({"success": False, "error": "Invalid or expired token"}), 401
        
        token_data = tokens_db[token]
        email = token_data['email']
        user = users_db.get(email)
        
        if not user:
            del tokens_db[token]
            return jsonify({"success": False, "error": "User not found"}), 401
        
        return jsonify({
            "success": True,
            "user": {
                "id": user['id'],
                "email": user['email'],
                "fullName": user['fullName']
            }
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Chat endpoint
@app.route("/api/chat", methods=["POST"])
def chat():
    """Chat endpoint with optional Gemini integration"""
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return jsonify({"success": False, "error": "Message is required"}), 400
        
        # Try to use Gemini if available
        if GEMINI_API_KEY:
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(user_message)
                ai_response = response.text
                return jsonify({
                    "success": True,
                    "response": ai_response,
                    "message": user_message
                }), 200
            except Exception as e:
                print(f"Gemini API error: {e}")
                # Fall back to keyword-based responses
        
        # Fallback: keyword-based responses
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['covid', 'coronavirus']):
            response = "COVID-19 is a viral infection. If you test positive, consult your healthcare provider. Wear masks, maintain distance, and follow local health guidelines."
        elif any(word in message_lower for word in ['pneumonia', 'lung']):
            response = "Pneumonia is a lung infection that can be serious. Seek medical attention if you experience persistent cough, fever, or difficulty breathing."
        elif any(word in message_lower for word in ['fever', 'temperature']):
            response = "A fever is your body's natural response to infection. Rest, stay hydrated, and monitor your temperature. Seek medical help if fever persists above 103°F (39.4°C)."
        elif any(word in message_lower for word in ['vaccine', 'vaccination']):
            response = "Vaccines are safe and effective. Consult your doctor about which vaccines are appropriate for you."
        elif any(word in message_lower for word in ['mask', 'prevention']):
            response = "Prevention measures include: wearing masks in crowded areas, washing hands frequently, maintaining distance from sick people, and staying updated with vaccinations."
        else:
            response = "I'm an AI health assistant. Please ask about symptoms, prevention, or common health conditions. For serious concerns, always consult a healthcare professional."
        
        return jsonify({
            "success": True,
            "response": response,
            "message": user_message
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    # Ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)
    # Run the Flask app
    print("Starting Medical AI Bot...")
    print("Frontend will be available at: http://localhost:5003")
    print("API endpoints:")
    print("   - POST /api/predict - Upload medical images for diagnosis")
    print("   - POST /api/chat - Chat with the AI")
    print("   - POST /api/auth/signup - Register new user")
    print("   - POST /api/auth/login - Login user")
    app.run(debug=True, host='0.0.0.0', port=5003)
