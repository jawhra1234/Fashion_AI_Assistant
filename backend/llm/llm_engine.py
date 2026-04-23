import requests
import json
from typing import Dict, Any, List

class LLMEngine:
    """
    LLM engine using Ollama for generating fashion recommendations.
    """
    
    def __init__(self, model: str = "mistral"):
        """
        Initialize LLM engine.
        
        Args:
            model: Ollama model name (e.g., 'mistral', 'llama3')
        """
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
    
    def generate_outfit(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate outfit recommendation using LLM.
        
        Args:
            context: Dictionary containing vision_output, occasion, and retrieved_rules
        
        Returns:
            Dictionary with outfit, reasoning, alternatives, and style_score
        """
        vision_output = context.get("vision_output", {})
        occasion = context.get("occasion", "")
        retrieved_rules = context.get("retrieved_rules", [])
        
        # Create prompt
        prompt = self._create_prompt(vision_output, occasion, retrieved_rules)
        
        # Generate response from Ollama
        response = self._call_ollama(prompt)
        
        # Parse response
        return self._parse_response(response)
    
    def _create_prompt(self, vision_output: Dict[str, Any], occasion: str, rules: List[str]) -> str:
        """
        Create structured prompt for the LLM.
        
        Args:
            vision_output: Clothing information from vision module
            occasion: User occasion
            rules: Retrieved fashion rules
        
        Returns:
            Formatted prompt string
        """
        rules_text = "\n".join([f"- {rule}" for rule in rules])
        
        prompt = f"""You are a professional fashion stylist.

User clothing: {vision_output}
Occasion: {occasion}
Fashion rules: {rules_text}

Task:
1. Suggest the best outfit based on the user's clothing and occasion
2. Explain your reasoning clearly
3. Suggest 1 alternative outfit option
4. Give a style score from 0-10 (where 10 is perfect)

Format your response as JSON:
{{
    "outfit": ["item1", "item2", "item3"],
    "reasoning": "your detailed explanation",
    "alternatives": ["alternative item1", "alternative item2"],
    "style_score": 8.5
}}

Be specific and helpful in your recommendations."""
        
        return prompt
    
    def _call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API to generate response.
        
        Args:
            prompt: Input prompt
        
        Returns:
            Generated text response
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
        
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama: {e}")
            return self._fallback_response()
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured format.
        
        Args:
            response: Raw LLM response
        
        Returns:
            Structured dictionary
        """
        try:
            # Try to extract JSON from response
            # Look for JSON block in the response
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start != -1 and end != -1:
                json_str = response[start:end]
                parsed = json.loads(json_str)
                return parsed
            else:
                # Fallback parsing
                return self._fallback_response()
        
        except json.JSONDecodeError:
            return self._fallback_response()
    
    def _fallback_response(self) -> Dict[str, Any]:
        """
        Provide fallback response when LLM fails.
        
        Returns:
            Default structured response
        """
        return {
            "outfit": ["casual shirt", "jeans", "sneakers"],
            "reasoning": "Based on general fashion guidelines for comfort and style.",
            "alternatives": ["polo shirt", "chinos", "loafers"],
            "style_score": 7.0
        }