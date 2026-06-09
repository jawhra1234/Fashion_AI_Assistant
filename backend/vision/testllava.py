import base64
import requests

with open(r"D:\fashion-ai-assistant\backend\vision\test.jpg", "rb") as f:
    image = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "model": "llava:7b",
    "prompt": """
Describe all clothing items.
Return ONLY JSON:
{
  "items":[
    {
      "type":"",
      "color":"",
      "pattern":"",
      "material":""
    }
  ]
}
""",
    "images": [image],
    "stream": False,
    "format": "json"
}

r = requests.post(
    "http://localhost:11434/api/generate",
    json=payload
)

print(r.json()["response"])