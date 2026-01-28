import json
import re

def extract_json(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except Exception as e:
        print(f">>> JSON 파싱 에러: {e}"); return None