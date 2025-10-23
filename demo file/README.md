# 전략 리포트 생성 데모 시스템

**독립 실행 가능한 HTML + DOCX 리포트 생성기**

> 메인 파이프라인과 독립적으로 실행되는 리포트 템플릿 및 생성기
>
> 빠른 프로토타이핑 및 리포트 포맷 테스트용

---

## 🎯 개요

이 시스템은 다국적 시장 진출 의사결정을 위한 **전문적이고 예쁜 전략 보고서**를 자동 생성합니다.

### 주요 특징

✨ **2가지 형식 지원**
- **HTML**: 웹에서 바로 확인, Tailwind CSS로 아름다운 디자인
- **DOCX**: Word에서 편집 가능, 인쇄 및 공유 최적화

📊 **완전한 전략 분석**
- 시장조사 (TAM, 성장률, Why Now)
- 규제검토 (커버리지 점수, 리스크 배지)
- 경쟁사 분석 (화이트스페이스 발굴)
- 파트너 발굴 (후보사 + PoC 제안서)
- 리스크 시나리오 (비관/기준/낙관)
- 의사결정 (Go/No-Go, 점수 계산)

🎨 **전문적인 디자인**
- 그라데이션 헤더
- 인터랙티브 카드
- 프로그레스 바
- 색상 코딩 (리스크 배지, 의사결정 배너)
- 반응형 레이아웃

---

## 📁 파일 구조

```
demo file/
├── report_templates.py          # HTML 보고서 템플릿 생성기 (Tailwind CSS)
├── docx_report_generator.py     # DOCX 보고서 생성기 (python-docx)
├── report_agent.py              # LangGraph 통합 가능한 에이전트
├── report_guide.py              # 프롬프트 템플릿 & 가이드
├── test_report_generation.py    # 독립 테스트 스크립트 (샘플 데이터 포함)
└── README.md                    # 이 문서

# 실행 시 생성되는 출력물 (프로젝트 루트에 생성)
output_demo_*.html               # 데모 HTML 리포트
output_demo_*.docx               # 데모 DOCX 리포트
```

**메인 파이프라인과의 차이점**:
- 메인 파이프라인: `src/app.py` → 전체 에이전트 실행 → `outputs/{Company}_{Country}/`
- 데모 시스템: `demo file/test_report_generation.py` → 샘플 데이터만 사용 → 루트에 출력

---

## 🚀 빠른 시작

### 1. 독립 실행 (테스트)

```bash
# 프로젝트 루트에서
cd "demo file"
python test_report_generation.py
```

**실행 결과**:
- 샘플 데이터로 HTML + DOCX 보고서를 즉시 생성
- 출력 위치: 프로젝트 루트 (`../output_demo_*.html`, `../output_demo_*.docx`)
- 의존성: `python-docx` (메인 `requirements.txt`에 포함)

**주의사항**:
- 메인 파이프라인 (`src/app.py`)과 완전히 독립적
- LangGraph 또는 에이전트 실행 없음
- 샘플 데이터만 사용하므로 빠른 테스트에 적합

### 2. 코드에서 사용

```python
from report_templates import StrategyReportTemplate
from docx_report_generator import DocxReportGenerator

# 데이터 준비
data = {
    "company": "스타트업A",
    "country": "베트남",
    "market_summary": {...},
    "regulatory_data": {...},
    # ... 기타
}

# HTML 생성
html = StrategyReportTemplate.generate_html_report(**data)
with open("report.html", "w", encoding="utf-8") as f:
    f.write(html)

# DOCX 생성
DocxReportGenerator.generate_full_report(**data, output_path="report.docx")
```

### 3. LangGraph 워크플로우 통합

```python
from report_agent import generate_report_agent
from langgraph.graph import StateGraph, END

workflow = StateGraph(MarketEntryState)

# 기존 에이전트들...
workflow.add_node("market_research", market_research_agent)
workflow.add_node("regulatory_review", regulatory_review_agent)
# ...

# 보고서 생성 에이전트 추가
workflow.add_node("report_generation", generate_report_agent)

# 마지막 단계로 연결
workflow.add_edge("decision_making", "report_generation")
workflow.add_edge("report_generation", END)

app = workflow.compile()
```

---

## 📊 데이터 구조

### State 정의

```python
from typing import Dict, TypedDict

class ReportState(TypedDict):
    company: str          # 회사명
    country: str          # 진출 국가
    
    # 각 섹션별 데이터
    market_summary: Dict  # 시장 조사
    regulatory_data: Dict # 규제 검토
    competitor_data: Dict # 경쟁사 분석
    partner_data: Dict    # 파트너 발굴
    risk_data: Dict       # 리스크 시나리오
    decision_data: Dict   # 의사결정
    
    # 시각화 (옵션)
    visualizations: Dict[str, str]  # {name: filepath}
    
    # 출력
    html_report_path: str
    docx_report_path: str
```

