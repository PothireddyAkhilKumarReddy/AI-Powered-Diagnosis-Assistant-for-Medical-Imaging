#!/usr/bin/env python
# app_simple.py - Simplified Flask backend without TensorFlow (for now)
import os
import sys
import random
import json
import hashlib
import uuid
from pathlib import Path
from datetime import datetime, timedelta

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

try:
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS
    print("✓ Flask loaded successfully")
except ImportError as e:
    print(f"✗ Flask not available: {e}")
    sys.exit(1)

# Don't use static_folder so we can handle all routing manually
app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.h5')

# Mock predictions
labels = ["COVID-19", "Normal", "Pneumonia"]

# In-memory user database (mock)
users_db = {}
tokens_db = {}

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    """Generate a mock auth token"""
    return str(uuid.uuid4())

def verify_token(token):
    """Verify if a token is valid"""
    return token in tokens_db

def mock_predict():
    """Generate mock predictions for testing"""
    class_idx = random.randint(0, 2)
    confidence = random.uniform(0.75, 0.95)
    return class_idx, confidence

# Routes

def mock_predict():
    """Generate mock predictions for testing"""
    class_idx = random.randint(0, 2)
    confidence = random.uniform(0.75, 0.95)
    return class_idx, confidence

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "tensorflow_available": False,
        "model_loaded": False,
        "classes": labels,
        "mode": "mock",
        "message": "Running in mock mode (TensorFlow unavailable on macOS)"
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image provided"}), 400
    
    file = request.files['image']
    print(f"Received file: {file.filename}")
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    img_path = os.path.join("uploads", file.filename)
    file.save(img_path)
    
    try:
        # Use mock prediction
        class_idx = random.randint(0, 2)
        confidence = random.uniform(0.75, 0.95)
        diagnosis = labels[class_idx]
        
        # Generate confidence scores for all classes
        all_scores = [random.uniform(0.01, 0.3) for _ in labels]
        all_scores[class_idx] = confidence
        # Normalize to sum to 1
        total = sum(all_scores)
        all_scores = [s / total for s in all_scores]
        
        description_map = {
            "COVID-19": "Signs of pneumonia detected. Seek immediate medical attention and follow isolation protocols.",
            "Normal": "No significant findings detected. Results appear normal.",
            "Pneumonia": "Signs of infection detected. Consult with a healthcare provider for treatment."
        }
        
        response = {
            "success": True,
            "prediction": {
                "class": diagnosis,
                "confidence": float(confidence),
                "description": description_map.get(diagnosis, ""),
                "all_predictions": {
                    label: float(score) for label, score in zip(labels, all_scores)
                }
            },
            "mode": "mock",
            "filename": file.filename
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"success": False, "error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Simple keyword-based responses
    responses = {
        "covid": "COVID-19 is a respiratory illness. If you suspect infection, consult a healthcare professional immediately.",
        "pneumonia": "Pneumonia is a lung infection that requires medical attention. Please seek care if you have symptoms.",
        "normal": "Normal results indicate no significant findings. Continue monitoring your health.",
        "symptoms": "Please describe your symptoms and consult with a healthcare professional for proper diagnosis.",
        "treatment": "Treatment depends on the diagnosis. Always consult with your doctor for personalized medical advice.",
        "help": "I'm here to help analyze chest X-rays and answer health questions. Upload an image or ask a question."
    }
    
    # Check for keywords in the message
    response_text = "Thank you for your question. For medical concerns, please consult with a healthcare professional."
    user_lower = user_message.lower()
    for keyword, response in responses.items():
        if keyword in user_lower:
            response_text = response
            break
    
    return jsonify({
        "success": True,
        "response": response_text,
        "message": user_message
    })

@app.route("/api/auth/signup", methods=["POST"])
def signup():
    """Handle user signup"""
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    full_name = data.get("fullName", "")
    phone = data.get("phone", "")
    
    # Validation
    if not email or not password or not full_name:
        return jsonify({
            "success": False,
            "message": "Email, password, and full name are required"
        }), 400
    
    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters"
        }), 400
    
    if email in users_db:
        return jsonify({
            "success": False,
            "message": "Email already registered"
        }), 400
    
    # Create user
    user_id = str(uuid.uuid4())
    users_db[email] = {
        "id": user_id,
        "email": email,
        "fullName": full_name,
        "phone": phone,
        "password": hash_password(password),
        "created_at": datetime.now().isoformat()
    }
    
    return jsonify({
        "success": True,
        "message": "Account created successfully. Please login.",
        "user": {
            "id": user_id,
            "email": email,
            "fullName": full_name
        }
    }), 201

@app.route("/api/auth/login", methods=["POST"])
def login():
    """Handle user login"""
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    
    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400
    
    # Check if user exists
    if email not in users_db:
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401
    
    user = users_db[email]
    
    # Verify password
    if user["password"] != hash_password(password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401
    
    # Generate token
    token = generate_token()
    tokens_db[token] = {
        "email": email,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(days=7)
    }
    
    return jsonify({
        "success": True,
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "fullName": user["fullName"]
        }
    }), 200

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    """Handle user logout"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    if token in tokens_db:
        del tokens_db[token]
    
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200

@app.route("/api/auth/verify", methods=["GET"])
def verify_auth():
    """Verify if user is authenticated"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    if not token or token not in tokens_db:
        return jsonify({
            "success": False,
            "message": "Not authenticated"
        }), 401
    
    token_data = tokens_db[token]
    
    # Check if token is expired
    if token_data["expires_at"] < datetime.now():
        del tokens_db[token]
        return jsonify({
            "success": False,
            "message": "Token expired"
        }), 401
    
    user = users_db.get(token_data["email"], {})
    
    return jsonify({
        "success": True,
        "message": "Token is valid",
        "user": {
            "id": user.get("id"),
            "email": user.get("email"),
            "fullName": user.get("fullName")
        }
    }), 200

@app.route('/')
def serve_index():
    """Serve index.html for SPA routing"""
    return send_from_directory(os.path.join(BASE_DIR, '../frontend/dist'), 'index.html')

@app.route('/assets/<path:path>')
def serve_assets(path):
    """Serve static assets"""
    return send_from_directory(os.path.join(BASE_DIR, '../frontend/dist/assets'), path)

@app.route('/<path:path>')
def serve_static_or_index(path):
    """Serve static files or index.html for SPA routing"""
    # Try to serve as a static file first
    dist_dir = os.path.join(BASE_DIR, '../frontend/dist')
    file_path = os.path.join(dist_dir, path)
    
    if os.path.isfile(file_path):
        return send_from_directory(dist_dir, path)
    
    # Otherwise serve index.html for client-side routing
    return send_from_directory(dist_dir, 'index.html')

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    print("\n" + "="*70)
    print("🏥 Medical AI Diagnosis Assistant - Mock Backend (macOS)")
    print("="*70)
    print("⚠️  Running in MOCK MODE")
    print("Reason: TensorFlow segmentation fault on macOS")
    print("\n✅ Features available:")
    print("   • Frontend: http://localhost:5003")
    print("   • API (Predict): POST /api/predict")
    print("   • API (Chat): POST /api/chat")
    print("   • Health Check: GET /api/health")
    print("   • Auth (Signup): POST /api/auth/signup")
    print("   • Auth (Login): POST /api/auth/login")
    print("   • Auth (Logout): POST /api/auth/logout")
    print("   • Auth (Verify): GET /api/auth/verify")
    print("\n📝 Note: This mock backend generates random predictions for testing")
    print("         Deploy to Linux for real model inference")
    print("="*70 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5003, use_reloader=False)
