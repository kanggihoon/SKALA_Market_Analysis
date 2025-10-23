"""
보고서 생성 에이전트 - LangGraph 워크플로우 통합

이 모듈은 HTML과 DOCX 형식의 보고서를 자동 생성하는 에이전트입니다.
"""

import os
from typing import Dict, Annotated
from pathlib import Path
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from report_templates import StrategyReportTemplate
from docx_report_generator import DocxReportGenerator


class ReportGenerationState(TypedDict):
    """보고서 생성용 State (전체 MarketEntryState의 서브셋)"""
    company: str
    country: str
    messages: Annotated[list, add_messages]
    
    # 각 섹션별 데이터
    market_summary: Dict
    regulatory_data: Dict
    competitor_data: Dict
    partner_data: Dict
    risk_data: Dict
    decision_data: Dict
    
    # 시각화 파일 경로들
    visualizations: Dict[str, str]
    
    # 최종 산출물
    html_report_path: str
    docx_report_path: str
    report_generated: bool


def generate_report_agent(state: ReportGenerationState) -> ReportGenerationState:
    """
    보고서 생성 에이전트
    
    HTML과 DOCX 형식의 보고서를 생성하고 /mnt/user-data/outputs에 저장합니다.
    """
    company = state["company"]
    country = state["country"]
    
    print(f"📄 보고서 생성 시작: {company} × {country}")
    
    # 출력 디렉토리 설정
    output_dir = Path("/mnt/user-data/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 파일명 생성 (공백 제거, 안전한 파일명)
    safe_company = company.replace(" ", "_").replace("/", "-")
    safe_country = country.replace(" ", "_").replace("/", "-")
    
    html_path = output_dir / f"strategy_report_{safe_company}_{safe_country}.html"
    docx_path = output_dir / f"strategy_report_{safe_company}_{safe_country}.docx"
    
    try:
        # 1. HTML 보고서 생성
        print("  → HTML 보고서 생성 중...")
        html_content = StrategyReportTemplate.generate_html_report(
            company=company,
            country=country,
            market_summary=state.get("market_summary", {}),
            regulatory_data=state.get("regulatory_data", {}),
            competitor_data=state.get("competitor_data", {}),
            partner_data=state.get("partner_data", {}),
            risk_data=state.get("risk_data", {}),
            decision_data=state.get("decision_data", {}),
            visualizations=state.get("visualizations", {})
        )
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"  ✓ HTML 저장: {html_path}")
        
        # 2. DOCX 보고서 생성
        print("  → DOCX 보고서 생성 중...")
        DocxReportGenerator.generate_full_report(
            company=company,
            country=country,
            market_summary=state.get("market_summary", {}),
            regulatory_data=state.get("regulatory_data", {}),
            competitor_data=state.get("competitor_data", {}),
            partner_data=state.get("partner_data", {}),
            risk_data=state.get("risk_data", {}),
            decision_data=state.get("decision_data", {}),
            visualizations=state.get("visualizations", {}),
            output_path=str(docx_path)
        )
        
        print(f"  ✓ DOCX 저장: {docx_path}")
        
        # State 업데이트
        state["html_report_path"] = str(html_path)
        state["docx_report_path"] = str(docx_path)
        state["report_generated"] = True
        
        # 메시지 추가
        state["messages"].append({
            "role": "assistant",
            "content": f"보고서 생성 완료!\n\n"
                      f"📊 [HTML 보고서 보기](computer://{html_path})\n"
                      f"📄 [DOCX 보고서 다운로드](computer://{docx_path})\n\n"
                      f"두 가지 형식으로 제공됩니다:\n"
                      f"- HTML: 웹 브라우저에서 바로 확인 가능 (시각적으로 예쁨)\n"
                      f"- DOCX: Word에서 편집 가능 (인쇄/공유 용이)"
        })
        
        print("✅ 보고서 생성 완료!")
        
    except Exception as e:
        print(f"❌ 보고서 생성 실패: {e}")
        state["report_generated"] = False
        state["messages"].append({
            "role": "assistant",
            "content": f"⚠️ 보고서 생성 중 오류 발생: {str(e)}"
        })
    
    return state


# ============================================================
# 사용 예시: LangGraph 워크플로우에 통합
# ============================================================

