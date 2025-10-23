"""
독립 실행 테스트 - LangGraph 없이 보고서만 생성
"""

import sys
sys.path.append('/home/claude')

from report_templates import StrategyReportTemplate
from docx_report_generator import DocxReportGenerator
from pathlib import Path

# 테스트 데이터 (기획서 예시와 동일)
test_data = {
    "company": "스타트업A (한국 물류 SaaS)",
    "country": "베트남",
    "market_summary": {
        "metrics": {
            "TAM (전체 시장)": "$2.5B",
            "연간 성장률": "15% YoY",
            "연간 택배량": "500M건",
            "평균 배송비": "$2.50",
            "평균 리드타임": "2-3일",
            "이커머스 성장": "35% YoY",
            "중산층 비율": "30% (연 7% 증가)"
        },
        "why_now": "이커머스가 급성장(35% YoY)하며 중산층이 확대(연 7% 증가)되면서 빠른 배송 수요가 폭증하고 있습니다. 정부의 물류 인프라 투자로 진입 장벽이 완화되어 지금이 최적의 진입 시기입니다."
    },
    "regulatory_data": {
        "coverage_score": 0.76,
        "risk_badge": "보통",
        "checklist": [
            {
                "item": "택배업 등록 (Postal Service License)",
                "grade": "MUST",
                "state": "PASS",
                "evidence": "Decree 163/2017/ND-CP, 국토부 고시 확인"
            },
            {
                "item": "개인정보 국외이전 (DPA/SCC)",
                "grade": "MUST",
                "state": "TBD",
                "evidence": "Personal Data Protection Decree 13/2023 해당, 근거 미확보"
            },
            {
                "item": "전자상거래 환불·반품 고지",
                "grade": "SHOULD",
                "state": "PASS",
                "evidence": "Law on Consumer Protection 2010, 공정위 가이드라인"
            },
            {
                "item": "표시·광고 규제 준수",
                "grade": "SHOULD",
                "state": "WARN",
                "evidence": "업계 블로그만 존재, 공식 문서 미확인"
            },
            {
                "item": "FTZ (자유무역지대) 관세 특례",
                "grade": "NICE",
                "state": "NA",
                "evidence": "선택사항, 해당 없음"
            },
            {
                "item": "창고업 허가 (Warehousing License)",
                "grade": "MUST",
                "state": "PASS",
                "evidence": "Decree 163/2017/ND-CP Article 15"
            },
            {
                "item": "라이더 안전교육/보험",
                "grade": "SHOULD",
                "state": "WARN",
                "evidence": "Labor Code 요구사항 있으나 상세 기준 모호"
            }
        ]
    },
    "competitor_data": {
        "whitespace_gaps": [
            "🌾 농촌 지역 당일배송 서비스 부재 - 메콩델타 인프라는 있으나 업체 없음",
            "❄️ 프리미엄 콜드체인 물류 미개척 - 의약품/화장품 B2B 수요 높음",
            "🏪 중소기업 전용 통합 물류 플랫폼 없음 - 영세상인 페인포인트 존재"
        ]
    },
    "partner_data": {
        "candidates": [
            {
                "name": "Vietnam Post (VietPost)",
                "role": "라스트마일 배송",
                "rationale": "국영우편 전국 네트워크 보유, B2G 신뢰도 높음",
                "alternative": "Giao Hang Nhanh (GHN) - 민간 1위"
            },
            {
                "name": "FPT Software",
                "role": "시스템 통합 (SI)",
                "rationale": "베트남 IT 1위, 물류 프로젝트 경험 풍부",
                "alternative": "TMA Solutions"
            },
            {
                "name": "GlobalPort Logistics",
                "role": "통관 브로커",
                "rationale": "하이퐁/호치민 항만 특화, 빠른 통관 처리",
                "alternative": "Saigon Newport"
            },
            {
                "name": "Shopee Vietnam",
                "role": "플랫폼 파트너",
                "rationale": "베트남 이커머스 1위, 판매자 물류 수요 대량",
                "alternative": "Lazada Vietnam"
            }
        ],
        "poc_proposal": """
**1단계: 호치민 시범 운영 (3개월)**
- 목표: 월 10K 건, 배송 성공률 95% 이상
- 파트너: VietPost (라스트마일) + FPT (시스템)
- 주요 고객: Shopee 판매자 50명

**2단계: 하노이 확장 (3개월)**
- 목표: 월 30K 건, 2개 도시 커버
- 추가 파트너: 하노이 창고 3PL

**3단계: 전국 네트워크 (6개월)**
- 목표: 월 100K 건, Top 5 도시 커버
- 콜드체인 서비스 출시
"""
    },
    "risk_data": {
        "register": [
            {
                "risk": "개인정보보호법 강화로 DPA 없이 영업 불가",
                "likelihood": "보통",
                "impact": "높음",
                "early_sign": "국회 법안 상정 뉴스, 정부 발표",
                "mitigation": "DPA 사전 체결 + 현지 데이터센터 확보"
            },
            {
                "risk": "주요 파트너 (VietPost) 이탈 또는 SLA 미달",
                "likelihood": "낮음",
                "impact": "높음",
                "early_sign": "월 배송 성공률 < 90%",
                "mitigation": "GHN과 백업 계약 체결"
            },
            {
                "risk": "현지 경쟁사 (GHN, Ninja Van) 가격 공세",
                "likelihood": "높음",
                "impact": "보통",
                "early_sign": "시장 점유율 정체, 이탈율 증가",
                "mitigation": "프리미엄 서비스 (콜드체인) 차별화"
            },
            {
                "risk": "환율 변동 (VND/USD) 리스크",
                "likelihood": "보통",
                "impact": "보통",
                "early_sign": "환율 ±10% 이상 변동",
                "mitigation": "헷징 계약 + 현지 통화 수익 확대"
            }
        ],
        "scenarios": {
            "pessimistic": {
                "월 거래량": "10K건",
                "월 수익": "-$50K",
                "조건": "경쟁 심화 + 규제 강화 + 파트너 이탈"
            },
            "base": {
                "월 거래량": "30K건",
                "월 수익": "+$20K",
                "조건": "계획대로 진행, 시범 운영 성공"
            },
            "optimistic": {
                "월 거래량": "100K건",
                "월 수익": "+$150K",
                "조건": "Shopee 전략적 파트너십 + 콜드체인 조기 성공"
            }
        }
    },
    "decision_data": {
        "decision": "진행 (추천)",
        "rationale": "시장 성장성(85점)과 실행 가능성(75점)이 높고, 규제 리스크는 DPA 체결로 관리 가능한 수준입니다. 농촌/콜드체인 화이트스페이스가 명확하여 차별화 가능합니다.",
        "final_score": 72,
        "scorecard": {
            "시장 매력도": 85,
            "규제 리스크": 65,
            "경쟁 강도": 60,
            "실행 가능성": 75,
            "파트너 가용성": 80
        },
        "next_steps": [
            "1️⃣ DPA 협약 체결 가능성 재검토 및 현지 법무법인 미팅 (2주 이내)",
            "2️⃣ VietPost와 MOU 체결 협의 시작 (1개월 이내)",
            "3️⃣ FPT Software와 시스템 통합 PoC 제안서 작성 (2주 이내)",
            "4️⃣ 호치민 파일럿 준비: 파트너 선정 및 창고 확보 (2개월 이내)",
            "5️⃣ Shopee Vietnam 비즈니스 개발팀 컨택 (1개월 이내)"
        ]
    },
    "visualizations": {}  # 실제로는 PNG 경로 포함
}

