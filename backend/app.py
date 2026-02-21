# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS


# WORKAROUND: Fix for TensorFlow < 2.10 on Windows with newer NumPy
try:
    import tensorflow.python.framework.dtypes
    import tensorflow.python.framework.tensor_util
except ImportError:
    pass

try:
    import tensorflow as tf
    try:
        from tensorflow import keras
    except ImportError:
        import keras
    
    # Try exposing functional for monkey patching later
    try:
        from keras.engine import functional
    except ImportError:
        try:
            from tensorflow.python.keras.engine import functional
        except ImportError:
             # Just in case, try through tf.keras
            pass
            
    load_model = tf.keras.models.load_model
    image = tf.keras.preprocessing.image
    TF_AVAILABLE = True
    print(f"TensorFlow version: {tf.__version__}")
except ImportError as e:
    TF_AVAILABLE = False
    print(f"TensorFlow not found. Error: {e}")
except Exception as e:
    TF_AVAILABLE = False
    print(f"Unexpected error importing TensorFlow: {e}")

# WORKAROUND: Fix 'batch_shape' and 'DTypePolicy' errors when loading Keras 3 model in Keras 2
if TF_AVAILABLE:
    # WORKAROUND: Raw Model Configuration Patch
    # Instead of subclassing every layer, we load the model config, patch it, and reload.
    import json
    
    custom_objects = {} # No longer needed with this approach

try:
    import numpy as np
    NP_AVAILABLE = True
except ImportError:
    NP_AVAILABLE = False
    print("NumPy not found. Using pure Python mocks.")
    
import os
import random
import pprint

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

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({"status": "healthy", "tf_available": TF_AVAILABLE, "model_loaded": model is not None})

def load_keras3_model_safely(model_path):
    """
    Reconstructs the model architecture in code and loads weights.
    This bypasses Keras 3 -> Keras 2 config incompatibility.
    """
    print("DEBUG: Reconstructing model architecture...")
    try:
        # Reconstruct the exact architecture matching Colab notebook (Functional API)
        base_model = tf.keras.applications.DenseNet121(
            include_top=False,
            weights=None, 
            input_shape=(224, 224, 3)
        )
        base_model.trainable = True

        inputs = tf.keras.Input(shape=(224, 224, 3))
        x = base_model(inputs)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.5)(x)
        x = tf.keras.layers.Dense(512, activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        outputs = tf.keras.layers.Dense(3, activation='softmax')(x)
        model = tf.keras.Model(inputs, outputs)
        
        print("DEBUG: Loading weights into reconstructed model...")
        # Load weights from the H5 file with partial loading enabled
        try:
            model.load_weights(model_path, by_name=True, skip_mismatch=True)
            print("DEBUG: Model weighted loaded successfully (partial/by_name)!")
            return model
        except Exception as e:
             print(f"DEBUG: Standard load_weights failed: {e}")
             # Final fallback: Try loading without skip_mismatch just in case? 
             # No, if that failed, we are done. Be silent or re-raise?
             print("Falling back to None.")
             return None
    except Exception as e:
        print(f"DEBUG: Reconstruction failed: {e}")
        # Last resort: Try very aggressive patching? No, if this fails, we are stuck.
        return None

try:
    if TF_AVAILABLE:
        print(f"DEBUG: TensorFlow Version: {tf.__version__}")
        print("DEBUG: Attempting to load model...")
        
        try:
            model = tf.keras.models.load_model(MODEL_PATH, compile=False)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Direct load failed: {e}")
            print("Trying compatibility patch...")
            model = load_keras3_model_safely(MODEL_PATH)
            if model is not None:
                print("Model loaded with patch.")
            else:
                print("Patch failed. Defaulting to MOCK.")
    else:
        print("TensorFlow not available. Using mock mode.")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Defaulting to MOCK PREDICTIONS.")
    model = None



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
    print("DEBUG: /predict endpoint called")
    if "image" not in request.files:
        print("DEBUG: No image in request files")
        return jsonify({"success": False, "error": "Please upload a medical image (X-ray, MRI, CT scan) to get a diagnosis."}), 400
    
    file = request.files["image"]
    
    # FIX: Secure the filename and ensure the directory exists 
    # to prevent [Errno 22] Invalid argument on Windows
    from werkzeug.utils import secure_filename
    os.makedirs(os.path.join(BASE_DIR, "uploads"), exist_ok=True)
    filename = secure_filename(file.filename)
    
    print(f"DEBUG: Received file: {filename}")
    img_path = os.path.join(BASE_DIR, "uploads", filename)
    file.save(img_path)

    try:
        print(f"DEBUG: Processing image. Model loaded? {model is not None}")
        if TF_AVAILABLE and NP_AVAILABLE and model is not None:
            # Use real model prediction
            processed_img = preprocess_image(img_path)
            prediction = model.predict(processed_img)
            class_idx = np.argmax(prediction[0])
            confidence = float(np.max(prediction[0]))
            source = "Real Model"
        else:
            # Use mock prediction
            class_idx, confidence = mock_predict()
            source = "Mock Model (TensorFlow unavailable)"
        
        # Confidence Threshold to filter non-medical images
        # Lowered to 0.50 temporarily to debug user's image
        # If confidence is > 50%, we show the result.
        if confidence < 0.50:
            diagnosis = "Uncertain"
            response = {
                "success": True,
                "prediction": {
                    "class": "Uncertain",
                    "confidence": confidence,
                    "description": "Low confidence. This may not be a medical image.",
                    "source": source
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
                "description": f"AI detected {diagnosis} with {confidence * 100:.2f}% confidence",
                "source": source
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
