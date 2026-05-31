import base64
import requests
import json
import time
import io

from PIL import Image
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

            # --------------------------------------------------
            # COMPRESS IMAGE BEFORE SENDING TO LLAVA
            # --------------------------------------------------

            img = Image.open(io.BytesIO(image_bytes))

            img.thumbnail((448, 448))

            buffer = io.BytesIO()

            img.convert("RGB").save(
                buffer,
                format="JPEG",
                quality=75,
                optimize=True
            )

            compressed_bytes = buffer.getvalue()

            print(
                f"Original: {len(image_bytes)/1024:.1f} KB | "
                f"Compressed: {len(compressed_bytes)/1024:.1f} KB"
            )

            base64_image = base64.b64encode(
                compressed_bytes
            ).decode("utf-8")

            prompt = """
Analyze this fashion image carefully.

Identify ONLY clothing items that are clearly visible.

Return ONLY valid JSON.

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

- Do NOT invent items.
- Do NOT repeat items.
- Maximum 5 items.
- If unsure, skip the item.
- Use lowercase values.

Allowed types:
shirt, t-shirt, blouse, blazer,
jacket, hoodie, sweater,
dress, skirt, pants, jeans,
shorts, shoes, sneakers,
boots, bag, hat

Allowed patterns:
solid, striped, plaid,
checkered, graphic,
floral, printed, unknown

If material is unclear:
"unknown"

Return JSON only.
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
                    "type": str(
                        item.get("type", "unknown")
                    ).lower().strip(),

                    "color": str(
                        item.get("color", "unknown")
                    ).lower().strip(),

                    "pattern": str(
                        item.get("pattern", "unknown")
                    ).lower().strip(),

                    "material": str(
                        item.get("material", "unknown")
                    ).lower().strip()
                }

                # Skip useless detections

                if clothing_item["type"] in [
                    "",
                    "unknown",
                    "clothing"
                ]:
                    continue

                key = (
                    clothing_item["type"],
                    clothing_item["color"]
                )

                if key not in seen:
                    seen.add(key)
                    cleaned_items.append(clothing_item)

            print(
                f"Detected {len(cleaned_items)} items"
            )

            print(cleaned_items)

            return {"items": cleaned_items}

        except Exception as e:

            print(f"VISION ERROR: {e}")

            return {
                "items": []
            }