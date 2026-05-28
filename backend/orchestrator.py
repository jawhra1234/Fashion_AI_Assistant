from backend.vision.vision_model import VisionModel
from backend.rag.retrieve import RAGRetriever
from backend.llm.llm_engine import LLMEngine
from typing import Dict, Any, Optional

class FashionOrchestrator:
    """
    Orchestrates the fashion recommendation pipeline:
    1. Vision processing (if image provided)
    2. RAG retrieval for fashion rules
    3. LLM reasoning for recommendations
    """
    
    def __init__(self):
        self.vision = VisionModel()
        self.rag = RAGRetriever()
        self.llm = LLMEngine()
    
    def recommend(self, occasion: str, image_bytes: Optional[bytes] = None) -> Dict[str, Any]:
        """
        Main orchestration method.
        
        Args:
            occasion: The occasion for the outfit
            image_bytes: Optional image bytes for vision processing
        
        Returns:
            Dictionary containing outfit recommendations
        """
        # Step 1: Process image if provided
        vision_output = None
        detected_items_list = []
        
        if image_bytes:
            try:
                vision_output = self.vision.analyze_image(image_bytes)
                print("VISION OUTPUT:", vision_output)
                
                # Extract items safely
                if vision_output and isinstance(vision_output, dict):
                    detected_items_list = vision_output.get("items", [])
                    print(f"Extracted {len(detected_items_list)} items from vision")
            except Exception as e:
                print(f"ERROR in vision processing: {e}")
        else:
            print("VISION OUTPUT: No image provided")
        
        # Step 2: Retrieve relevant fashion rules
        try:
            retrieved_rules = self.rag.retrieve_rules(occasion)
            print("OCCASION:", occasion)
            print("RAG RULES:", retrieved_rules)
        except Exception as e:
            print(f"ERROR retrieving rules: {e}")
            retrieved_rules = []
        
        # Step 3: Generate recommendation using LLM
        context = {
            "vision": vision_output,
            "occasion": occasion,
            "rules": retrieved_rules
        }
        
        try:
            recommendation = self.llm.generate_outfit(context)
        except Exception as e:
            print(f"ERROR in LLM generation: {e}")
            recommendation = self._create_fallback_response()
        
        # Add detected items to response
        if detected_items_list:
            recommendation["detected_items"] = detected_items_list
        else:
            recommendation["detected_items"] = None
        
        return recommendation
    
    def _create_fallback_response(self) -> Dict[str, Any]:
        """Create a fallback response when things fail."""
        return {
            "outfit": ["casual shirt", "jeans", "sneakers"],
            "reasoning": "Default recommendation: comfortable casual outfit.",
            "alternative": ["polo shirt", "chinos", "loafers"],
            "style_score": 5.0
        }
