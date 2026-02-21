#!/usr/bin/env python
# app_simple.py - Simplified Flask backend without TensorFlow (for now)
import os
import sys
import random
import json
import hashlib
import uuid
import re
import logging
from pathlib import Path
from datetime import datetime, timedelta
from functools import wraps
from collections import defaultdict

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

try:
    from flask import Flask, request, jsonify, send_from_directory  # type: ignore
    from flask_cors import CORS  # type: ignore
    print("✓ Flask loaded successfully")
except ImportError as e:
    print(f"✗ Flask not available: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Don't use static_folder so we can handle all routing manually
app = Flask(__name__)

# Configure CORS with specific origins
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5003", "http://127.0.0.1:5003"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.h5')

# Configuration
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Mock predictions
labels = ["COVID-19", "Normal", "Pneumonia"]

# In-memory user database (mock)
users_db = {}
tokens_db = {}

# Rate limiting tracking (in-memory)
rate_limit_db = defaultdict(lambda: defaultdict(list))

# Validation functions
def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        return False, "Password must contain at least one special character"
    return True, "Password is strong"

def is_valid_phone(phone):
    """Validate phone number format (simple check)"""
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')) is not None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_filename(filename):
    """Sanitize filename to prevent path traversal attacks"""
    # Remove path separators and special characters
    filename = os.path.basename(filename)
    # Remove potentially dangerous characters
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit filename length
    name, ext = os.path.splitext(filename)
    if len(name) > 50:
        name = name[:50]
    return name + ext if ext else name

def check_rate_limit(ip_address, endpoint, limit_per_hour=50):
    """Check if request exceeds rate limit"""
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    
    # Clean old requests
    rate_limit_db[endpoint][ip_address] = [
        req_time for req_time in rate_limit_db[endpoint][ip_address]
        if req_time > one_hour_ago
    ]
    
    # Check limit
    if len(rate_limit_db[endpoint][ip_address]) >= limit_per_hour:
        return False
    
    # Record this request
    rate_limit_db[endpoint][ip_address].append(now)
    return True

def rate_limit(endpoint_name, limit_per_hour=50):
    """Decorator for rate limiting"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            if not check_rate_limit(ip, endpoint_name, limit_per_hour):
                logger.warning(f"Rate limit exceeded for {ip} on {endpoint_name}")
                return jsonify({
                    "success": False,
                    "error": "Rate limit exceeded. Try again later.",
                    "code": "RATE_LIMIT_EXCEEDED"
                }), 429
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def hash_password(password):
    """Hash password (use bcrypt in production)"""
    # Salt is important for security
    salt = "medical_ai_default_salt_v1"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def generate_token():
    """Generate a secure auth token"""
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

@app.route('/api/health')
def health():
    """Health check endpoint"""
    try:
        return jsonify({
            "status": "healthy",
            "tensorflow_available": False,
            "model_loaded": False,
            "classes": labels,
            "mode": "mock",
            "message": "Running in mock mode (TensorFlow unavailable on macOS)",
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error in health endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route('/api/predict', methods=['POST'])
@rate_limit('predict', limit_per_hour=20)
def predict():
    """Handle image upload and prediction"""
    try:
        if 'image' not in request.files:
            logger.warning("No image provided in request")
            return jsonify({
                "success": False,
                "error": "No image provided",
                "code": "NO_IMAGE"
            }), 400
        
        file = request.files['image']
        
        if file.filename == '':
            logger.warning("Empty filename provided")
            return jsonify({
                "success": False,
                "error": "No file selected",
                "code": "NO_FILE_SELECTED"
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            logger.warning(f"Invalid file type: {file.filename}")
            return jsonify({
                "success": False,
                "error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
                "code": "INVALID_FILE_TYPE"
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_UPLOAD_SIZE:
            logger.warning(f"File too large: {file_size} bytes")
            return jsonify({
                "success": False,
                "error": f"File too large. Maximum size: {MAX_UPLOAD_SIZE / 1024 / 1024:.1f}MB",
                "code": "FILE_TOO_LARGE"
            }), 413
        
        # Create uploads directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Sanitize filename
        safe_filename = sanitize_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        safe_filename = timestamp + safe_filename
        
        img_path = os.path.join(UPLOAD_FOLDER, safe_filename)
        file.save(img_path)
        logger.info(f"Saved uploaded file: {safe_filename}")
        
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
            "filename": safe_filename
        }
        
        logger.info(f"Prediction successful: {diagnosis} ({confidence:.2%})")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "An error occurred while processing the image",
            "code": "PROCESSING_ERROR"
        }), 500

@app.route("/api/chat", methods=["POST"])
@rate_limit('chat', limit_per_hour=100)
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        if not data:
            logger.warning("No JSON data in chat request")
            return jsonify({
                "success": False,
                "error": "Invalid request body",
                "code": "INVALID_REQUEST"
            }), 400
        
        user_message = data.get("message", "").strip()
        
        if not user_message:
            logger.warning("Empty message in chat request")
            return jsonify({
                "success": False,
                "error": "Message cannot be empty",
                "code": "EMPTY_MESSAGE"
            }), 400
        
        if len(user_message) > 5000:
            logger.warning(f"Message too long: {len(user_message)} characters")
            return jsonify({
                "success": False,
                "error": "Message too long (max 5000 characters)",
                "code": "MESSAGE_TOO_LONG"
            }), 413
        
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
                logger.info(f"Chat response matched keyword: {keyword}")
                break
        
        return jsonify({
            "success": True,
            "response": response_text,
            "message": user_message
        }), 200
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "An error occurred while processing your message",
            "code": "PROCESSING_ERROR"
        }), 500

@app.route("/api/auth/signup", methods=["POST"])
@rate_limit('signup', limit_per_hour=50)
def signup():
    """Handle user signup with comprehensive validation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Invalid request body",
                "code": "INVALID_REQUEST"
            }), 400
        
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        full_name = data.get("fullName", "").strip()
        phone = data.get("phone", "").strip()
        
        # Validation
        if not email or not password or not full_name:
            logger.warning(f"Missing required fields in signup: email={bool(email)}, password={bool(password)}, fullName={bool(full_name)}")
            return jsonify({
                "success": False,
                "message": "Email, password, and full name are required",
                "code": "MISSING_FIELDS"
            }), 400
        
        # Email validation
        if not is_valid_email(email):
            logger.warning(f"Invalid email format: {email}")
            return jsonify({
                "success": False,
                "message": "Invalid email format",
                "code": "INVALID_EMAIL"
            }), 400
        
        # Check if email already exists
        if email in users_db:
            logger.warning(f"Signup attempt with existing email: {email}")
            return jsonify({
                "success": False,
                "message": "Email already registered. Please login instead.",
                "code": "EMAIL_ALREADY_EXISTS"
            }), 409
        
        # Password strength validation
        is_strong, message = is_strong_password(password)
        if not is_strong:
            logger.warning(f"Weak password in signup: {message}")
            return jsonify({
                "success": False,
                "message": f"Password requirement: {message}",
                "code": "WEAK_PASSWORD"
            }), 400
        
        # Phone validation (optional)
        if phone and not is_valid_phone(phone):
            logger.warning(f"Invalid phone format: {phone}")
            return jsonify({
                "success": False,
                "message": "Invalid phone number format",
                "code": "INVALID_PHONE"
            }), 400
        
        # Name validation (alphanumeric and spaces only)
        if not re.match(r'^[a-zA-Z\s]+$', full_name):
            logger.warning(f"Invalid full name format: {full_name}")
            return jsonify({
                "success": False,
                "message": "Full name should only contain letters and spaces",
                "code": "INVALID_NAME"
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
        
        logger.info(f"New user registered: {email}")
        
        return jsonify({
            "success": True,
            "message": "Account created successfully. Please login.",
            "code": "SIGNUP_SUCCESS",
            "user": {
                "id": user_id,
                "email": email,
                "fullName": full_name
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Error in signup endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "An error occurred during signup",
            "code": "SERVER_ERROR"
        }), 500

@app.route("/api/auth/login", methods=["POST"])
@rate_limit('login', limit_per_hour=50)
def login():
    """Handle user login with enhanced security"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Invalid request body",
                "code": "INVALID_REQUEST"
            }), 400
        
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        
        if not email or not password:
            logger.warning(f"Login attempt with missing credentials: email={bool(email)}, password={bool(password)}")
            return jsonify({
                "success": False,
                "message": "Email and password are required",
                "code": "MISSING_FIELDS"
            }), 400
        
        # Check if user exists
        if email not in users_db:
            logger.warning(f"Login attempt with non-existent email: {email}")
            return jsonify({
                "success": False,
                "message": "Invalid email or password",
                "code": "INVALID_CREDENTIALS"
            }), 401
        
        user = users_db[email]
        
        # Verify password
        if user["password"] != hash_password(password):
            logger.warning(f"Failed login attempt for email: {email}")
            return jsonify({
                "success": False,
                "message": "Invalid email or password",
                "code": "INVALID_CREDENTIALS"
            }), 401
        
        # Generate token
        token = generate_token()
        tokens_db[token] = {
            "email": email,
            "user_id": user["id"],
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(days=7)
        }
        
        logger.info(f"Successful login for email: {email}")
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "code": "LOGIN_SUCCESS",
            "token": token,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "fullName": user["fullName"]
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in login endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "An error occurred during login",
            "code": "SERVER_ERROR"
        }), 500

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    """Handle user logout"""
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        
        if not token:
            logger.warning("Logout attempt without token")
            return jsonify({
                "success": False,
                "message": "No token provided",
                "code": "NO_TOKEN"
            }), 400
        
        if token in tokens_db:
            del tokens_db[token]
            logger.info("User logged out successfully")
        
        return jsonify({
            "success": True,
            "message": "Logged out successfully",
            "code": "LOGOUT_SUCCESS"
        }), 200
        
    except Exception as e:
        logger.error(f"Error in logout endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "An error occurred during logout",
            "code": "SERVER_ERROR"
        }), 500

@app.route("/api/auth/verify", methods=["GET"])
def verify_auth():
    """Verify if user is authenticated"""
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        
        if not token:
            logger.debug("Auth verification attempt without token")
            return jsonify({
                "success": False,
                "message": "Not authenticated",
                "code": "NO_TOKEN"
            }), 401
        
        if token not in tokens_db:
            logger.warning(f"Verification attempt with invalid token")
            return jsonify({
                "success": False,
                "message": "Invalid token",
                "code": "INVALID_TOKEN"
            }), 401
        
        token_data = tokens_db[token]
        
        # Check if token is expired
        if token_data["expires_at"] < datetime.now():
            del tokens_db[token]
            logger.info(f"Token expired for user: {token_data.get('email')}")
            return jsonify({
                "success": False,
                "message": "Token expired",
                "code": "TOKEN_EXPIRED"
            }), 401
        
        user_email = token_data.get("email")
        user = users_db.get(user_email, {})
        
        logger.debug(f"Token verified for user: {user_email}")
        
        return jsonify({
            "success": True,
            "message": "Token is valid",
            "code": "TOKEN_VALID",
            "user": {
                "id": user.get("id"),
                "email": user.get("email"),
                "fullName": user.get("fullName")
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in verify endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "An error occurred during verification",
            "code": "SERVER_ERROR"
        }), 500

@app.route('/')
def serve_index():
    """Serve index.html for SPA routing"""
    try:
        return send_from_directory(os.path.join(BASE_DIR, '../frontend/dist'), 'index.html')
    except Exception as e:
        logger.error(f"Error serving index: {str(e)}", exc_info=True)
        return jsonify({"error": "Unable to serve frontend"}), 500

@app.route('/assets/<path:path>')
def serve_assets(path):
    """Serve static assets"""
    try:
        return send_from_directory(os.path.join(BASE_DIR, '../frontend/dist/assets'), path)
    except Exception as e:
        logger.error(f"Error serving asset {path}: {str(e)}", exc_info=True)
        return jsonify({"error": "Asset not found"}), 404

@app.route('/<path:path>')
def serve_static_or_index(path):
    """Serve static files or index.html for SPA routing"""
    try:
        # Try to serve as a static file first
        dist_dir = os.path.join(BASE_DIR, '../frontend/dist')
        file_path = os.path.join(dist_dir, path)
        
        if os.path.isfile(file_path):
            return send_from_directory(dist_dir, path)
        
        # Otherwise serve index.html for client-side routing
        return send_from_directory(dist_dir, 'index.html')
    except Exception as e:
        logger.error(f"Error serving static for {path}: {str(e)}", exc_info=True)
        return jsonify({"error": "File not found", "path": path}), 404

# Global error handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request"""
    logger.warning(f"Bad request: {error}")
    return jsonify({
        "success": False,
        "error": "Bad request",
        "code": "BAD_REQUEST"
    }), 400

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "code": "NOT_FOUND"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed"""
    logger.warning(f"Method not allowed: {error}")
    return jsonify({
        "success": False,
        "error": "Method not allowed",
        "code": "METHOD_NOT_ALLOWED"
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 Internal Server Error"""
    logger.error(f"Internal server error: {error}", exc_info=True)
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "code": "SERVER_ERROR"
    }), 500

if __name__ == "__main__":
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        logger.info(f"Upload folder ready: {UPLOAD_FOLDER}")
        
        print("\n" + "="*70)
        print("🏥 Medical AI Diagnosis Assistant - Mock Backend (macOS)")
        print("="*70)
        print("⚠️  Running in MOCK MODE")
        print("Reason: TensorFlow segmentation fault on macOS")
        print("\n✅ Features available:")
        print("   • Frontend: http://localhost:5003")
        print("   • Health Check: GET /api/health")
        print("   • Predict: POST /api/predict")
        print("   • Chat: POST /api/chat")
        print("   • Auth: POST /api/auth/signup, /api/auth/login, /api/auth/logout")
        print("   • Verify: GET /api/auth/verify")
        print("\n🔒 Security Features:")
        print("   • Email validation with regex")
        print("   • Strong password validation")
        print("   • File type & size validation")
        print("   • Filename sanitization")
        print("   • Rate limiting on endpoints")
        print("   • CORS configured")
        print("   • Comprehensive error handling")
        print("   • Request logging & debugging")
        print("\n📝 Configuration:")
        print(f"   • Max upload size: {MAX_UPLOAD_SIZE / 1024 / 1024:.1f}MB")
        print(f"   • Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}")
        print(f"   • Token expiry: 7 days")
        print("   • Rate limits: auth=50/hr, predict=20/hr, chat=100/hr")
        print("\n📋 Deployment:")
        print("         Deploy to Linux for real TensorFlow model inference")
        print("="*70 + "\n")
        
        logger.info("Starting Flask application on http://0.0.0.0:5003")
        app.run(debug=False, host='0.0.0.0', port=5003, use_reloader=False)
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        print("\n✓ Server shutdown cleanly\n")
    except Exception as e:
        logger.critical(f"Fatal error starting server: {str(e)}", exc_info=True)
        print(f"\n✗ Error: {str(e)}\n")
        sys.exit(1)
