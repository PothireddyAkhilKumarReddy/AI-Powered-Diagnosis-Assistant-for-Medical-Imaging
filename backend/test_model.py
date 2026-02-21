import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np
from PIL import Image

print("Loading model...")
# Try loading model
MODEL_PATH = 'model.h5'
try:
    print("Direct load...")
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
except Exception as e:
    print("Direct load failed:", e)
    print("Patch load...")
    base_model = tf.keras.applications.DenseNet121(include_top=False, weights=None, input_shape=(224, 224, 3))
    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = base_model(inputs)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    x = tf.keras.layers.Dense(512, activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(4, activation='softmax')(x)
    model = tf.keras.Model(inputs, outputs)
    try:
        model.load_weights(MODEL_PATH, by_name=True, skip_mismatch=True)
    except Exception as patch_e:
        print("Patch load failed:", patch_e)

print(f"Model loaded. Output shape: {model.output_shape}")

print("Predicting...")
img = np.zeros((1, 224, 224, 3), dtype=np.float32)
pred = model.predict(img)
print("Prediction:", pred)
