"""
보고서 생성 시스템 - 완전 가이드

이 문서는 다국적 시장 진출 전략 보고서 생성 시스템의
사용법, 프롬프트 템플릿, 커스터마이징 방법을 설명합니다.
"""

# ============================================================
# 1. 빠른 시작
# ============================================================

"""
## 기본 사용법

```python
from report_agent import generate_report_agent

# 1. State 준비 (각 에이전트가 수집한 데이터)
state = {
    "company": "스타트업A",
    "country": "베트남",
    "market_summary": {...},
    "regulatory_data": {...},
    # ... 기타 데이터
}

# 2. 보고서 생성
result = generate_report_agent(state)

# 3. 결과 확인
print(f"HTML: {result['html_report_path']}")
print(f"DOCX: {result['docx_report_path']}")
```

생성된 보고서는 `/mnt/user-data/outputs/` 에 저장됩니다.
"""


# ============================================================
# 2. 각 에이전트용 프롬프트 템플릿
# ============================================================

class PromptTemplates:
    """각 에이전트에서 사용할 프롬프트 템플릿"""
    
    # --------------------------------------------------------
    # 시장조사 에이전트
    # --------------------------------------------------------
    MARKET_RESEARCH = """
당신은 글로벌 시장 조사 전문가입니다.
{company}의 {country} 시장 진출을 위한 시장 조사를 수행하세요.

## 조사 범위
1. TAM (Total Addressable Market) - 전체 시장 규모
2. 연간 성장률 (YoY)
3. 택배/물류 거래량
4. 평균 배송 비용 및 리드타임
5. 소비 행태 및 문화적 특성
6. 항만/공항/물류 인프라 현황

## 산출물 요구사항
다음 형식의 JSON을 반환하세요:
{{
    "metrics": {{
        "TAM": "구체적 금액 (예: $2.5B)",
        "성장률": "% YoY",
        "택배량": "건수/년",
        "평균 배송비": "금액",
        "리드타임": "일수"
    }},
    "why_now": "이 시장에 지금 진입해야 하는 이유를 1-2문장으로",
    "customer_segments": {{
        "high": "프리미엄 고객 세그먼트 설명",
        "mid": "중간 고객 세그먼트 설명",
        "low": "저가 고객 세그먼트 설명"
    }}
}}

## 가드레일
- 모든 수치는 출처를 명시할 것
- "Why Now"는 50단어 이내로 간결하게
- 도시 vs 비도시 수요 차이를 반드시 언급

## 예시
베트남의 경우:
- TAM: $2.5B (Statista 2024)
- 성장률: 15% YoY (Vietnam E-commerce Report)
- Why Now: "이커머스 급성장(35% YoY)과 중산층 확대(연 7% 증가)로 
   빠른 배송 수요 폭증. 정부의 물류 인프라 투자로 진입 장벽 완화."

지금 조사를 시작하세요.
"""

    # --------------------------------------------------------
    # 규제검토 에이전트
    # --------------------------------------------------------
    REGULATORY_REVIEW = """
당신은 국제 규제 및 법률 전문가입니다.
{company}의 {country} 시장 진출 시 준수해야 할 규제를 검토하세요.

## 검토 항목
1. 사업 라이선스 (택배업 등록, 창고업 허가 등)
2. 통관·관세 (HS코드, FTA, 관세율)
3. 데이터/개인정보 (GDPR, 국외 이전 규정)
4. 노동법 (라이더 고용, 최저임금)
5. 플랫폼 규제 (전자상거래법, 환불/반품)

## 등급 정의
- **MUST**: 법령상 의무사항, 미준수 시 영업 불가
- **SHOULD**: 강한 권고사항, 미준수 시 리스크 존재
- **NICE**: 선택사항, 경쟁력 강화 요소

## 상태 정의
- **PASS**: 요구사항 충족 (근거 확보)
- **WARN**: 부분 충족 또는 모호
- **TBD**: 적용 여부 미확인
- **NA**: 해당 없음

## 산출물 요구사항
다음 형식의 JSON을 반환하세요:
{{
    "checklist": [
        {{
            "item": "택배업 등록",
            "grade": "MUST",
            "state": "PASS",
            "evidence": "국토부 고시 제2024-123호 확인",
            "score_impact": 3  // MUST=3, SHOULD=2, NICE=0
        }},
        // ... 최소 10개 항목
    ],
    "coverage_score": 0.76,  // 자동 계산됨
    "risk_badge": "보통",  // 낮음/보통/높음
    "hold_flag": false  // MUST-FAIL 시 true
}}

## 커버리지 계산 공식
커버리지 = Σ(등급 가중치 × 상태점수) ÷ Σ(등급 가중치)

- 등급 가중치: MUST=3, SHOULD=2, NICE=0(제외)
- 상태 점수: PASS=1.0, WARN=0.5, TBD=0.0, NA=제외

## 페널티 규칙
- 커버리지 < 80% → 의사결정 점수 -20
- 가중 TBD 비율 ≥ 20% → 의사결정 점수 -5
- MUST 항목이 FAIL → 즉시 HOLD (hold_flag = true)

## 예시
베트남 택배업의 경우:
- 택배업 등록: MUST/PASS (Decree 163/2017/ND-CP)
- 개인정보 국외이전: MUST/TBD (DPA 협약 필요, 근거 미확보)
- 환불·반품 고지: SHOULD/PASS (Law on Consumer Protection)

지금 검토를 시작하세요.
"""

    # --------------------------------------------------------
    # 경쟁사 분석 에이전트
    # --------------------------------------------------------
    COMPETITOR_ANALYSIS = """
당신은 경쟁 전략 분석가입니다.
{country} 시장의 물류/택배 경쟁 환경을 분석하세요.

## 분석 항목
1. 주요 경쟁사 (현지 Top 3 + 글로벌 플레이어)
2. 각사의 가격대, 서비스 범위, 채널
3. 지역별 경쟁 밀집도
4. 화이트스페이스 (경쟁 갭) 식별

## 경쟁사 신호 정의
다음 중 2개 이상 해당 시 직접 경쟁사:
- 같은 고객 세그먼트 타깃
- 우리 오퍼와 대체 가능
- 같은 영업 채널 (RFP 겹침)

## 산출물 요구사항
{{
    "competitors": [
        {{
            "name": "회사명",
            "type": "현지/글로벌",
            "price_level": "고가/중가/저가",
            "service_scope": "국내/국제/풀필먼트/...",
            "geographic_focus": ["하노이", "호치민", "..."],
            "strengths": ["강점1", "강점2"],
            "weaknesses": ["약점1", "약점2"]
        }},
        // ... 5-10개사
    ],
    "whitespace_gaps": [
        "농촌 지역 당일배송 서비스 부재",
        "프리미엄 콜드체인 물류 미개척",
        "중소기업 전용 통합 플랫폼 없음"
    ],
    "competition_intensity": "높음/보통/낮음"
}}

## 화이트스페이스 기준
- 수요는 있으나 공급 부족
- 기존 업체의 서비스 품질 불만족
- 인프라는 있으나 활용 미흡

## 예시
베트남의 경우:
- 주요 경쟁사: Vietnam Post (공기업), Giao Hang Nhanh (민간 1위), 
  Ninja Van (동남아 강자)
- 화이트스페이스: 
  1) 메콩델타 당일배송 (인프라 있지만 업체 없음)
  2) 온도관리 필수 상품 (의약/화장품) B2B 물류
  3) 영세상인용 간편 통합 플랫폼

지금 분석을 시작하세요.
"""

    # --------------------------------------------------------
    # 파트너 발굴 에이전트
    # --------------------------------------------------------
    PARTNER_DISCOVERY = """
당신은 비즈니스 개발 전문가입니다.
{company}의 {country} 진출을 위한 핵심 파트너를 발굴하세요.

## 파트너 카테고리
1. 라스트마일 (배송 파트너)
2. 통관 브로커 (관세/통관 대행)
3. 창고/풀필먼트 (3PL)
4. 결제 게이트웨이
5. 시스템 통합/리셀러 (SI)
6. 플랫폼 파트너 (Shopee, Lazada 등)

## 파트너 선정 기준
- 우리의 핵심 성공요인(KSF) 보완
- 공동 KPI 설정 가능
- 수익 공유 모델 성립
- Plan B (대안) 존재

## 산출물 요구사항
{{
    "candidates": [
        {{
            "name": "파트너사명",
            "role": "라스트마일/통관/3PL/...",
            "rationale": "선정 이유 (1-2문장)",
            "kpis": ["공동 KPI1", "KPI2"],
            "revenue_model": "마진공유/리퍼럴/조인트세일즈",
            "alternative": "Plan B 업체명"
        }},
        // ... 3-5개사
    ],
    "poc_proposal": "PoC 제안서 3문단 초안",
    "priority_zones": ["우선 탐색 권역1", "권역2"]  // 경쟁 밀집 지역
}}

## PoC 제안서 구조
1단락: 배경 및 목표
2단락: 3개월 시범 운영 계획
3단락: 성공 지표 및 확장 로드맵

## 예시
베트남의 경우:
- VietPost: 국영우편, 전국 네트워크, 정부 신뢰도 → 초기 B2G 파트너
  (대안: Giao Hang Nhanh - 민간 1위)
- FPT Software: 베트남 SI 1위, 물류 경험 → 시스템 커스터마이징
  (대안: TMA Solutions)

지금 발굴을 시작하세요.
"""

    # --------------------------------------------------------
    # 리스크 시나리오 에이전트
    # --------------------------------------------------------
    RISK_SCENARIOS = """
당신은 리스크 관리 전문가입니다.
{company}의 {country} 진출 시 발생 가능한 리스크를 분석하세요.

## 리스크 카테고리
1. 규제 리스크 (법 개정, 집행 강화)
2. 시장 리스크 (수요 부진, 가격 경쟁)
3. 운영 리스크 (파트너 이탈, 품질 문제)
4. 재무 리스크 (환율, 자금 부족)
5. 평판 리스크 (사고, 불만)

## 평가 기준
- **가능성**: 높음/보통/낮음
- **영향**: 높음/보통/낮음
- 높음×높음 → 즉시 대응 필요

## 산출물 요구사항
{{
    "register": [
        {{
            "risk": "리스크 설명",
            "likelihood": "높음/보통/낮음",
            "impact": "높음/보통/낮음",
            "early_sign": "초기 징후 (KPI 임계치)",
            "mitigation": "완화 전략",
            "plan_b": "Plan B"
        }},
        // ... 5-10개
    ],
    "scenarios": {{
        "pessimistic": {{
            "월 거래량": "10K건",
            "수익": "-$50K",
            "조건": "경쟁 심화 + 규제 강화"
        }},
        "base": {{
            "월 거래량": "30K건",
            "수익": "$20K",
            "조건": "계획대로 진행"
        }},
        "optimistic": {{
            "월 거래량": "100K건",
            "수익": "$150K",
            "조건": "플랫폼 파트너십 성공"
        }}
    }}
}}

## 얼리 워닝 임계치 예시
- 리드타임 > 5일 (기준: 3일) → 물류 문제
- 반품율 > 10% (기준: 5%) → 품질 문제
- CAC > $50 (기준: $30) → 마케팅 비효율

## 예시
베트남 규제 리스크:
- 리스크: 개인정보보호법 강화로 DPA 없이 영업 불가
- 가능성: 보통 (정부 발표 없음)
- 영향: 높음 (서비스 중단)
- 초기 징후: 국회 법안 상정 뉴스
- 완화: DPA 사전 체결 + 현지 데이터센터 확보

지금 분석을 시작하세요.
"""

    # --------------------------------------------------------
    # 의사결정 에이전트
    # --------------------------------------------------------
    DECISION_MAKING = """
당신은 전략 의사결정 담당자입니다.
모든 분석 결과를 종합하여 Go/No-Go를 결정하세요.

## 입력 데이터
- 시장조사 결과
- 규제 커버리지 및 리스크
- 경쟁 강도
- 파트너 가용성
- 리스크 시나리오

## 의사결정 룰
기본 점수: 70점

**가점**
- 규제 커버리지 ≥ 90% → +10
- 실행가능성 높음 (파트너 2개 이상) → +20

**감점**
- 규제 커버리지 < 80% → -20
- 가중 TBD 비율 ≥ 20% → -5
- 경쟁 강도 높음 & 화이트스페이스 없음 → -10

**즉시 HOLD**
- MUST 규제 FAIL → hold_flag = true

**최종 판정**
- 점수 ≥ 60 → "진행(추천)"
- 점수 < 60 → "보류 (추가조사 2개 제시)"

## 산출물 요구사항
{{
    "decision": "진행(추천) / 보류",
    "rationale": "한 문장으로 근거",
    "final_score": 72,
    "scorecard": {{
        "시장 매력도": 85,
        "규제 리스크": 65,
        "경쟁 강도": 60,
        "실행 가능성": 75,
        "파트너 가용성": 80
    }},
    "next_steps": [
        "액션1 (기한)",
        "액션2 (기한)",
        // ... 보류 시 추가조사 2개만
    ]
}}

## 예시
진행 케이스:
- 점수: 72 (규제 커버리지 76% → -20, 파트너 2개 → +20, 기본 70)
- 근거: "시장 성장성(85)과 실행 가능성(75) 높음. 규제는 DPA 체결로 해결 가능"

보류 케이스:
- 점수: 45
- 근거: "MUST 규제(DPA) 미확보 및 경쟁 밀집으로 진입 장벽 높음"
- Next Steps:
  1. DPA 협약 체결 가능성 재검토 (2주)
  2. 대안 시장(필리핀) 검토 (1개월)

지금 결정하세요.
"""


