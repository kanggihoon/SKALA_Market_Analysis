# 다국적 시장 진출 전략 에이전트 (SKALA Market Analysis)

회사×국가 단위의 시장 진출 전략을 자동으로 분석하고 리포트를 생성하는 AI 에이전트 파이프라인입니다.

**핵심 기능**:
- 시장/규제/경쟁/GTM/파트너/리스크 분석을 자동화
- 각 케이스별 상이한 수치, 문구, 지도, 표 생성
- Markdown, HTML, Word(DOCX) 형식의 전략 리포트 출력
- Phase별 실행 (빠른 Phase1 / 전체 Full 파이프라인)

---

## 📊 프로젝트 상태 요약 (기존 계획 대비)

### ✅ 구현 완료

**파이프라인 & 에이전트**
- ✅ 15개 에이전트 노드 구현 (Input Validation → Market Research → ... → Final Reporter)
- ✅ Phase1 / Full 모드 지원 (단계별 실행 가능)
- ✅ GTM 세그먼트 병렬 처리 (ThreadPool 기반)
- ✅ 케이스별 출력 폴더 자동 생성

**핵심 분석 기능**
- ✅ 시장 조사: Why Now + 5대 지표 (TAM, CAGR, 이커머스 침투율, 인프라 점수, 배송비)
- ✅ 규제 분석: MUST/SHOULD/NICE 등급, PASS/WARN/TBD/FAIL 상태, Coverage 점수 계산
- ✅ 경쟁사 분석: CSV 데이터 로드, 카테고리별 색상 마커, 히트맵/지도 생성, 화이트스페이스 발굴
- ✅ GTM 전략: 3개 세그먼트(high/mid/low) 카드 생성, 팬인(최적 세그먼트 선택)
- ✅ 파트너 발굴: 후보 3개 이상, 역할/우선순위, 지도 시각화
- ✅ 리스크 시나리오: 가능성×영향도, 완화책, 조기 경보 트리거
- ✅ 의사결정: 스코어카드(base → 각종 adjustment → final), RECOMMEND/HOLD 판정

**리포트 생성**
- ✅ Markdown 전략 카드 (케이스별)
- ✅ HTML 전략 카드 (Tailwind CSS 기반 인터랙티브)
- ✅ Word 통합 리포트 (전체 케이스 통합, 표/이미지/Evidence 포함)
- ✅ 자동 인덱스 테이블 (`outputs/README.md`)

**시각화**
- ✅ 한글 폰트 자동 설정 (Noto Sans KR / Malgun Gothic / NanumGothic)
- ✅ matplotlib 차트 (시장 지표, 통관 플로우)
- ✅ geopandas 지도 (경쟁사 마커, 파트너 위치, 히트맵)
- ✅ 환경변수 기반 마커 크기 조정

**검증 & 데이터**
- ✅ 리포트 검증 스크립트 (`tools/validate_report.py`)
- ✅ 경쟁사 CSV 로더 (`data/rag_corpus/competition/*.csv`)
- ✅ 케이스별 상이한 수치/문구 생성 (해시 기반)

### 🚧 부분 구현 (템플릿/더미 데이터 사용)

- 🚧 **시장 데이터**: 해시 기반 더미 데이터 생성 (실제 RAG 미연동)
  - 현재: 케이스별 차별화된 수치 자동 생성
  - 부족: 실제 PDF/JSON 시장 리서치 데이터 로드 미구현

- 🚧 **규제 데이터**: 템플릿 기반 5개 항목 하드코딩
  - 현재: MUST/SHOULD/NICE 등급 및 상태 추적 로직 완성
  - 부족: 국가별 규제 체크리스트 외부 파일 로드 미구현

- 🚧 **Evidence 블록**: 플레이스홀더 URL + 날짜
  - 현재: 각 섹션별 Evidence 블록 구조 생성
  - 부족: 실제 출처 URL 수집 및 검증 미구현

### 📋 향후 구현 예정

**Phase 2 (단기)**
- [ ] RAG 파이프라인 연동
  - PDF 파서 (PyPDF2, pdfplumber)
  - 시장 데이터 오버라이드 (JSON 파일 기반)
  - 규제 체크리스트 외부 파일 관리
- [ ] Evidence 자동 수집
  - 실제 출처 URL 크롤링/검색
  - 발행일 자동 추출
  - URL 유효성 검증
