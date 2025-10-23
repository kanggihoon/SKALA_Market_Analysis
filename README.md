# 다국적 시장 진출 전략 에이전트 (Agentic Market Entry)

기획서(v1.0)를 기준으로, 회사×국가 단위의 전략 카드를 자동 생성하고 최종 Word 리포트(Executive 포함)를 산출하는 파이프라인입니다. 핵심 노드(시장/규제/경쟁/GTM 팬아웃→팬인/파트너/리스크/의사결정)를 순차/병렬로 실행하며, 각 케이스의 수치·문구·지도·표가 모두 상호 상이하게 생성되도록 설계되었습니다.

본 README는 “기획서 기준으로 구현된 것 vs. 미구현/보완 예정 항목”을 명확히 구분합니다.

---

## 1) 구현 현황 (기획서 대비)

구현됨
- Executive/Decision
  - 규제 커버리지 규칙 반영(+10/0/−20 및 TBD −5, MUST‑FAIL 즉시 HOLD)
  - 각 케이스별 상이한 최종 점수 및 사유 문장
- Market
  - Why Now 1문장 + 핵심 지표 5개(TAM, CAGR, Ecom Penetration, Infra Score, Avg Ship Cost)
  - PNG 경로 표기, 차트 이미지(01_market_summary_*.png) 생성
  - 케이스별 오버라이드: `data/market_overrides/{Company}_{Country}.json`
- Regulation
  - Coverage/TBD/Blocker, MUST/SHOULD/NICE 요약
  - 통관·관세 Flow(02_customs_flow_*.png) 경로 표기
- Competition
  - 화이트스페이스 3개(문구 상이), 지도 경로 표기(map_*.png)
  - 경쟁사 CSV(`data/rag_corpus/competition/*.csv`) 읽어 카테고리별 색상 마커/범례 반영, DOCX 표로 요약
  - 히트맵(03_competition_heatmap_*.png) + 마커 지도 보존(map_*.png)
- GTM (팬아웃→팬인)
  - high/mid/low 세그먼트 카드 3개(ICP/Offer/Price/Channel/KPI)
  - 세그먼트 스코어 3개 “모두 상이” 보장 (결코 동일값 3개 아님)
  - 팬인 결과(선택 세그먼트 + 선정 이유 1문장)
- Partners
  - 후보 3개 이상 + 역할/우선순위 상이, 지도(04_partner_map_*.png) 경로 표기
- Risks
  - 케이스별 2개 이상, 가능성×영향/완화책/트리거 기술
- Decision Scorecard
  - base, coverage_adj, tbd_adj, blocker_flag, competition_adj, partner_adj, gtm_adj, final 구조로 표기
- 최종 리포트(DOCX)
  - 케이스별 섹션(## 제목), 표/불릿/배지(간단 배경색) 적용, 4개 이미지/경로 표기
  - Evidence 블록(각 섹션 최소 2행, URL+date) 생성
- 검증 스크립트
  - `tools/validate_report.py` 제공: 규격 위반(반복 coverage, 맵/차트 경로 누락, 동일 점수 3개, MUST‑FAIL/Decision 불정합 등) 검출

보완 예정
- Evidence 블록의 실제 출처 연결: RAG/크롤러와 접속해 URL/발행일 자동 수집
- 지도 확대/색상 팔레트/라벨 튜닝(환경 변수 노출 범위 확대)
- 표 스타일(Word 탭룰) 고급 서식 및 브랜드 테마 적용
- GTM 스코어링 가중치 외부 설정/설명 테이블 노출

---

## 2) 폴더 구조

```
agentic-market-entry/
├─ src/
│  ├─ app.py                         # CLI 엔트리 (phase1/full)
│  ├─ state_schema.py                # Pydantic 스키마
│  ├─ agents/                        # 노드(시장/규제/경쟁/GTM/파트너/리스크/리포트)
│  ├─ graph/build_graph.py           # 파이프라인(직렬+병렬) 및 리포트 생성
│  ├─ viz/                           # 차트/지도 유틸
│  └─ utils/                         # 경쟁사 CSV 로더, 인덱서 등
├─ data/
│  ├─ companies.json                 # 입력 메타(3개 기업)
│  ├─ rag_corpus/competition/*.csv   # 경쟁사 CSV (company,target_market,...)
│  └─ market_overrides/*.json        # 케이스별 지표/Why Now 오버라이드
├─ outputs/                          # 케이스별 산출물 + Final_Report.docx
├─ artifacts/                        # (옵션) 디버그/근거 저장소
├─ tools/validate_report.py          # 리포트 검증 스크립트
├─ requirements.txt                  # 의존성
└─ .gitignore                        # 비공개/산출물 제외 규칙
```

케이스 폴더 산출물(예: `outputs/ShipBob_KR/`)
- 01_market_summary_*.png
- 02_customs_flow_*.png
- 03_competition_heatmap_*.png
- 04_partner_map_*.png
- strategy_card_{Company}_{ISO2}.md / .html
- summary.json / case_state.json

---

## 3) 실행

가상환경/의존성
```
python -m venv .venv
. .venv/Scripts/activate   # PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

환경 변수(선택)
```
# 지도 마커 크기 조정
set MARKER_SIZE_DEFAULT=28
set MARKER_SIZE_KR=40
```

파이프라인
```
# Phase1 (시장→규제→의사결정→카드/리포트)
python src/app.py --input data/companies.json --out outputs/ --phase phase1

# Full (경쟁/GTM/파트너/리스크 포함)
python src/app.py --input data/companies.json --out outputs/ --phase full
```

검증
```
python tools/validate_report.py
# PASS: report ok  (성공 기준)
```

---

## 4) 보안/운영 가이드

- 절대 커밋 금지: `.env`, `.env.example`, 기타 `*.env` (이미 `.gitignore` 반영)
- 산출물(outputs/), artifacts/는 대용량/민감 가능성 → 기본 제외
- Final_Report.docx가 열려 있으면 저장 충돌 발생 → 열려 있으면 타임스탬프 파일로 자동 저장

---

## 5) 기여 가이드

- 시장 지표 보강: `data/market_overrides/{Company}_{Country}.json`
- 경쟁사 보강: `data/rag_corpus/competition/*.csv`에 competitor/category/homepage 추가
- 시각화 튜닝: env 또는 `src/viz` 파라미터 조정
- 리포트 서식: `src/agents/final_reporter.py` 내 표/색상/섹션 부분 개선

