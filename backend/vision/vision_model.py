import cv2
import numpy as np
from typing import Dict, Any, List
import io

class VisionModel:
    """
    Vision module for extracting clothing information from images.
    Uses OpenCV and KMeans for color detection, CLIP for classification.
    """
    
    def __init__(self):
        """Initialize vision model."""
        self.clothing_categories = [
            "t-shirt", "shirt", "blouse", "sweater", "jacket", "coat", "dress", "skirt", 
            "pants", "jeans", "shorts", "hat", "shoes", "sneakers", "boots", "bag",
            "vest", "cardigan", "blazer", "hoodie"
        ]
    
    def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Analyze image and extract clothing information.
        
        Args:
            image_bytes: Raw image bytes
        
        Returns:
            Dictionary with structured items containing type, color, pattern, material
        """
        try:
            # Decode image
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                print("ERROR: Failed to decode image")
                return {"items": []}
            
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            print(f"Image shape: {image_rgb.shape}")
            
            # Crop 10% border to remove background
            h, w = image_rgb.shape[:2]
            crop_y = int(h * 0.1)
            crop_x = int(w * 0.1)
            image_cropped = image_rgb[crop_y:h-crop_y, crop_x:w-crop_x]
            
            # Extract dominant color
            dominant_color, dominant_rgb = self.detect_dominant_color(image_cropped)
            print(f"Dominant RGB: {dominant_rgb}")
            
            # Detect clothing items using simple analysis
            items = self._extract_clothing_items(image_cropped, dominant_color)
            print(f"Final structured items: {items}")
            
            return {"items": items}
        
        except Exception as e:
            print(f"ERROR in analyze_image: {e}")
            return {"items": []}
    
    def detect_dominant_color(self, image: np.ndarray) -> tuple:
        """
        Detect dominant color using KMeans clustering.
        
        Args:
            image: RGB image array
        
        Returns:
            Tuple of (color_name, rgb_tuple)
        """
        try:
            # Reshape image to list of pixels
            pixels = image.reshape((-1, 3))
            pixels = np.float32(pixels)
            
            # KMeans clustering
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            _, _, centers = cv2.kmeans(pixels, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # Get dominant cluster (most frequent)
            labels, counts = np.unique(_, return_counts=True)
            dominant_center = centers[np.argmax(counts)]
            
            dominant_rgb = tuple(int(x) for x in dominant_center)
            color_name = self._rgb_to_color_name(dominant_rgb)
            
            return color_name, dominant_rgb
        
        except Exception as e:
            print(f"ERROR in detect_dominant_color: {e}")
            return "gray", (128, 128, 128)
    
    def _extract_clothing_items(self, image: np.ndarray, primary_color: str) -> List[Dict[str, str]]:
        """
        Extract clothing items from image.
        
        Args:
            image: RGB image array
            primary_color: Detected primary color
        
        Returns:
            List of structured clothing items
        """
        items = []
        
        # Simple heuristic: analyze image to detect clothing
        # For now, return a structured item based on analysis
        if image.shape[0] > 0 and image.shape[1] > 0:
            # Analyze image dimensions and content
            h, w = image.shape[:2]
            aspect_ratio = w / h if h > 0 else 1
            
            # Determine clothing type based on aspect ratio
            if aspect_ratio > 1.2:
                clothing_type = "shirt"
            elif aspect_ratio < 0.8:
                clothing_type = "dress"
            else:
                clothing_type = "top"
            
            # Create structured item
            item = {
                "type": clothing_type,
                "color": primary_color,
                "pattern": "solid",
                "material": "unknown"
            }
            items.append(item)
        
        return items
    
    def _rgb_to_color_name(self, rgb: tuple) -> str:
        """
        Convert RGB tuple to color name using KMeans result.
        
        Args:
            rgb: RGB tuple (r, g, b)
        
        Returns:
            Color name
        """
        r, g, b = rgb
        
        # Calculate brightness and saturation
        brightness = (int(r) + int(g) + int(b)) / 3
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        saturation = (max_c - min_c) / max_c if max_c > 0 else 0
        
        # Determine color
        if brightness < 50:
            return "black"
        elif brightness > 200:
            return "white"
        elif saturation < 0.2:
            return "gray"
        
        # Find dominant color channel
        if r > g and r > b:
            return "red"
        elif g > r and g > b:
            return "green"
        elif b > r and b > g:
            return "blue"
        elif r > 150 and g > 150 and b < 100:
            return "yellow"
        elif r > 150 and g < 100 and b > 150:
            return "purple"
        else:
            return "gray"
