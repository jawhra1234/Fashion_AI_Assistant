import requests
import json
from typing import Dict, Any, List

class LLMEngine:
    """
    LLM engine using Ollama for generating fashion recommendations.
    """
    
    def __init__(self, model: str = "llama3.1"):
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
            context: Dictionary containing vision, occasion, and rules
        
        Returns:
            Dictionary with outfit, reasoning, alternatives, and style_score
        """
        vision_output = context.get("vision")
        occasion = context.get("occasion", "")
        retrieved_rules = context.get("rules", [])
        
        # Create prompt
        prompt = self._create_prompt(vision_output, occasion, retrieved_rules)
        
        # Generate response from Ollama
        response = self._call_ollama(prompt)
        
        # Parse response
        return self._parse_response(response)
    
    def _create_prompt(self, vision_output, occasion: str, rules: List[str]) -> str:
        """
        Create structured prompt for the LLM.
        
        Args:
            vision_output: Clothing information from vision module (dict with "items" or None)
            occasion: User occasion
            rules: Retrieved fashion rules
        
        Returns:
            Formatted prompt string
        """
        rules_text = "\n".join([f"- {rule}" for rule in rules]) if rules else "No specific rules provided"
        
        # Format detected items
        if vision_output and "items" in vision_output and vision_output["items"]:
            items_list = vision_output["items"]
            if isinstance(items_list, list) and len(items_list) > 0:
                # Check if items are dicts or strings
                if isinstance(items_list[0], dict):
                    detected_items = "\n".join([
                        f"- {item.get('color', 'unknown')} {item.get('type', 'item')}"
                        for item in items_list
                    ])
                else:
                    detected_items = "\n".join([f"- {item}" for item in items_list])
                
                case_instruction = """CASE 1: You MUST work with provided clothing items:
- ONLY suggest items from the detected items list
- DO NOT invent new clothing
- Select combinations that BEST fit the occasion
- Use fashion rules to guide selection"""
            else:
                detected_items = "None"
                case_instruction = """CASE 2: Generate outfit from general knowledge:
- Use occasion and fashion rules
- Choose realistic appropriate clothing"""
        else:
            detected_items = "None"
            case_instruction = """CASE 2: Generate outfit from general knowledge:
- Use occasion and fashion rules
- Choose realistic appropriate clothing"""
        
        prompt = f"""You are a professional fashion stylist.

DETECTED ITEMS:
{detected_items}

OCCASION: {occasion}

FASHION RULES:
{rules_text}

INSTRUCTIONS:
{case_instruction}

Generate outfit recommendations in valid JSON format.

Return ONLY a JSON object with no other text:
{{
  "outfit": ["item1", "item2", "item3"],
  "reasoning": "Why this outfit works",
  "alternative": ["alt_item1", "alt_item2"],
  "style_score": 7.5
}}

Be concise and realistic."""
        
        return prompt
    
    def _call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API to generate response.
        
        Args:
            prompt: Input prompt
        
        Returns:
            Generated text response (or JSON string on error)
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            }
            print("\n========== OLLAMA DEBUG ==========")
            print("MODEL:", self.model)
            print("PAYLOAD SENT:", payload)
            print("=================================\n")
            print("=" * 50)
            print("OLLAMA URL:", self.ollama_url)
            print("MODEL:", self.model)
            print("PAYLOAD:", payload)
            print("=" * 50)
            response = requests.post(self.ollama_url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            print("\n========== RAW OLLAMA RESPONSE ==========")
            print(result)
            print("========================================\n")
            return result.get("response", "")
        
        except requests.exceptions.ConnectionError as e:
            print(f"ERROR: Failed to connect to Ollama at {self.ollama_url}: {e}")
            print("Make sure Ollama is running: ollama serve")
            return json.dumps(self._fallback_response())
        
        except requests.exceptions.Timeout as e:
            print(f"ERROR: Ollama request timed out: {e}")
            return json.dumps(self._fallback_response())
        
        except Exception as e:
            print(f"ERROR calling Ollama: {e}")
            return json.dumps(self._fallback_response())
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured format.
        
        Args:
            response: Raw LLM response string
        
        Returns:
            Structured dictionary
        """
        try:
            # Handle empty response
            if not response or len(response.strip()) == 0:
                print("ERROR: Empty response from LLM")
                return self._fallback_response()
            
            # Try to extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = response[start:end]
                parsed = json.loads(json_str)
                
                # Validate parsed response has required fields
                if "outfit" in parsed and "reasoning" in parsed:
                    # Ensure alternative is a list
                    if "alternative" not in parsed:
                        parsed["alternative"] = []
                    if not isinstance(parsed["alternative"], list):
                        parsed["alternative"] = [parsed["alternative"]]
                    
                    # Ensure style_score is a float
                    if "style_score" not in parsed:
                        parsed["style_score"] = 5.0
                    else:
                        try:
                            parsed["style_score"] = float(parsed["style_score"])
                        except (ValueError, TypeError):
                            parsed["style_score"] = 5.0
                    
                    return parsed
            
            print("ERROR: Could not extract valid JSON from LLM response")
            return self._fallback_response()
        
        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to parse JSON: {e}")
            return self._fallback_response()
        
        except Exception as e:
            print(f"ERROR in _parse_response: {e}")
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
            "alternative": ["polo shirt", "chinos", "loafers"],
            "style_score": 7.0
        }