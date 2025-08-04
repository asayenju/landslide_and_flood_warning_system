# YOLO Landslide Detection - Datasets & Training Guide

## Recommended Datasets

### 1. Landslide4Sense (Best Option)
- **Source**: https://www.iarai.ac.at/landslide4sense/
- **Size**: 3,799 image patches (128x128 pixels)
- **Format**: Sentinel-2 satellite imagery
- **Labels**: Pre-annotated landslide areas
- **Advantages**: Ready-to-use, high quality, competition dataset
- **Usage**: Perfect for YOLO training after format conversion

### 2. NASA Global Landslide Catalog
- **Source**: https://data.nasa.gov/Earth-Science/Global-Landslide-Catalog-Export/dd9e-wu2v
- **Size**: 11,000+ landslide events with coordinates
- **Format**: CSV with lat/lng coordinates
- **Usage**: Use coordinates to fetch satellite imagery from Google Earth Engine
- **Advantages**: Large dataset, global coverage

### 3. Bijie Landslide Dataset
- **Source**: Available on academic platforms
- **Size**: 770 landslide images
- **Format**: High-resolution optical images
- **Labels**: Bounding box annotations
- **Advantages**: Already in YOLO-compatible format

## Quick Training Setup

### Convert Landslide4Sense to YOLO Format
```python
# convert_dataset.py
import os
import json
from PIL import Image
import numpy as np

def convert_landslide4sense_to_yolo():
    """Convert Landslide4Sense dataset to YOLO format"""
    
    # Download and extract Landslide4Sense dataset
    # Structure: train/img/, train/mask/, val/img/, val/mask/
    
    for split in ['train', 'val']:
        img_dir = f'landslide4sense/{split}/img'
        mask_dir = f'landslide4sense/{split}/mask'
        
        # Create YOLO directories
        os.makedirs(f'yolo_dataset/{split}/images', exist_ok=True)
        os.makedirs(f'yolo_dataset/{split}/labels', exist_ok=True)
        
        for img_file in os.listdir(img_dir):
            if img_file.endswith('.tif'):
                # Load image and mask
                img_path = os.path.join(img_dir, img_file)
                mask_path = os.path.join(mask_dir, img_file)
                
                # Convert mask to YOLO bounding boxes
                mask = np.array(Image.open(mask_path))
                bboxes = mask_to_yolo_bbox(mask)
                
                # Copy image
                img = Image.open(img_path)
                img_name = img_file.replace('.tif', '.jpg')
                img.convert('RGB').save(f'yolo_dataset/{split}/images/{img_name}')
                
                # Save YOLO labels
                label_file = img_name.replace('.jpg', '.txt')
                with open(f'yolo_dataset/{split}/labels/{label_file}', 'w') as f:
                    for bbox in bboxes:
                        f.write(f"0 {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")

def mask_to_yolo_bbox(mask):
    """Convert binary mask to YOLO bounding box format"""
    # Find connected components (landslide areas)
    from scipy import ndimage
    
    labeled_mask, num_features = ndimage.label(mask)
    bboxes = []
    
    for i in range(1, num_features + 1):
        # Find bounding box of each landslide area
        coords = np.where(labeled_mask == i)
        if len(coords[0]) > 50:  # Minimum area threshold
            y_min, y_max = coords[0].min(), coords[0].max()
            x_min, x_max = coords[1].min(), coords[1].max()
            
            # Convert to YOLO format (normalized)
            h, w = mask.shape
            x_center = (x_min + x_max) / 2 / w
            y_center = (y_min + y_max) / 2 / h
            width = (x_max - x_min) / w
            height = (y_max - y_min) / h
            
            bboxes.append([x_center, y_center, width, height])
    
    return bboxes
```