# ============================================================
# 3. 보고서 커스터마이징 가이드
# ============================================================

class CustomizationGuide:
    """보고서 스타일 및 내용 커스터마이징"""
    
    @staticmethod
    def change_colors():
        """색상 변경 예시"""
        instructions = """
        HTML 보고서의 색상을 변경하려면:
        
        1. report_templates.py 파일 열기
        2. <style> 태그 내부의 색상 코드 수정:
        
        ```css
        /* 기본 그라데이션 (파란색 → 보라색) */
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* 초록색 테마로 변경 */
        .gradient-bg {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }
        
        /* 빨간색 테마로 변경 */
        .gradient-bg {
            background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
        }
        ```
        
        3. 배지 색상도 마찬가지로 RGBColor 수정
        """
        return instructions
    
    @staticmethod
    def add_custom_section():
        """커스텀 섹션 추가 예시"""
        instructions = """
        새로운 섹션을 추가하려면:
        
        1. report_templates.py에 메서드 추가:
        
        ```python
        @staticmethod
        def _generate_custom_section(data: Dict) -> str:
            return f'''
                <div class="card p-8">
                    <h2 class="section-title">🎯 커스텀 섹션</h2>
                    <p>{data.get('content', '내용 없음')}</p>
                </div>
            '''
        ```
        
        2. generate_html_report() 메서드 내부에 추가:
        
        ```python
        <!-- 기존 섹션들 -->
        {cls._generate_custom_section(state.get('custom_data', {}))}
        <!-- 다음 섹션 -->
        ```
        
        3. State에 custom_data 필드 추가
        """
        return instructions
    
    @staticmethod
    def change_fonts():
        """폰트 변경 예시"""
        instructions = """
        폰트를 변경하려면:
        
        HTML: <style> 태그에서
        ```css
        @import url('https://fonts.googleapis.com/css2?family=원하는폰트&display=swap');
        
        body {
            font-family: '원하는폰트', sans-serif;
        }
        ```
        
        DOCX: docx_report_generator.py의 _setup_styles()에서
        ```python
        font.name = 'Malgun Gothic'  # 원하는 폰트
        ```
        """
        return instructions


