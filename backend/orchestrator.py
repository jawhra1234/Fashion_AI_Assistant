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
        vision_output = {}
        if image_bytes:
            vision_output = self.vision.extract_clothing_info(image_bytes)
        
        # Step 2: Retrieve relevant fashion rules
        retrieved_rules = self.rag.retrieve_rules(occasion)
        
        # Step 3: Generate recommendation using LLM
        context = {
            "vision_output": vision_output,
            "occasion": occasion,
            "retrieved_rules": retrieved_rules
        }
        
        recommendation = self.llm.generate_outfit(context)
        
        return recommendation