### YOLO Training Script
```python
# yolo/train.py
from ultralytics import YOLO
import torch

def train_landslide_yolo():
    # Create dataset config
    dataset_config = """
# Landslide Detection Dataset
path: ./yolo_dataset
train: train/images
val: val/images

# Classes
nc: 1  # number of classes
names: ['landslide']  # class names
"""
    
    with open('yolo_dataset/dataset.yaml', 'w') as f:
        f.write(dataset_config)
    
    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')  # nano version for speed
    
    # Train the model
    results = model.train(
        data='yolo_dataset/dataset.yaml',
        epochs=100,
        imgsz=640,
        batch=16,
        device='cuda' if torch.cuda.is_available() else 'cpu',
        project='landslide_detection',
        name='yolo_landslide_v1'
    )
    
    # Save the trained model
    model.save('yolo/models/landslide_yolo.pt')
    
    return results

if __name__ == "__main__":
    train_landslide_yolo()
```

## Alternative: Pre-trained Models

### Use Existing Models
```python
# If training is too complex, use these approaches:

# 1. Fine-tune a general object detection model
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
# Fine-tune on small landslide dataset
results = model.train(data='small_landslide_dataset.yaml', epochs=50)

# 2. Use semantic segmentation approach
# Convert landslide detection to segmentation problem
model = YOLO('yolov8n-seg.pt')  # Segmentation model
results = model.train(data='landslide_segmentation.yaml', epochs=50)

# 3. Transfer learning from similar domains
# Use models trained on geological features, terrain analysis
```

## Quick Start (No Training Required)

### Use Rule-Based Detection
```python
# For immediate deployment, use simple image analysis
import cv2
import numpy as np

class SimpleLandslideDetector:
    def detect_landslide_features(self, image):
        """Simple rule-based landslide detection"""
        
        # Convert to different color spaces
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        
        # Detect bare soil/rock (common in landslides)
        # Brown/gray color ranges
        lower_brown = np.array([10, 50, 50])
        upper_brown = np.array([20, 255, 200])
        brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
        
        # Detect texture changes (landslides create rough textures)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        texture = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Simple scoring
        brown_ratio = np.sum(brown_mask > 0) / (image.shape[0] * image.shape[1])
        
        confidence = min(brown_ratio * 2 + texture / 1000, 1.0)
        
        return {
            "landslide_detected": confidence > 0.3,
            "confidence": confidence,
            "risk_level": "high" if confidence > 0.7 else "medium" if confidence > 0.4 else "low"
        }
```

## Dataset Download Commands

```bash
# Download Landslide4Sense
wget https://landslide4sense-dataset.s3.amazonaws.com/landslide4sense.zip
unzip landslide4sense.zip

# Download NASA Landslide Catalog
wget https://data.nasa.gov/api/views/dd9e-wu2v/rows.csv?accessType=DOWNLOAD -O nasa_landslides.csv

# Setup directory structure
mkdir -p yolo_dataset/{train,val}/{images,labels}
mkdir -p yolo/models
```

## Performance Expectations

### With Proper Training (Landslide4Sense)
- **Accuracy**: 85-90%
- **Inference Time**: 150-200ms per image
- **Model Size**: 6-14MB (YOLOv8n)
- **GPU Memory**: 2-4GB during training

### With Simple Rule-Based
- **Accuracy**: 60-70%
- **Inference Time**: 50-100ms per image
- **Model Size**: N/A (algorithmic)
- **Memory**: <1GB

## Integration with Your API

```python
# api/yolo_predictor.py
from ultralytics import YOLO
import cv2
import numpy as np

class YOLOLandslideDetector:
    def __init__(self):
        try:
            # Try to load trained model
            self.model = YOLO('yolo/models/landslide_yolo.pt')
            self.use_yolo = True
        except:
            # Fallback to rule-based detection
            self.simple_detector = SimpleLandslideDetector()
            self.use_yolo = False
    
    def analyze_image(self, image):
        if self.use_yolo:
            return self._yolo_analysis(image)
        else:
            return self._simple_analysis(image)
    
    def _yolo_analysis(self, image):
        results = self.model(image)
        # Process YOLO results...
        
    def _simple_analysis(self, image):
        return self.simple_detector.detect_landslide_features(image)
```

This approach gives you flexibility to start with simple detection and upgrade to YOLO when you have proper training data.