# ============================================================
# 4. 통합 예시 - 전체 플로우
# ============================================================

def example_full_workflow():
    """전체 워크플로우 실행 예시"""
    
    from langgraph.graph import StateGraph, END
    from typing_extensions import TypedDict
    from typing import Annotated
    
    # State 정의
    class FullState(TypedDict):
        company: str
        country: str
        messages: Annotated[list, add_messages]
        market_summary: Dict
        regulatory_data: Dict
        competitor_data: Dict
        partner_data: Dict
        risk_data: Dict
        decision_data: Dict
        visualizations: Dict[str, str]
        html_report_path: str
        docx_report_path: str
        report_generated: bool
        hold_flag: bool
    
    # 각 에이전트 (실제로는 LLM 호출 포함)
    def market_research(state):
        # TODO: LLM에 PromptTemplates.MARKET_RESEARCH 전달
        state["market_summary"] = {"metrics": {}, "why_now": "..."}
        return state
    
    def regulatory_review(state):
        # TODO: LLM에 PromptTemplates.REGULATORY_REVIEW 전달
        state["regulatory_data"] = {"coverage_score": 0.8, ...}
        return state
    
    def competitor_analysis(state):
        # TODO: LLM에 PromptTemplates.COMPETITOR_ANALYSIS 전달
        state["competitor_data"] = {"whitespace_gaps": [...]}
        return state
    
    def partner_discovery(state):
        # TODO: LLM에 PromptTemplates.PARTNER_DISCOVERY 전달
        state["partner_data"] = {"candidates": [...]}
        return state
    
    def risk_scenarios(state):
        # TODO: LLM에 PromptTemplates.RISK_SCENARIOS 전달
        state["risk_data"] = {"register": [...]}
        return state
    
    def decision_making(state):
        # TODO: LLM에 PromptTemplates.DECISION_MAKING 전달
        state["decision_data"] = {"decision": "진행", ...}
        return state
    
    # 보고서 생성은 이미 구현됨
    from report_agent import generate_report_agent
    
    # 그래프 구성
    workflow = StateGraph(FullState)
    workflow.add_node("market_research", market_research)
    workflow.add_node("regulatory_review", regulatory_review)
    workflow.add_node("competitor_analysis", competitor_analysis)
    workflow.add_node("partner_discovery", partner_discovery)
    workflow.add_node("risk_scenarios", risk_scenarios)
    workflow.add_node("decision_making", decision_making)
    workflow.add_node("report_generation", generate_report_agent)
    
    # 엣지
    workflow.set_entry_point("market_research")
    workflow.add_edge("market_research", "regulatory_review")
    workflow.add_edge("regulatory_review", "competitor_analysis")
    workflow.add_edge("competitor_analysis", "partner_discovery")
    workflow.add_edge("partner_discovery", "risk_scenarios")
    workflow.add_edge("risk_scenarios", "decision_making")
    workflow.add_edge("decision_making", "report_generation")
    workflow.add_edge("report_generation", END)
    
    app = workflow.compile()
    
    # 실행
    initial_state = {
        "company": "스타트업A",
        "country": "베트남",
        "messages": [],
        # ... 나머지 초기화
    }
    
    result = app.invoke(initial_state)
    
    print(f"✅ 보고서 생성 완료!")
    print(f"   HTML: {result['html_report_path']}")
    print(f"   DOCX: {result['docx_report_path']}")


