from core.engine import MetaDynamicManager

if __name__ == "__main__":
    manager = MetaDynamicManager()
    # 이 질문을 넣으면 아키텍트가 알아서 '논리 대결' 구조로 팀을 짤 것임
    query = "몬티홀 문제에서 선택을 바꾸는 것이 유리한지, 아니면 확률이 50:50으로 동일한지 수학적으로 증명하고 최종 결론을 내려라."
    manager.run(query)