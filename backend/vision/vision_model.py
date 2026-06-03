import base64
import requests
import json
import time
from typing import Dict, Any


class VisionModel:

    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llava:7b"

    def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:

        if not image_bytes:
            return {"items": []}

        try:
            print("\n========== LLAVA VISION ==========")

            base64_image = base64.b64encode(image_bytes).decode("utf-8")

            prompt = """
Analyze this image.

Identify visible clothing items.

Return ONLY valid JSON:

{
  "items": [
    {
      "type": "",
      "color": "",
      "pattern": "",
      "material": ""
    }
  ]
}

Rules:
- Do not repeat duplicate items.
- Only describe clearly visible clothing.
- If unsure use "unknown".
- No explanation.
- JSON only.
"""

            payload = {
                "model": self.model,
                "prompt": prompt,
                "images": [base64_image],
                "stream": False,
                "format": "json"
            }

            start = time.time()

            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=300
            )

            elapsed = time.time() - start

            print(f"VISION TOOK {elapsed:.2f} seconds")

            response.raise_for_status()

            result = response.json()

            raw_output = result.get("response", "{}")

            print("\nRAW LLAVA OUTPUT:")
            print(raw_output)

            parsed = json.loads(raw_output)

            items = parsed.get("items", [])

            cleaned_items = []

            seen = set()

            for item in items:

                if not isinstance(item, dict):
                    continue

                clothing_item = {
                    "type": str(item.get("type", "unknown")).lower(),
                    "color": str(item.get("color", "unknown")).lower(),
                    "pattern": str(item.get("pattern", "unknown")).lower(),
                    "material": str(item.get("material", "unknown")).lower()
                }

                key = (
                    clothing_item["type"],
                    clothing_item["color"]
                )

                if key not in seen:
                    seen.add(key)
                    cleaned_items.append(clothing_item)

            print(f"Detected {len(cleaned_items)} items")
            print(cleaned_items)

            if len(cleaned_items) == 0:
                return {
                    "items": [
                        {
                            "type": "unknown",
                            "color": "unknown",
                            "pattern": "unknown",
                            "material": "unknown"
                        }
                    ]
                }

            return {"items": cleaned_items}

        except Exception as e:

            print(f"VISION ERROR: {e}")

            return {
                "items": [
                    {
                        "type": "unknown",
                        "color": "unknown",
                        "pattern": "unknown",
                        "material": "unknown"
                    }
                ]
            }