# ============================================================
# 5. 자주 묻는 질문 (FAQ)
# ============================================================

FAQ = """
Q1. 보고서에 로고를 추가하고 싶어요.
A1. HTML: <img src="data:image/png;base64,..." 방식으로 삽입
    DOCX: doc.add_picture(logo_path) 사용

Q2. 보고서를 PDF로도 받고 싶어요.
A2. HTML을 생성한 후 wkhtmltopdf 또는 playwright로 PDF 변환:
    ```bash
    playwright chromium --headless --print-to-pdf report.pdf report.html
    ```

Q3. 차트/지도가 안 나와요.
A3. visualizations 딕셔너리에 올바른 경로가 있는지 확인:
    ```python
    state["visualizations"] = {
        "demand_heatmap": "/mnt/user-data/outputs/heatmap.png",
        ...
    }
    ```

Q4. 여러 국가를 한 번에 분석하고 싶어요.
A4. 루프로 실행:
    ```python
    countries = ["베트남", "태국", "인도네시아"]
    for country in countries:
        state["country"] = country
        result = app.invoke(state)
    ```

Q5. 보고서 생성이 느려요.
A5. 이미지 최적화 (해상도 낮추기) 또는 병렬 처리 고려

Q6. 특정 섹션만 업데이트하고 싶어요.
A6. 해당 에이전트만 재실행 후 보고서 재생성
"""


if __name__ == "__main__":
    print("=" * 70)
    print(" 다국적 시장 진출 전략 보고서 생성 시스템 - 완전 가이드")
    print("=" * 70)
    print()
    print("📚 이 파일은 보고서 생성 시스템의 사용법을 설명합니다.")
    print()
    print("주요 컴포넌트:")
    print("  1. report_templates.py - HTML 보고서 생성기")
    print("  2. docx_report_generator.py - DOCX 보고서 생성기")
    print("  3. report_agent.py - LangGraph 통합 에이전트")
    print("  4. 이 파일 - 프롬프트 템플릿 & 가이드")
    print()
    print("=" * 70)
    print()
    print("📋 프롬프트 템플릿 목록:")
    print("  - MARKET_RESEARCH")
    print("  - REGULATORY_REVIEW")
    print("  - COMPETITOR_ANALYSIS")
    print("  - PARTNER_DISCOVERY")
    print("  - RISK_SCENARIOS")
    print("  - DECISION_MAKING")
    print()
    print("각 템플릿은 PromptTemplates 클래스에서 확인하세요.")
    print()
    print("=" * 70)