- [ ] 시각화 고도화
  - 지도 확대/색상 팔레트 커스터마이징
  - 인터랙티브 차트 (Plotly, D3.js)
- [ ] Word 리포트 고급 서식
  - 브랜드 테마 적용
  - 고급 표 스타일
  - 자동 목차 생성

**Phase 3 (중장기)**
- [ ] 벡터 DB 연동 (ChromaDB, FAISS)
  - PDF 임베딩 및 시맨틱 검색
  - 질의 기반 Evidence 자동 추출
- [ ] 웹 크롤러 통합
  - 경쟁사 웹사이트 자동 수집
  - 시장 통계 자동 업데이트
- [ ] 다국어 지원 (영어, 중국어)
- [ ] API 서버 구축 (FastAPI)
- [ ] 대시보드 UI (Streamlit / React)

---

## 목차

- [1) 구현 현황 (상세)](#1-구현-현황)
- [2) 폴더 구조](#2-폴더-구조)
- [3) 실행](#3-실행)
- [4) 보안/운영 가이드](#4-보안운영-가이드)
- [5) 데이터 확장 가이드](#5-데이터-확장-가이드)
- [6) 기여 가이드](#6-기여-가이드)

---

## 1) 구현 현황

### ✅ 구현 완료

**파이프라인 구조**
- Phase1 모드: 시장 조사 → 규제 검토 → 의사결정 → 리포트 생성 (빠른 분석)
- Full 모드: 경쟁사 분석, GTM 전략, 파트너 발굴, 리스크 시나리오 포함 (전체 분석)
- 병렬 처리: GTM high/mid/low 세그먼트 분석을 ThreadPool로 동시 실행

**노드별 기능**
- **Market Research**: Why Now 분석 + 핵심 지표 5개 (TAM, CAGR, 이커머스 침투율, 인프라 점수, 평균 배송비)
  - 차트 이미지 생성: `01_market_summary_*.png`
  - 케이스별 해시 기반 차별화된 데이터 생성

- **Regulation Check**: 규제 컴플라이언스 분석
  - MUST/SHOULD/NICE 등급별 체크리스트
  - PASS/WARN/TBD/FAIL 상태 추적
  - Coverage 점수 계산 (가중평균)
  - 통관 프로세스 플로우차트: `02_customs_flow_*.png`

- **Competitor Mapping**: 경쟁사 지도 및 히트맵
  - CSV 데이터 로드: `data/rag_corpus/competition/*.csv`
  - 카테고리별 색상 마커 (3PL, Last Mile, Fulfillment 등)
  - 히트맵 이미지: `03_competition_heatmap_*.png`
  - 화이트스페이스 3개 발굴 (케이스별 상이)

- **GTM Strategy (Fan-out/Fan-in)**:
  - 3개 세그먼트 카드 (high/mid/low) 병렬 생성
  - 각 카드: ICP, Offer, Price, Channel, KPI 포함
  - 세그먼트 스코어 3개 모두 상이하게 보장
  - 팬인: 최적 세그먼트 선택 + 사유 1문장

- **Partner Sourcing**: 파트너 후보 발굴
  - 3개 이상 후보 + 역할/우선순위
  - 파트너 지도: `04_partner_map_*.png`

- **Risk Scenarios**: 리스크 레지스터
  - 케이스별 2개 이상 리스크
  - 가능성×영향도 평가
  - 완화책 및 조기 경보 트리거

- **Decision Maker**: 의사결정 스코어카드
  - base → coverage_adj → tbd_adj → blocker_flag → competition_adj → partner_adj → gtm_adj → final
  - 규제 커버리지 기반 가감점 (+10/0/−20)
  - MUST 규제 FAIL 시 자동 HOLD

**리포트 생성**
- Markdown 전략 카드: `strategy_card_{Company}_{Country}.md`
- HTML 전략 카드: `strategy_card_{Company}_{Country}.html`
- 통합 Word 리포트: `Final_Report.docx` (전체 케이스 통합)
- 각 섹션별 Evidence 블록 (URL + date)
- 케이스별 출력 폴더 구조화

**시각화**
- 한글 폰트 자동 설정 (Noto Sans KR / Malgun Gothic / NanumGothic)
- matplotlib 차트 생성 (시장 지표, 통관 플로우)
- geopandas 지도 생성 (경쟁사 마커, 파트너 위치)
- 환경변수 기반 마커 크기 조정 (MARKER_SIZE_DEFAULT, MARKER_SIZE_KR)

**검증**
- `tools/validate_report.py`: 리포트 규격 검증
  - 반복 coverage 체크
  - 맵/차트 경로 누락 검출
  - 동일 점수 3개 검출
  - MUST FAIL vs Decision 불일치 검출

**데이터 관리**
- `data/companies.json`: 3개 회사 (ShipBob, Locus.sh, Ninja Van) × 국가별 메타데이터
- `data/rag_corpus/competition/`: 경쟁사 CSV 및 엔티티 목록
- `outputs/{Company}_{Country}/`: 케이스별 산출물 폴더
- `outputs/README.md`: 자동 생성되는 케이스 인덱스 테이블

### 🚧 보완 예정

- Evidence URL의 실제 RAG/크롤러 연동 (현재는 플레이스홀더)
- 시장 데이터 오버라이드 기능 (JSON 기반 케이스별 커스터마이징)
- 지도 확대/색상 팔레트 고급 커스터마이징
- Word 리포트 브랜드 테마 및 고급 서식
- GTM 스코어링 가중치 외부 설정 파일

---

## 2) 폴더 구조

```
SKALA_Market_Analysis/
├─ src/                              # 소스 코드
│  ├─ app.py                         # CLI 엔트리 (phase1/full)
│  ├─ state_schema.py                # Pydantic State 스키마
│  ├─ agents/                        # 15개 에이전트 노드
│  │  ├─ input_validation.py        # 입력 검증
│  │  ├─ market_research.py         # 시장 조사
│  │  ├─ regulation_check.py        # 규제 분석
│  │  ├─ competitor_mapping.py      # 경쟁사 맵핑
│  │  ├─ gtm_high.py / gtm_mid.py / gtm_low.py  # GTM 세그먼트 (병렬)
│  │  ├─ gtm_merge.py               # GTM 팬인
│  │  ├─ partner_sourcing.py        # 파트너 발굴
│  │  ├─ risk_scenarios.py          # 리스크 시나리오
│  │  ├─ decision_maker.py          # 의사결정 스코어링
│  │  ├─ report_writer.py           # Markdown 리포트
│  │  ├─ html_reporter.py           # HTML 리포트
│  │  └─ final_reporter.py          # Word 통합 리포트
│  ├─ graph/
│  │  └─ build_graph.py             # 파이프라인 오케스트레이션
│  ├─ viz/                           # 시각화 유틸리티
│  │  ├─ charts.py                  # matplotlib 차트
│  │  ├─ maps.py                    # geopandas 지도
│  │  ├─ fonts.py                   # 한글 폰트 설정
│  │  └─ tables.py                  # 표 포맷팅
│  ├─ utils/                         # 유틸리티
│  │  ├─ competitor_data.py         # 경쟁사 CSV 로더
│  │  ├─ geocode.py                 # 지오코딩
│  │  └─ output_index.py            # 출력 인덱스 생성
│  └─ prompts/                       # (옵션) 프롬프트 템플릿
├─ data/
│  ├─ companies.json                 # 입력: 3개 회사 × 국가별 메타데이터
│  ├─ seeds/
│  │  └─ companies.demo.json        # 데모 샘플 데이터
│  └─ rag_corpus/                    # RAG 데이터 저장소
│     ├─ competition/
│     │  ├─ sample_competitors.csv  # 경쟁사 CSV (company, target_market, competitor, category, homepage)
│     │  ├─ KR_entities.txt         # 한국 경쟁사 목록
│     │  └─ JP_entities.txt         # 일본 경쟁사 목록
│     ├─ market/                     # (향후) 시장 데이터 PDF/JSON
│     └─ regulation/                 # (향후) 규제 데이터 PDF/JSON
├─ outputs/                          # 생성된 산출물
│  ├─ ShipBob_KR/                    # 케이스별 폴더
│  ├─ ShipBob_JP/
│  ├─ Locus.sh_US/
│  ├─ Locus.sh_KR/
│  ├─ Ninja Van_JP/
│  ├─ Final_Report.docx              # 통합 Word 리포트
│  └─ README.md                      # 자동 생성 인덱스 테이블
├─ logs/                             # 실행 로그
│  └─ node_dumps/                    # 노드별 디버그 덤프
├─ demo file/                        # 독립 실행 가능한 데모 리포트 생성기
│  ├─ report_templates.py           # HTML 템플릿
│  ├─ docx_report_generator.py      # DOCX 생성기
│  ├─ report_agent.py               # LangGraph 통합 에이전트
│  ├─ report_guide.py               # 프롬프트 가이드
│  └─ test_report_generation.py     # 독립 테스트 스크립트
├─ tools/
│  └─ validate_report.py            # 리포트 검증 스크립트
├─ requirements.txt                  # Python 의존성
├─ .gitignore                        # Git 제외 규칙
└─ README.md                         # 이 문서
```

### 케이스 폴더 산출물 예시 (`outputs/ShipBob_KR/`)

```
ShipBob_KR/
├─ 01_market_summary_ShipBob_KR.png       # 시장 지표 차트
├─ 02_customs_flow_ShipBob_KR.png         # 통관 프로세스 플로우
├─ 03_competition_heatmap_ShipBob_KR.png  # 경쟁 히트맵
├─ 04_partner_map_ShipBob_KR.png          # 파트너 위치 지도
├─ strategy_card_ShipBob_KR.md            # Markdown 전략 카드
├─ strategy_card_ShipBob_KR.html          # HTML 전략 카드
├─ summary.json                           # 요약 데이터
└─ case_state.json                        # 전체 State 스냅샷
```

---

## 3) 실행

### 사전 준비

**1. 가상환경 생성 및 활성화**
```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows CMD
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

**2. 의존성 설치**
```bash
pip install -r requirements.txt
```

**주요 의존성**:
- `pydantic>=2.7`: 데이터 스키마 검증
- `python-dotenv>=1.0`: 환경변수 관리
- `pandas>=2.2`: 데이터 처리
- `matplotlib>=3.8`: 차트 생성
- `geopandas>=0.14`: 지도 생성
- `python-docx>=1.1.0`: Word 리포트
- `loguru>=0.7`: 로깅
- `rich>=13.7`: CLI 출력

**3. 환경 변수 (선택)**

`.env` 파일 생성 (프로젝트 루트):
```bash
# Google Maps API (지도 생성 시 선택적으로 사용)
GOOGLE_MAPS_API_KEY=your_api_key_here

# 지도 마커 크기 조정
MARKER_SIZE_DEFAULT=28
MARKER_SIZE_KR=40
```

### 파이프라인 실행

**Phase1 모드 (빠른 분석)**
```bash
python src/app.py --input data/companies.json --out outputs/ --phase phase1
```
- 실행 노드: Market Research → Regulation Check → Decision Maker → Report Writer → HTML Reporter
- 소요 시간: ~2-5분 (3개 회사 × 국가)
- 적합: 빠른 프로토타이핑, 초기 의사결정

**Full 모드 (전체 분석)**
```bash
python src/app.py --input data/companies.json --out outputs/ --phase full
```
- 실행 노드: 위 + Competitor Mapping + GTM(high/mid/low 병렬) + GTM Merge + Partner Sourcing + Risk Scenarios
- 소요 시간: ~5-10분
- 적합: 최종 리포트, 상세 전략 수립

### 출력 확인

**케이스별 산출물**
```bash
# Markdown 리포트
cat outputs/ShipBob_KR/strategy_card_ShipBob_KR.md

# HTML 리포트 (브라우저에서 열기)
open outputs/ShipBob_KR/strategy_card_ShipBob_KR.html

# 이미지 파일
ls outputs/ShipBob_KR/*.png
```

**통합 Word 리포트**
```bash
# 전체 케이스 통합 리포트
open outputs/Final_Report.docx
```

**출력 인덱스 테이블**
```bash
cat outputs/README.md
```

### 검증

**리포트 규격 검증**
```bash
python tools/validate_report.py

# 출력 예시 (성공):
# ✅ PASS: Report validation passed

# 출력 예시 (실패):
# ❌ FAIL: Found 3 issues:
#   - Missing map image: ShipBob_KR/map_*.png
#   - Duplicate coverage scores detected
#   - MUST FAIL but Decision is RECOMMEND
```

### 데모 리포트 생성 (독립 실행)

```bash
cd "demo file"
python test_report_generation.py
```
- 샘플 데이터로 HTML + DOCX 리포트 즉시 생성
- 메인 파이프라인과 독립적으로 실행 가능

---

## 4) 보안/운영 가이드

### 보안 주의사항

**절대 커밋 금지**
- `.env` 파일 (API 키, 인증 정보 포함)
- `*.env` 파일 (모든 환경변수 파일)
- 유료 리포트 PDF (저작권 위반)
- 내부 법률 자문 문서
- 고객사 계약 정보

**이미 .gitignore에 반영됨**
```
.env
.env.*
outputs/
logs/
*.pyc
__pycache__/
```

### 운영 가이드

**1. Word 리포트 충돌 방지**
- `Final_Report.docx`가 열려 있으면 저장 실패
- 자동으로 타임스탬프 파일로 저장 (예: `Final_Report_20241023_143000.docx`)
- 실행 전 Word 파일 닫기 권장

**2. 대용량 산출물 관리**
- `outputs/` 폴더는 자동으로 Git에서 제외
- 주기적으로 오래된 케이스 폴더 정리:
  ```bash
  # 30일 이상 된 케이스 폴더 삭제
  find outputs/ -type d -mtime +30 -exec rm -rf {} \;
  ```

**3. 로그 관리**
- `logs/` 폴더는 자동으로 Git에서 제외
- loguru 설정으로 자동 로테이션 (10MB 단위)
- 디버그 시 `logs/node_dumps/` 확인

**4. 폰트 문제 해결**
- 한글 폰트 자동 감지: Noto Sans KR → Malgun Gothic → NanumGothic
- 폰트 없을 시 경고 로그 출력 (한글 깨짐 가능)
- Linux: `apt-get install fonts-noto-cjk` 권장

---

## 5) 데이터 확장 가이드

### 회사 추가

`data/companies.json` 편집:
```json
{
  "companies": [
    {
      "name": "NewCompany",
      "size": "Mid",
      "hq_country": "SG",
      "target_countries": ["TH", "VN"],
      "sector": "Logistics Tech",
      "notes": {
        "hypothesis": "동남아 3PL 디지털화",
        "icp_hint": "중소 3PL 업체",
        "pricing_hint": "$1k-$5k/월"
      }
    }
  ]
}
```

### 경쟁사 데이터 추가

`data/rag_corpus/competition/sample_competitors.csv` 편집:
```csv
company,target_market,competitor,category,homepage
NewCompany,TH,Kerry Express,Last Mile,https://kerryexpress.com
NewCompany,VN,Giao Hang Nhanh,3PL,https://ghn.vn
```

### 시장 데이터 커스터마이징 (향후)

케이스별 오버라이드 JSON 생성 (현재 미지원, 향후 추가 예정):
```bash
# data/market_overrides/NewCompany_TH.json
{
  "TAM": "$5.2B",
  "CAGR": "18.5%",
  "why_now": "정부 디지털화 정책 + 이커머스 급성장"
}
```

### 시각화 커스터마이징

**지도 마커 크기 조정** (`.env`):
```bash
MARKER_SIZE_DEFAULT=28
MARKER_SIZE_KR=40
MARKER_SIZE_JP=35
```

**차트 스타일 변경** (`src/viz/charts.py`):
```python
# 색상 팔레트
COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe']

# DPI 설정
plt.savefig(path, dpi=150, bbox_inches='tight')
```

**지도 배경 변경** (`src/viz/maps.py`):
```python
# 기본 지도 스타일
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
ax = world.plot(color='lightgray', edgecolor='white')
```

### 리포트 서식 커스터마이징

**Word 리포트 스타일** (`src/agents/final_reporter.py`):
```python
# 제목 폰트
heading.font.name = 'Noto Sans KR'
heading.font.size = Pt(18)
heading.font.bold = True

# 표 스타일
table.style = 'Light Grid Accent 1'
```

**HTML 리포트 테마** (`demo file/report_templates.py`):
```css
/* 그라데이션 변경 */
.gradient-bg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

---

## 6) 기여 가이드

프로젝트 개선에 기여하고 싶으시다면:

1. **이슈 생성**: 버그 리포트 또는 기능 제안
2. **브랜치 생성**: `feature/your-feature-name`
3. **코드 작성**: PEP 8 스타일 가이드 준수
4. **테스트 실행**: `python tools/validate_report.py`
5. **Pull Request**: 상세한 설명과 함께 제출

**주요 개선 영역**:
- RAG 파이프라인 연동 (PDF → 벡터 DB → 검색)
- 실제 Evidence URL 수집 자동화
- 추가 국가 지원 (동남아, 유럽 등)
- 다국어 리포트 생성 (영어, 중국어)
- 시각화 고도화 (인터랙티브 차트, 대시보드)

