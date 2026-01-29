# 파일 위치: agents/system_agents.py

import os
from autogen import AssistantAgent

def _load_prompt(filename):
    """
    prompts 폴더에서 텍스트 파일을 읽어오기
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "prompts", filename)
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f">>> [System Error] 프롬프트 파일을 찾을 수 없습니다: {path}")
        return "You are a helpful AI assistant." # 파일이 없을 경우 기본값

def get_architect(llm_config):
    prompt = _load_prompt("architect.txt")
    return AssistantAgent(
        name="Architect",
        llm_config=llm_config,
        system_message=prompt
    )

def get_enricher(llm_config):
    prompt = _load_prompt("enricher.txt")
    return AssistantAgent(
        name="Prompt_Enricher",
        llm_config=llm_config,
        system_message=prompt
    )