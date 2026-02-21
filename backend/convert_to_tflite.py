#!/usr/bin/env python3
"""
Convert the trained DenseNet121 model.h5 to TFLite format for low-memory deployment.
Run this LOCALLY (not on Render) since it requires full TensorFlow:
    python convert_to_tflite.py
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
import numpy as np

MODEL_PATH = 'model.h5'
TFLITE_PATH = 'model.tflite'

print("Step 1: Reconstructing model architecture...")
base_model = tf.keras.applications.DenseNet121(
    include_top=False,
    weights=None,
    input_shape=(224, 224, 3)
)

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

print("Step 2: Loading weights...")
try:
    model.load_weights(MODEL_PATH, by_name=True, skip_mismatch=True)
    print("  Weights loaded successfully!")
except Exception as e:
    print(f"  Warning: {e}")
    print("  Trying direct load...")
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    print("  Direct load succeeded!")

print("Step 3: Converting to TFLite...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Use float16 quantization for smaller size while keeping accuracy
converter.target_spec.supported_types = [tf.float16]

tflite_model = converter.convert()

print(f"Step 4: Saving to {TFLITE_PATH}...")
with open(TFLITE_PATH, 'wb') as f:
    f.write(tflite_model)

original_size = os.path.getsize(MODEL_PATH) / (1024 * 1024)
tflite_size = os.path.getsize(TFLITE_PATH) / (1024 * 1024)
print(f"\nDone!")
print(f"  Original model.h5:  {original_size:.1f} MB")
print(f"  Converted model.tflite: {tflite_size:.1f} MB")
print(f"  Size reduction: {((original_size - tflite_size) / original_size * 100):.0f}%")
print(f"\nNow commit model.tflite to your repo and push to GitHub.")