### 데이터 예시

<details>
<summary>📄 market_summary 예시</summary>

```python
market_summary = {
    "metrics": {
        "TAM": "$2.5B",
        "성장률": "15% YoY",
        "택배량": "500M건/년",
        "평균 배송비": "$2.50",
        "리드타임": "2-3일"
    },
    "why_now": "이커머스 급성장과 중산층 확대로 진입 최적기"
}
```
</details>

<details>
<summary>✅ regulatory_data 예시</summary>

```python
regulatory_data = {
    "coverage_score": 0.76,  # 커버리지 (0.0~1.0)
    "risk_badge": "보통",     # "낮음"/"보통"/"높음"
    "checklist": [
        {
            "item": "택배업 등록",
            "grade": "MUST",     # MUST/SHOULD/NICE
            "state": "PASS",     # PASS/WARN/TBD/NA
            "evidence": "국토부 고시 확인"
        },
        # ... 더 많은 항목
    ]
}
```
</details>

<details>
<summary>🗺️ competitor_data 예시</summary>

```python
competitor_data = {
    "whitespace_gaps": [
        "농촌 지역 당일배송 서비스 부재",
        "프리미엄 콜드체인 물류 미개척",
        "중소기업 전용 통합 플랫폼 없음"
    ]
}
```
</details>

<details>
<summary>🤝 partner_data 예시</summary>

```python
partner_data = {
    "candidates": [
        {
            "name": "VietPost",
            "role": "라스트마일",
            "rationale": "전국 네트워크",
            "alternative": "GHN"
        },
        # ... 더 많은 파트너
    ],
    "poc_proposal": "3개월 시범 운영 계획..."
}
```
</details>

<details>
<summary>⚠️ risk_data 예시</summary>

```python
risk_data = {
    "register": [
        {
            "risk": "규제 변경",
            "likelihood": "보통",
            "impact": "높음",
            "early_sign": "정부 발표",
            "mitigation": "로비스트 고용"
        },
        # ...
    ],
    "scenarios": {
        "pessimistic": {"월 거래량": "10K건", "수익": "-$50K"},
        "base": {"월 거래량": "30K건", "수익": "$20K"},
        "optimistic": {"월 거래량": "100K건", "수익": "$150K"}
    }
}
```
</details>

<details>
<summary>🎯 decision_data 예시</summary>

```python
decision_data = {
    "decision": "진행(추천)",
    "rationale": "시장 성장성 높고 리스크 관리 가능",
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
        "VietPost MOU (1개월)",
        # ...
    ]
}
```
</details>

---

## 🎨 커스터마이징

### 색상 변경

`report_templates.py`의 CSS 섹션:

```css
/* 기본 그라데이션 (파란색) */
.gradient-bg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 초록색 테마 */
.gradient-bg {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

/* 빨간색 테마 */
.gradient-bg {
    background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
}
```

### 로고 추가

HTML 헤더 섹션에:

```python
<div class="gradient-bg ...">
    <img src="data:image/png;base64,{logo_base64}" class="h-12 mb-4">
    <h1>...</h1>
</div>
```

DOCX 표지에:

```python
def add_cover_page(self, company, country, logo_path=None):
    if logo_path:
        self.doc.add_picture(logo_path, width=Inches(2))
    # ...
```

### 섹션 추가

`report_templates.py`에 메서드 추가:

```python
@staticmethod
def _generate_custom_section(data: Dict) -> str:
    return f'''
        <div class="card p-8">
            <h2 class="section-title">🎯 커스텀 섹션</h2>
            <p>{data.get('content')}</p>
        </div>
    '''
```

`generate_html_report()`에서 호출:

```python
# 기존 섹션들...
{cls._generate_custom_section(state.get('custom_data', {}))}
# ...
```

---

## 📋 프롬프트 템플릿

각 에이전트용 프롬프트는 `report_guide.py`의 `PromptTemplates` 클래스에 정의되어 있습니다:

- `MARKET_RESEARCH`: 시장 조사 프롬프트
- `REGULATORY_REVIEW`: 규제 검토 프롬프트
- `COMPETITOR_ANALYSIS`: 경쟁사 분석 프롬프트
- `PARTNER_DISCOVERY`: 파트너 발굴 프롬프트
- `RISK_SCENARIOS`: 리스크 시나리오 프롬프트
- `DECISION_MAKING`: 의사결정 프롬프트

### 사용 예시

```python
from report_guide import PromptTemplates

prompt = PromptTemplates.MARKET_RESEARCH.format(
    company="스타트업A",
    country="베트남"
)

# LLM에 전달
response = llm.invoke(prompt)
```

---

## 🔧 의존성

**이미 메인 프로젝트 requirements.txt에 포함됨**:
```bash
# 프로젝트 루트에서 이미 설치했다면 추가 설치 불필요
pip install -r requirements.txt
```

