import os
import json
from autogen import UserProxyAgent
from config.settings import llm_config
from agents.system_agents import get_architect, get_enricher
from agents.factory import create_agent
from utils.parser import extract_json

class MetaDynamicManager:
    def __init__(self):
        self.agents = {}
        self.step_results = {}
        self.admin = UserProxyAgent(name="Admin", human_input_mode="NEVER", code_execution_config=False)
        self.log_dir = "logs"
        self.initial_file = f"{self.log_dir}/1_initial_plan.json"
        self.final_file = f"{self.log_dir}/2_final_plan.json"
        os.makedirs(self.log_dir, exist_ok=True)

    def run(self, user_query):
        # --- [1/5] PHASE 1: Architect (범용 설계) ---
        architect = get_architect(llm_config)
        
        print("\n[1/5] Architect가 전략 수립 중...")
        res = self.admin.initiate_chat(architect, message=user_query, max_turns=1)
        initial_plan = extract_json(res.summary)
        
        # [파일 브릿지 1] 초안 저장
        with open(self.initial_file, "w", encoding="utf-8") as f:
            json.dump(initial_plan, f, indent=2, ensure_ascii=False)

        # --- [2/5] PHASE 2: Prompt_Enricher (범용 보강) ---
        # [파일 브릿지 2] 초안 읽기
        with open(self.initial_file, "r", encoding="utf-8") as f:
            plan_to_enrich = json.load(f)

        enricher = get_enricher(llm_config)
        
        print("\n[2/5] Prompt_Enricher가 설계를 보강 중...")
        enrich_res = self.admin.initiate_chat(enricher, message=json.dumps(plan_to_enrich, ensure_ascii=False), max_turns=1)
        enriched_plan = extract_json(enrich_res.summary)
        
        # [파일 브릿지 3] 최종본 저장
        with open(self.final_file, "w", encoding="utf-8") as f:
            json.dump(enriched_plan, f, indent=2, ensure_ascii=False)

        # --- [3/5] PHASE 3: 에이전트 생성 ---
        print("\n[3/5] 최종 설계도를 읽어 에이전트 생성 중...")
        with open(self.final_file, "r", encoding="utf-8") as f:
            execution_plan = json.load(f)

        workflow_list = execution_plan.get('workflow', [])
        if isinstance(workflow_list, dict): workflow_list = workflow_list.get('steps', [])

        for member in execution_plan.get('team', []):
            self.agents[member['name']] = create_agent(member['name'], member['persona'], llm_config)

        # --- [4/5] PHASE 4: 작업 개시 (상세 모드) ---
        print("\n[4/5] 작업 개시")
        for step in workflow_list:
            agent_name = step.get('agent') or step.get('responsible')
            agent = self.agents.get(agent_name)
            if not agent: continue

            deps = step.get('depends_on') or []
            context = "\n".join([f"Step {d} 결과: {self.step_results.get(d, '')}" for d in deps])
            
            print(f"\n>>> [Step {step.get('id') or step.get('step')}] {agent_name} 작업 중...")

            prompt = f"""
            [전체 목표 (사용자 질문)]
            "{user_query}"

            [이전 맥락]
            {context}

            [수행할 임무]
            {step.get('task') or step.get('description')}

            [응답 규칙]
            - 너의 전문가적 페르소나를 십분 활용하여 상세하고 논리적으로 답변하라.
            """

            work_res = self.admin.initiate_chat(agent, message=prompt, max_turns=1, summary_method="last_msg")
            self.step_results[step.get('id') or step.get('step')] = work_res.summary

        # --- [5/5] PHASE 5: 보고서 저장 ---
        
        return self.step_results