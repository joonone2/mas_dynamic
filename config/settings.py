import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", "").strip().replace('"', '').replace("'", "")
config_list = [{"model": "gpt-4o-mini", "api_key": api_key}]
llm_config = {"config_list": config_list, "temperature": 0.1}