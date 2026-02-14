#!/usr/bin/env python3
"""
Create a smaller dataset for faster training
Samples a subset of images from each class
"""

import os
import shutil
import random
from pathlib import Path

# Get the base directory (where this script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_small_dataset(samples_per_class=500):
    """Create a smaller dataset with specified samples per class"""
    print(f"Creating small dataset with {samples_per_class} samples per class...")
    
    # Create small dataset directory
    small_dataset_dir = os.path.join(BASE_DIR, 'small_dataset')
    os.makedirs(small_dataset_dir, exist_ok=True)
    
    # Classes to process
    classes = ['Normal', 'Pneumonia', 'COVID-19']
    
    # Define source directories for each class
    # Helper to find existing source directory
    source_mappings = {
        'Normal': [
            os.path.join(BASE_DIR, 'COVID-19_Radiography_Dataset', 'Normal'), 
            os.path.join(BASE_DIR, 'chest_xray', 'train', 'NORMAL')
        ],
        'Pneumonia': [
            os.path.join(BASE_DIR, 'chest_xray', 'train', 'PNEUMONIA'),
            os.path.join(BASE_DIR, 'COVID-19_Radiography_Dataset', 'Viral Pneumonia'),
            os.path.join(BASE_DIR, 'COVID-19_Radiography_Dataset', 'Lung_Opacity')
        ],
        'COVID-19': [
            os.path.join(BASE_DIR, 'COVID-19_Radiography_Dataset', 'COVID')
        ]
    }
    
    for class_name in classes:
        target_dir = f'{small_dataset_dir}/{class_name}'
        os.makedirs(target_dir, exist_ok=True)
        
        # Collect all potential images for this class
        all_potential_images = []
        
        if class_name in source_mappings:
            for source_path in source_mappings[class_name]:
                if os.path.exists(source_path):
                    # Check if images are in a subdirectory (common in some datasets)
                    images_dir = os.path.join(source_path, 'images')
                    if os.path.exists(images_dir):
                        search_dir = images_dir
                    else:
                        search_dir = source_path
                        
                    # Get images
                    for f in os.listdir(search_dir):
                         if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                             all_potential_images.append(os.path.join(search_dir, f))
        
        if not all_potential_images:
            print(f"Warning: No images found for class '{class_name}' in expected locations.")
            continue
            
        # Sample images
        if len(all_potential_images) > samples_per_class:
            selected_files = random.sample(all_potential_images, samples_per_class)
        else:
            selected_files = all_potential_images
        
        # Copy selected files
        for source_path in selected_files:
            filename = os.path.basename(source_path)
            # Handle duplicate filenames by prepending unique prefix if needed
            target_path = os.path.join(target_dir, filename)
            if os.path.exists(target_path):
                base, ext = os.path.splitext(filename)
                target_path = os.path.join(target_dir, f"{base}_{random.randint(1000, 9999)}{ext}")
                
            shutil.copy2(source_path, target_path)
        
        print(f"   {class_name}: {len(selected_files)} images (from {len(all_potential_images)} found)")
    
    # Print summary
    print(f"\nSmall Dataset Summary:")
    total_images = 0
    for class_name in classes:
        class_dir = f'{small_dataset_dir}/{class_name}'
        if os.path.exists(class_dir):
            image_count = len([f for f in os.listdir(class_dir) 
                              if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            print(f"   {class_name}: {image_count} images")
            total_images += image_count
    
    print(f"   Total: {total_images} images")
    print(f"Small dataset created in '{small_dataset_dir}' directory!")

def create_tiny_dataset(samples_per_class=100):
    """Create a very small dataset for quick testing"""
    print(f"Creating tiny dataset with {samples_per_class} samples per class...")
    
    # Create tiny dataset directory
    tiny_dataset_dir = os.path.join(BASE_DIR, 'tiny_dataset')
    os.makedirs(tiny_dataset_dir, exist_ok=True)
    
    # Classes to process
    classes = ['Normal', 'Pneumonia', 'COVID-19']
    
    # Define source directories for each class
    source_mappings = {
        'Normal': [
            os.path.join(BASE_DIR, 'COVID-19_Radiography_Dataset', 'Normal'), 
            os.path.join(BASE_DIR, 'chest_xray', 'train', 'NORMAL')
        ],
        'Pneumonia': [
            os.path.join(BASE_DIR, 'chest_xray', 'train', 'PNEUMONIA'),
            os.path.join(BASE_DIR, 'COVID-19_Radiography_Dataset', 'Viral Pneumonia'),
            os.path.join(BASE_DIR, 'COVID-19_Radiography_Dataset', 'Lung_Opacity')
        ],
        'COVID-19': [
            os.path.join(BASE_DIR, 'COVID-19_Radiography_Dataset', 'COVID')
        ]
    }
    
    for class_name in classes:
        target_dir = f'{tiny_dataset_dir}/{class_name}'
        os.makedirs(target_dir, exist_ok=True)
        
        # Collect all potential images for this class
        all_potential_images = []
        
        if class_name in source_mappings:
            for source_path in source_mappings[class_name]:
                if os.path.exists(source_path):
                    # Check if images are in a subdirectory (common in some datasets)
                    images_dir = os.path.join(source_path, 'images')
                    if os.path.exists(images_dir):
                        search_dir = images_dir
                    else:
                        search_dir = source_path
                        
                    # Get images
                    for f in os.listdir(search_dir):
                         if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                             all_potential_images.append(os.path.join(search_dir, f))
        
        if not all_potential_images:
            print(f"Warning: No images found for class '{class_name}' in expected locations.")
            continue
            
        # Sample images
        if len(all_potential_images) > samples_per_class:
            selected_files = random.sample(all_potential_images, samples_per_class)
        else:
            selected_files = all_potential_images
        
        # Copy selected files
        for source_path in selected_files:
            filename = os.path.basename(source_path)
            # Handle duplicate filenames by prepending unique prefix if needed
            target_path = os.path.join(target_dir, filename)
            if os.path.exists(target_path):
                base, ext = os.path.splitext(filename)
                target_path = os.path.join(target_dir, f"{base}_{random.randint(1000, 9999)}{ext}")
                
            shutil.copy2(source_path, target_path)
        
        print(f"   {class_name}: {len(selected_files)} images (from {len(all_potential_images)} found)")
    
    # Print summary
    print(f"\nTiny Dataset Summary:")
    total_images = 0
    for class_name in classes:
        class_dir = f'{tiny_dataset_dir}/{class_name}'
        if os.path.exists(class_dir):
            image_count = len([f for f in os.listdir(class_dir) 
                              if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            print(f"   {class_name}: {image_count} images")
            total_images += image_count
    
    print(f"   Total: {total_images} images")
    print(f"Tiny dataset created in '{tiny_dataset_dir}' directory!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Create smaller datasets for faster training')
    parser.add_argument('--size', type=str, default='tiny', 
                       choices=['small', 'tiny'],
                       help='Dataset size: small (500 per class) or tiny (100 per class)')
    parser.add_argument('--samples', type=int, default=None,
                       help='Custom number of samples per class')
    
    args = parser.parse_args()
    
    # Set random seed for reproducibility
    random.seed(42)
    
    if args.size == 'small':
        samples = args.samples if args.samples else 500
        create_small_dataset(samples)
    elif args.size == 'tiny':
        samples = args.samples if args.samples else 100
        create_tiny_dataset(samples) 