print("=" * 70)
print("📊 다국적 시장 진출 전략 보고서 생성 테스트")
print("=" * 70)
print()

output_dir = Path("/mnt/user-data/outputs")
output_dir.mkdir(parents=True, exist_ok=True)

company_safe = test_data["company"].split()[0]
country_safe = test_data["country"]

html_path = output_dir / f"strategy_report_{company_safe}_{country_safe}_DEMO.html"
docx_path = output_dir / f"strategy_report_{company_safe}_{country_safe}_DEMO.docx"

print("1️⃣ HTML 보고서 생성 중...")
html_content = StrategyReportTemplate.generate_html_report(
    company=test_data["company"],
    country=test_data["country"],
    market_summary=test_data["market_summary"],
    regulatory_data=test_data["regulatory_data"],
    competitor_data=test_data["competitor_data"],
    partner_data=test_data["partner_data"],
    risk_data=test_data["risk_data"],
    decision_data=test_data["decision_data"],
    visualizations=test_data["visualizations"]
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"   ✅ HTML 저장 완료: {html_path}")
print()

print("2️⃣ DOCX 보고서 생성 중...")
DocxReportGenerator.generate_full_report(
    company=test_data["company"],
    country=test_data["country"],
    market_summary=test_data["market_summary"],
    regulatory_data=test_data["regulatory_data"],
    competitor_data=test_data["competitor_data"],
    partner_data=test_data["partner_data"],
    risk_data=test_data["risk_data"],
    decision_data=test_data["decision_data"],
    visualizations=test_data["visualizations"],
    output_path=str(docx_path)
)

print()
print("=" * 70)
print("✅ 테스트 보고서 생성 완료!")
print("=" * 70)
print()
print(f"📊 HTML 보고서: {html_path}")
print(f"📄 DOCX 보고서: {docx_path}")
print()
print("💡 Tip:")
print("  - HTML: 웹 브라우저에서 바로 확인 (시각적으로 예쁨)")
print("  - DOCX: Microsoft Word에서 편집 가능 (인쇄/공유 용이)")
print()
print("=" * 70)
