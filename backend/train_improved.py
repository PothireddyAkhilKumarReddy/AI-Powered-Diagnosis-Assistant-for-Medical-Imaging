#!/usr/bin/env python3
"""
Improved Medical AI Training Script (DenseNet121)
-------------------------------------------------
This script trains a DenseNet121 model, which is widely considered 
state-of-the-art for medical image classification (X-rays).

Key improvements over the previous script:
1. Uses DenseNet121 architecture (better feature reuse).
2. Implements Fine-Tuning (unfreezes top layers of base model).
3. Adds Class Weights to handle unbalanced datasets.
4. Uses slightly more aggressive augmentation.
"""

import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.utils import class_weight
import argparse
import json

# Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

def create_improved_model(num_classes):
    """
    Creates a DenseNet121 based model with fine-tuning enabled.
    """
    print("Building DenseNet121 model...")
    
    # 1. Load the base model with pre-trained ImageNet weights
    base_model = DenseNet121(
        weights='imagenet',
        include_top=False,
        input_shape=IMG_SIZE + (3,)
    )
    
    # 2. Unfreeze the last block of the base model for fine-tuning
    # DenseNet121 has distinct blocks. We unfreeze the last conv block.
    base_model.trainable = True
    
    # Freeze all layers except the last 50 (approx last dense block)
    for layer in base_model.layers[:-50]:
        layer.trainable = False
        
    print(f"Base model has {len(base_model.layers)} layers. Fine-tuning last 50 layers.")

    # 3. Add custom classification head
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    # 4. Compile with a lower learning rate for fine-tuning
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-4), # Lower LR for fine-tuning
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train(data_dir, epochs=30):
    """
    Main training loop.
    """
    # 1. Data Generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2
    )

    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    print(f"Loading data from: {data_dir}")
    
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )

    val_generator = val_datagen.flow_from_directory(
        data_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    classes = list(train_generator.class_indices.keys())
    print(f"Classes found: {classes}")
    
    # 2. Compute Class Weights (to handle imbalance)
    # This helps if you have more 'Normal' images than 'COVID'
    class_weights_vals = class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_generator.classes),
        y=train_generator.classes
    )
    class_weights = dict(enumerate(class_weights_vals))
    print(f"Computed Class Weights: {class_weights}")

    # 3. Create Model
    model = create_improved_model(len(classes))
    model.summary()

    # 4. Callbacks
    callbacks = [
        ModelCheckpoint(
            os.path.join(BASE_DIR, 'best_improved_model.h5'),
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_accuracy',
            patience=8,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1
        )
    ]

    # 5. Train
    print("Starting training...")
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator,
        callbacks=callbacks,
        class_weight=class_weights,
        verbose=1
    )
    
    # 6. Save
    print("Saving final model...")
    model.save(os.path.join(BASE_DIR, 'model.h5')) # Save as standard name for easy deploy
    
    # Save config
    config = {
        'classes': classes,
        'model_type': 'densenet121_finetuned',
        'final_accuracy': float(history.history['accuracy'][-1])
    }
    with open(os.path.join(BASE_DIR, 'model_config.json'), 'w') as f:
        json.dump(config, f)
        
    print("Done! Improved model saved to 'model.h5'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='dataset', help='Path to dataset directory')
    parser.add_argument('--epochs', type=int, default=30)
    args = parser.parse_args()
    
    if os.path.exists(args.data_dir):
        train(args.data_dir, args.epochs)
    else:
        print(f"Error: Data directory '{args.data_dir}' not found.")
