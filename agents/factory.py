from autogen import AssistantAgent

def _format_persona(persona):
    if isinstance(persona, dict):
        return ". ".join([f"{k}: {v}" for k, v in persona.items()])
    return str(persona)

def create_agent(name, persona, llm_config):
    """설계도 기반으로 에이전트 생성"""
    p_str = _format_persona(persona)
    return AssistantAgent(
        name=name,
        llm_config=llm_config,
        system_message=p_str
    )