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
    
    def patch_model_config(model_path):
        """
        Manually reads the H5 file, extracts the definition, patches incompatible names,
        and returns a model from the patched config.
        """
        import h5py
        from tensorflow.keras.models import model_from_config
        import pprint
        
        print("DEBUG: Starting patch_model_config...")
        
        with h5py.File(model_path, 'r') as f:
            if 'model_config' not in f.attrs:
                raise ValueError("No model_config found in h5 file")
            config_str = f.attrs['model_config']
            
        print("DEBUG: Model config loaded from H5.")
            
        # Parse config JSON
        if isinstance(config_str, bytes):
            config_str = config_str.decode('utf-8')
        config = json.loads(config_str)
        
        # Recursive patch function
        def patch_config(item):
            if isinstance(item, dict):
                # Debug logging for layers
                if "class_name" in item:
                   # print(f"DEBUG: Patching layer {item['class_name']}")
                   pass

                # Fix batch_shape -> batch_input_shape
                if "batch_shape" in item:
                    item["batch_input_shape"] = item.pop("batch_shape")
                # Remove dtype policies
                if "dtype" in item and isinstance(item["dtype"], dict):
                    item.pop("dtype")
                    
                # FIX: Keras 3 inbound_nodes (flat lists) vs Keras 2 (list of lists)
                if "inbound_nodes" in item:
                    inbound_nodes = item["inbound_nodes"]
                    
                    # LOGGING: Print what we found
                    if inbound_nodes and isinstance(inbound_nodes, list) and len(inbound_nodes) > 0:
                        # Only log if it looks suspicious (flat list) or just for the first non-empty one
                        # print(f"DEBUG: Found inbound_nodes: {inbound_nodes}")
                        pass

                    # Check if it's the new format and needs wrapping
                    if isinstance(inbound_nodes, list):
                        new_nodes = []
                        for node in inbound_nodes:
                            # Case 1: Node is a bare string (unexpected but possible in some formats)
                            if isinstance(node, str):
                                print(f"DEBUG: Wrapping bare string node: {node}")
                                new_nodes.append([node, 0, 0, {}])
                            # Case 2: Node is a flat list ['layer_name', 0, ...] - Keras 3 style
                            elif isinstance(node, list) and len(node) > 0 and isinstance(node[0], str):
                                # print(f"DEBUG: Wrapping flat list node: {node}")
                                new_nodes.append([node])
                            # Case 3: Already correct [[...]] (Keras 2 style) or empty
                            else:
                                new_nodes.append(node)
                        item["inbound_nodes"] = new_nodes

                # Recursive call for all values
                for key, value in item.items():
                    patch_config(value)
            elif isinstance(item, list):
                for element in item:
                    patch_config(element)
                    
        # Apply patch to the entire config tree
        patch_config(config)
        
        # DEBUG: Dump the config to logs so we can see the structure
        print("DEBUG: DUMPING PATCHED CONFIG (Partial):")
        try:
            # Print first layer's inbound nodes to see if we fixed it
            for layer in config.get('config', {}).get('layers', []):
                if layer.get('inbound_nodes'):
                    print(f"Layer {layer.get('name')} inbound_nodes: {layer['inbound_nodes']}")
        except Exception as e:
            print(f"DEBUG: Could not dump config: {e}")

        # Reconstruct model from patched config
        print("DEBUG: Reconstructing model from config...")
        model = model_from_config(config)
        print("DEBUG: Model reconstructed.")
        
        # Load weights
        print("DEBUG: Loading weights...")
        model.load_weights(model_path)
        print("DEBUG: Weights loaded.")
        
        return model
    
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

# Load pre-trained model or use mock model
model = None
try:
    if TF_AVAILABLE:
        print("DEBUG: Attempting to load model...")
        model = patch_model_config(MODEL_PATH)
        print("Model loaded successfully!")
    else:
        print("Skipping model load because TensorFlow is not available.")
except FileNotFoundError:
    print(f"Model file '{MODEL_PATH}' not found. Using mock predictions.")
except Exception as e:
    import traceback
    print(f"Error loading model: {e}. Defaulting to MOCK PREDICTIONS.")
    print("Full traceback:")
    traceback.print_exc()


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
    print(f"DEBUG: Received file: {file.filename}")
    img_path = os.path.join("uploads", file.filename)
    file.save(img_path)

    try:
        print(f"DEBUG: Processing image. Model loaded? {model is not None}")
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
