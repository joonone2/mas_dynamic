from core.engine import MetaDynamicManager

if __name__ == "__main__":
    manager = MetaDynamicManager()
    
    query = "몬티홀 문제에서 선택을 바꾸는 것이 유리한지, 아니면 확률이 50:50으로 동일한지 수학적으로 증명하고 최종 결론을 내려라."
    manager.run(query)