**필수 의존성**:
- `python-docx>=1.1.0`: DOCX 리포트 생성
- Python 3.8+

**선택적 의존성**:
- Tailwind CSS: HTML에 CDN으로 포함 (별도 설치 불필요)
- LangGraph: 메인 파이프라인과 통합 시 필요 (데모 단독 실행 시 불필요)

---

## 📚 주요 기능 상세

### 1. 규제 커버리지 계산

기획서의 공식을 정확히 구현:

```
커버리지 = Σ(등급 가중치 × 상태점수) ÷ Σ(등급 가중치)

등급 가중치:
- MUST: 3
- SHOULD: 2
- NICE: 0 (제외)

상태 점수:
- PASS: 1.0
- WARN: 0.5
- TBD: 0.0
- NA: 제외
```

### 2. 의사결정 스코어

```python
기본 점수: 70

가점:
- 규제 커버리지 ≥ 90% → +10
- 파트너 2개 이상 → +20

감점:
- 규제 커버리지 < 80% → -20
- 가중 TBD 비율 ≥ 20% → -5
- 경쟁 강도 높음 & 갭 없음 → -10

즉시 HOLD:
- MUST 규제 FAIL → hold_flag = true

최종 판정:
- 점수 ≥ 60 → "진행(추천)"
- 점수 < 60 → "보류"
```

### 3. 시각화 통합

이미지를 base64로 인코딩하여 HTML에 삽입:

```python
visualizations = {
    "demand_heatmap": "/path/to/heatmap.png",
    "customs_flow": "/path/to/customs.png",
    "competition_density": "/path/to/density.png",
    "positioning": "/path/to/positioning.png",
    "partner_map": "/path/to/partners.png"
}
```

---

## 🎯 실전 예시

### 전체 워크플로우

```python
# 1. 데이터 수집 (각 에이전트 실행)
market_data = market_research_agent(company, country)
regulatory_data = regulatory_review_agent(company, country)
# ... 기타 에이전트

# 2. State 구성
state = {
    "company": company,
    "country": country,
    "market_summary": market_data,
    "regulatory_data": regulatory_data,
    # ...
}

# 3. 보고서 생성
result = generate_report_agent(state)

# 4. 결과 확인
print(f"HTML: {result['html_report_path']}")
print(f"DOCX: {result['docx_report_path']}")
```

---

## 💡 팁 & 베스트 프랙티스

### 1. 프롬프트 작성
- 각 에이전트에게 **구조화된 JSON** 출력 요구
- **예시 포함**으로 품질 향상
- **가드레일 명시**로 일관성 확보

### 2. 데이터 검증
```python
def validate_regulatory_data(data):
    assert 0 <= data["coverage_score"] <= 1
    assert data["risk_badge"] in ["낮음", "보통", "높음"]
    for item in data["checklist"]:
        assert item["grade"] in ["MUST", "SHOULD", "NICE"]
        assert item["state"] in ["PASS", "WARN", "TBD", "NA"]
```

### 3. 에러 핸들링
```python
try:
    result = generate_report_agent(state)
except Exception as e:
    logger.error(f"보고서 생성 실패: {e}")
    # 부분 보고서라도 생성 시도
```

### 4. 성능 최적화
- 이미지 해상도 조절 (DPI 300 → 150)
- 병렬 처리 (멀티 국가 분석 시)

---

## 🐛 트러블슈팅

### Q1. 한글이 깨져요
**A:** DOCX의 경우 폰트 설정 확인:
```python
font.name = 'Noto Sans KR'  # 또는 'Malgun Gothic'
```

### Q2. 이미지가 안 보여요
**A:** 파일 경로와 권한 확인:
```python
assert Path(image_path).exists()
assert os.access(image_path, os.R_OK)
```

### Q3. HTML이 너무 커요
**A:** 이미지를 외부 링크로 변경:
```html
<img src="/outputs/image.png">  <!-- base64 대신 -->
```

### Q4. PDF로 변환하고 싶어요
**A:** playwright 사용:
```bash
playwright chromium --headless --print-to-pdf report.pdf report.html
```

---

## 📈 로드맵

- [x] HTML + DOCX 기본 템플릿
- [x] 규제 커버리지 계산
- [x] 의사결정 스코어링
- [x] 프롬프트 템플릿
- [ ] 시각화 자동 생성 (matplotlib/plotly)
- [ ] PDF 직접 생성
- [ ] 다국어 지원 (영어, 중국어)
- [ ] 클라우드 저장 (S3, GCS)

---

## 📞 문의

이 시스템은 기획서 v1.0을 기반으로 구현되었습니다.
추가 기능이나 개선 사항은 이슈로 등록해주세요.

---

## 📄 라이선스

MIT License

---

<div align="center">
  <strong>Made with ❤️ for Global Market Entry</strong>
  <br>
  <sub>Powered by LangGraph & Anthropic Claude</sub>
</div>