def create_full_workflow_with_reports():
    """
    전체 워크플로우 + 보고서 생성 통합 예시
    """
    from typing_extensions import TypedDict
    
    class FullMarketEntryState(TypedDict):
        """전체 State (기존 + 보고서)"""
        company: str
        country: str
        messages: Annotated[list, add_messages]
        
        # 각 단계별 산출물
        market_summary: Dict
        regulatory_data: Dict
        competitor_data: Dict
        partner_data: Dict
        risk_data: Dict
        decision_data: Dict
        visualizations: Dict[str, str]
        
        # 보고서
        html_report_path: str
        docx_report_path: str
        report_generated: bool
        
        # 제어 플래그
        hold_flag: bool
    
    # 그래프 생성
    workflow = StateGraph(FullMarketEntryState)
    
    # 노드 추가 (예시 - 실제로는 각 에이전트 함수 구현 필요)
    def market_research_agent(state): 
        print("1. 시장조사 실행...")
        state["market_summary"] = {
            "metrics": {"TAM": "$2.5B", "성장률": "15%"},
            "why_now": "이커머스 급성장"
        }
        return state
    
    def regulatory_review_agent(state):
        print("2. 규제검토 실행...")
        state["regulatory_data"] = {
            "coverage_score": 0.76,
            "risk_badge": "보통",
            "checklist": []
        }
        state["hold_flag"] = False  # MUST-FAIL 체크
        return state
    
    def competitor_mapping_agent(state):
        print("3. 경쟁사 지도 실행...")
        state["competitor_data"] = {"whitespace_gaps": []}
        return state
    
    def partner_discovery_agent(state):
        print("4. 파트너 발굴 실행...")
        state["partner_data"] = {"candidates": []}
        return state
    
    def risk_scenarios_agent(state):
        print("5. 리스크 시나리오 실행...")
        state["risk_data"] = {"register": [], "scenarios": {}}
        return state
    
    def decision_making_agent(state):
        print("6. 의사결정 실행...")
        state["decision_data"] = {
            "decision": "진행(추천)",
            "rationale": "시장 성장성 높음",
            "final_score": 72,
            "scorecard": {},
            "next_steps": []
        }
        return state
    
    # 노드 등록
    workflow.add_node("market_research", market_research_agent)
    workflow.add_node("regulatory_review", regulatory_review_agent)
    workflow.add_node("competitor_mapping", competitor_mapping_agent)
    workflow.add_node("partner_discovery", partner_discovery_agent)
    workflow.add_node("risk_scenarios", risk_scenarios_agent)
    workflow.add_node("decision_making", decision_making_agent)
    workflow.add_node("report_generation", generate_report_agent)  # ← 보고서 생성
    
    # 엣지 연결
    workflow.set_entry_point("market_research")
    workflow.add_edge("market_research", "regulatory_review")
    
    # 조건부 분기: HOLD 체크
    workflow.add_conditional_edges(
        "regulatory_review",
        lambda state: "hold" if state.get("hold_flag") else "continue",
        {
            "hold": "decision_making",  # 즉시 의사결정으로
            "continue": "competitor_mapping"
        }
    )
    
    workflow.add_edge("competitor_mapping", "partner_discovery")
    workflow.add_edge("partner_discovery", "risk_scenarios")
    workflow.add_edge("risk_scenarios", "decision_making")
    workflow.add_edge("decision_making", "report_generation")  # 의사결정 후 보고서
    workflow.add_edge("report_generation", END)
    
    return workflow.compile()


# ============================================================
# 독립 실행 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("보고서 생성 에이전트 테스트")
    print("=" * 60)
    
    # 테스트 데이터
    test_state: ReportGenerationState = {
        "company": "스타트업A",
        "country": "베트남",
        "messages": [],
        "market_summary": {
            "metrics": {
                "TAM": "$2.5B",
                "성장률": "15% YoY",
                "택배량": "500M건/년",
                "평균 배송비": "$2.50",
                "리드타임": "2-3일"
            },
            "why_now": "이커머스 급성장(35% YoY)과 중산층 확대로 빠른 배송 수요 증가"
        },
        "regulatory_data": {
            "coverage_score": 0.76,
            "risk_badge": "보통",
            "checklist": [
                {"item": "택배업 등록", "grade": "MUST", "state": "PASS", "evidence": "국토부 고시 확인"},
                {"item": "개인정보 국외이전", "grade": "MUST", "state": "TBD", "evidence": "DPA 근거 미확인"},
            ]
        },
        "competitor_data": {
            "whitespace_gaps": [
                "농촌 지역 당일배송 서비스 부재",
                "프리미엄 콜드체인 물류 미개척",
            ]
        },
        "partner_data": {
            "candidates": [
                {"name": "VietPost", "role": "라스트마일", "rationale": "전국 네트워크", "alternative": "GHN"},
            ],
            "poc_proposal": "1단계: 호치민 시범 운영\n2단계: 하노이 확장"
        },
        "risk_data": {
            "register": [
                {"risk": "규제 변경", "likelihood": "보통", "impact": "높음", 
                 "early_sign": "정부 발표", "mitigation": "로비스트 고용"},
            ],
            "scenarios": {
                "pessimistic": {"월 거래량": "10K건"},
                "base": {"월 거래량": "30K건"},
                "optimistic": {"월 거래량": "100K건"}
            }
        },
        "decision_data": {
            "decision": "진행(추천)",
            "rationale": "시장 성장성과 실행 가능성 높음. 규제 리스크는 관리 가능한 수준.",
            "final_score": 72,
            "scorecard": {
                "시장 매력도": 85,
                "규제 리스크": 65,
                "경쟁 강도": 60,
                "실행 가능성": 75,
                "파트너 가용성": 80
            },
            "next_steps": [
                "DPA 협약 체결 (2주)",
                "VietPost와 MOU 체결 (1개월)",
            ]
        },
        "visualizations": {},
        "html_report_path": "",
        "docx_report_path": "",
        "report_generated": False
    }
    
    # 보고서 생성 실행
    result = generate_report_agent(test_state)
    
    print("\n" + "=" * 60)
    print("결과:")
    print(f"  HTML: {result['html_report_path']}")
    print(f"  DOCX: {result['docx_report_path']}")
    print(f"  성공: {result['report_generated']}")
    print("=" * 60)
