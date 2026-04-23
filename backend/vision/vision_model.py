from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import io
from colorthief import ColorThief
from typing import Dict, Any

class VisionModel:
    """
    Vision module for extracting clothing information from images.
    Uses CLIP for clothing item classification and ColorThief for color extraction.
    """
    
    def __init__(self):
        # Load CLIP model for clothing classification
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        # Predefined clothing categories for classification
        self.clothing_categories = [
            "t-shirt", "shirt", "blouse", "sweater", "jacket", "coat", "dress", "skirt", 
            "pants", "jeans", "shorts", "hat", "shoes", "sneakers", "boots", "bag"
        ]
    
    def extract_clothing_info(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Extract clothing information from image bytes.
        
        Args:
            image_bytes: Raw image bytes
        
        Returns:
            Dictionary with item and color information
        """
        try:
            # Open image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Extract dominant color
            color = self._extract_dominant_color(image_bytes)
            
            # Classify clothing item using CLIP
            item = self._classify_clothing_item(image)
            
            return {
                "item": item,
                "color": color
            }
        
        except Exception as e:
            # Fallback if vision processing fails
            return {
                "item": "unknown",
                "color": "unknown"
            }
    
    def _classify_clothing_item(self, image: Image.Image) -> str:
        """
        Classify the main clothing item in the image using CLIP.
        
        Args:
            image: PIL Image object
        
        Returns:
            Predicted clothing item
        """
        # Prepare inputs
        inputs = self.processor(
            text=self.clothing_categories,
            images=image,
            return_tensors="pt",
            padding=True
        )
        
        # Get predictions
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        
        # Get the most likely category
        best_idx = probs.argmax().item()
        return self.clothing_categories[best_idx]
    
    def _extract_dominant_color(self, image_bytes: bytes) -> str:
        """
        Extract dominant color from image using ColorThief.
        
        Args:
            image_bytes: Raw image bytes
        
        Returns:
            Color name as string
        """
        try:
            # Use ColorThief to get dominant color
            color_thief = ColorThief(io.BytesIO(image_bytes))
            dominant_color = color_thief.get_color(quality=1)
            
            # Convert RGB to color name
            return self._rgb_to_color_name(dominant_color)
        
        except Exception:
            return "unknown"
    
    def _rgb_to_color_name(self, rgb: tuple) -> str:
        """
        Convert RGB tuple to approximate color name.
        
        Args:
            rgb: RGB tuple (r, g, b)
        
        Returns:
            Color name
        """
        r, g, b = rgb
        
        # Simple color mapping based on RGB values
        if r > 200 and g > 200 and b > 200:
            return "white"
        elif r > 150 and g < 100 and b < 100:
            return "red"
        elif r < 100 and g > 150 and b < 100:
            return "green"
        elif r < 100 and g < 100 and b > 150:
            return "blue"
        elif r > 150 and g > 150 and b < 100:
            return "yellow"
        elif r > 150 and g < 100 and b > 150:
            return "purple"
        elif r < 100 and g < 100 and b < 100:
            return "black"
        elif r > 100 and g > 100 and b > 100:
            return "gray"
        else:
            return "multicolor"