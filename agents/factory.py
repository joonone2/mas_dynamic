from autogen import AssistantAgent

def _format_persona(persona):
    """원본 클래스의 _format_persona 메서드 로직"""
    if isinstance(persona, dict):
        return ". ".join([f"{k}: {v}" for k, v in persona.items()])
    return str(persona)

def create_agent(name, persona, llm_config):
    """설계도 기반으로 동적 에이전트 생성"""
    p_str = _format_persona(persona)
    return AssistantAgent(
        name=name,
        llm_config=llm_config,
        system_message=p_str
    )