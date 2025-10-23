# RAG Corpus 데이터 가이드

이 폴더는 시장 진출 전략 분석을 위한 RAG(Retrieval-Augmented Generation) 데이터를 저장합니다.

## 폴더 구조

```
data/rag_corpus/
├── competition/       # 경쟁사 분석 데이터
├── market/           # 시장 리서치 데이터
└── regulation/       # 규제/법규 데이터
```

---

## 1. competition/ (경쟁사 분석)

### 필요한 파일 형식

#### A) CSV 파일 (권장)
각 회사×국가별 경쟁사 정보를 CSV로 저장합니다.

**파일명 예시**: `logistics_competitors.csv`, `kr_market_competitors.csv`

**필수 컬럼 (헤더)**:
```csv
company,target_market,competitor,category,homepage
```

**예시 데이터**:
```csv
company,target_market,competitor,category,homepage
ShipBob,KR,CJ Logistics,3PL,https://www.cjlogistics.com
ShipBob,KR,Lotte Global Logistics,3PL,https://www.lotteglogis.com
ShipBob,KR,Qxpress,Last Mile,https://www.qxpress.co
ShipBob,JP,Yamato Transport,3PL,https://www.kuronekoyamato.co.jp
Locus.sh,US,FedEx Fulfillment,3PL,https://www.fedex.com
Locus.sh,US,Amazon Logistics,Fulfillment,https://logistics.amazon.com
```

**컬럼 설명**:
- `company`: 분석 대상 회사명 (예: ShipBob, Locus.sh)
- `target_market`: 진출 목표 국가 ISO2 코드 (예: KR, JP, US)
- `competitor`: 경쟁사명
- `category`: 경쟁사 분류 (예: 3PL, Last Mile, Fulfillment, Freight Forwarder)
- `homepage`: 경쟁사 웹사이트 URL

**카테고리 예시**:
- `3PL`: Third-Party Logistics (종합 물류)
- `Last Mile`: 라스트마일 배송 업체
- `Fulfillment`: 풀필먼트 센터 운영사
- `Freight Forwarder`: 화물운송 중개업
- `Customs Broker`: 관세사/통관 대행

#### B) TXT 파일 (간단 버전)
국가별 경쟁사 이름 목록만 저장 (지도 마커용)

**파일명**: `{COUNTRY}_entities.txt`

**예시** (`KR_entities.txt`):
```
CJ Logistics
Lotte Global Logistics
Hanjin
Kurly
Qxpress
```

### 사용 위치
- `src/utils/competitor_data.py`: CSV 파싱
- `src/agents/competitor_mapping.py`: 경쟁사 분석 에이전트
- `src/viz/maps.py`: 경쟁사 지도 마커 생성

---

## 2. market/ (시장 리서치)

### 필요한 파일 형식

#### A) PDF 리포트 (권장)
시장 조사 리포트, 산업 분석 자료

**파일명 예시**:
- `KR_ecommerce_market_2024.pdf`: 한국 이커머스 시장 보고서
- `JP_logistics_industry_report.pdf`: 일본 물류 산업 리포트
- `US_fulfillment_trends_2024.pdf`: 미국 풀필먼트 트렌드

**내용 예시**:
- 시장 규모 (TAM, SAM, SOM)
- 성장률 (CAGR)
- 이커머스 침투율
- 물류 인프라 점수
- 배송 비용 평균
- 주요 트렌드 및 동향

#### B) JSON 데이터 (구조화)
국가별 시장 지표 데이터

**파일명**: `{COUNTRY}_market_data.json`

**예시** (`KR_market_data.json`):
```json
{
  "country": "KR",
  "year": 2024,
  "ecommerce": {
    "market_size_usd": "156B",
    "cagr_2024_2028": "8.5%",
    "penetration_rate": "28%"
  },
  "logistics": {
    "infrastructure_score": 82,
    "avg_delivery_days": 1.2,
    "last_mile_cost_usd": 3.5
  },
  "sources": [
    {"url": "https://example.com/kr-ecom-report", "date": "2024-01-15"},
    {"url": "https://statista.com/kr-logistics", "date": "2024-03-20"}
  ]
}
```

#### C) 텍스트/마크다운
시장 인사이트, Why Now 분석

**파일명**: `{COUNTRY}_insights.md`

**예시**:
```markdown
# 한국(KR) 시장 진출 분석

## Why Now
- 크로스보더 수요 급증 (YoY +35%)
- 당일배송 인프라 확대 (서울/경기 95% 커버리지)
- 정부 규제 완화 (FTA 확대, 통관 간소화)

## Key Metrics
- TAM: $156B (2024)
- CAGR: 8.5%
- Fulfillment Center 증가율: +25% YoY
```

### 사용 위치
- `src/agents/market_research.py`: 시장 데이터 분석 (현재는 해시 기반 자동 생성)
- 향후 RAG 연동 시 PDF/JSON에서 실제 데이터 추출

---

## 3. regulation/ (규제/법규)

### 필요한 파일 형식

#### A) PDF 문서 (공식 자료)
정부 규제, 법령, 가이드라인

**파일명 예시**:
- `KR_customs_law_2024.pdf`: 관세법
- `KR_ecommerce_consumer_protection.pdf`: 전자상거래 소비자보호법
- `JP_data_protection_act.pdf`: 개인정보보호법
- `US_import_regulations.pdf`: 수입 규정

**주제별 분류**:
- **Customs (통관)**: 관세법, 수입 절차, FTA 규정
- **License (허가)**: 사업자 등록, 물류업 면허, 택배업 신고
- **Data (데이터)**: 개인정보 보호, 국외 이전 규정
- **Ecom (전자상거래)**: 환불/반품 규정, 표시광고법, 약관 규제
- **Tax (세금)**: 부가가치세, 관세, 원천징수

#### B) JSON 규제 체크리스트
국가별 규제 요구사항 구조화

**파일명**: `{COUNTRY}_regulations.json`

**예시** (`KR_regulations.json`):
```json
{
  "country": "KR",
  "last_updated": "2024-10-01",
  "items": [
    {
      "id": "LICENSE_DELIVERY",
      "category": "License",
      "title": "택배업 신고 (우정법)",
      "criticality": "MUST",
      "description": "택배 사업 영위 시 과학기술정보통신부 신고 필요",
      "status": "PASS",
      "requirements": [
        "사업자 등록증",
        "물류 창고 확보 증명",
        "배상책임보험 가입"
      ],
      "timeline_days": 30,
      "sources": [
        {"url": "https://law.go.kr/postal-act", "date": "2024-01-01"}
      ]
    },
    {
      "id": "DATA_XFER",
      "category": "Data",
      "title": "개인정보 국외 이전",
      "criticality": "MUST",
      "description": "고객 데이터를 해외 서버에 저장 시 동의 및 고지 필요",
      "status": "TBD",
      "requirements": [
        "명시적 동의 획득",
        "국외 이전 고지",
        "PIPL 준수"
      ],
      "timeline_days": 60,
      "sources": [
        {"url": "https://pipc.go.kr", "date": "2024-03-15"}
      ]
    }
  ]
}
```

**status 값**:
- `PASS`: 요구사항 충족 확인
- `WARN`: 부분적 충족, 주의 필요
- `TBD`: 확인 필요 (법률 검토 중)
- `FAIL`: 미충족 (블로커 가능)

**criticality 값**:
- `MUST`: 필수 (미충족 시 사업 불가)
- `SHOULD`: 권장 (미충족 시 리스크)
- `NICE`: 선택 (부가 혜택)

#### C) 마크다운 요약
규제 가이드 문서

**파일명**: `{COUNTRY}_compliance_guide.md`

**예시**:
```markdown
# 한국(KR) 규제 컴플라이언스 가이드

## 필수 사항 (MUST)
1. **택배업 신고** - 과기부 신고 (30일 소요)
2. **개인정보 처리방침** - PIPC 가이드라인 준수
3. **통관 절차** - 관세청 전자통관 시스템 연동

## 권장 사항 (SHOULD)
1. **환불/반품 정책** - 전자상거래법 준수
2. **표시광고 가이드** - 공정거래위원회 규정

## 참고 자료
- [관세청](https://customs.go.kr)
- [개인정보보호위원회](https://pipc.go.kr)
```

### 사용 위치
- `src/agents/regulation_check.py`: 규제 컴플라이언스 분석 (현재는 하드코딩)
- 향후 RAG 연동 시 PDF/JSON에서 실제 규제 항목 추출

---

## 현재 구현 상태

### ✅ 구현됨 (Competition 데이터)

**파일 위치**: `src/utils/competitor_data.py`

**기능**:
- CSV 파싱: `load_competitor_entities()` 함수로 경쟁사 데이터 로드
- 컬럼: company, target_market, competitor, category, homepage
- 카테고리별 색상 매핑 (3PL, Last Mile, Fulfillment, Freight Forwarder 등)
- 지도 마커 생성: `src/viz/maps.py`에서 경쟁사 위치 표시
- 히트맵 생성: 경쟁 밀도 시각화

**현재 데이터**:
- `sample_competitors.csv`: 3개 회사 × 국가별 23개 경쟁사
- `KR_entities.txt`, `JP_entities.txt`: 국가별 엔티티 목록

**사용 에이전트**: `src/agents/competitor_mapping.py`

### ⚠️ 미구현 (향후 보완 예정)

**Market 데이터**:
- 현재: 해시 기반 더미 데이터 생성 (케이스별 차별화)
- 계획: PDF/JSON 파싱 → 실제 시장 리서치 데이터 로드
- 에이전트: `src/agents/market_research.py`

**Regulation 데이터**:
- 현재: 하드코딩된 5개 규제 항목 (템플릿 기반)
- 계획: PDF/JSON 파싱 → 국가별 규제 체크리스트 자동 로드
- 에이전트: `src/agents/regulation_check.py`

**RAG 파이프라인**:
- PDF → 임베딩 → 벡터 DB (ChromaDB, FAISS 등)
- LLM 기반 자동 추출 및 요약
- Evidence URL/발행일 자동 수집 및 Citation

**향후 로드맵**:
1. Phase 2: PDF 파서 추가 (PyPDF2, pdfplumber)
2. Phase 3: 벡터 DB 연동 (ChromaDB)
3. Phase 4: 웹 크롤러 (자동 데이터 업데이트)

---

## 데이터 수집 가이드

### 추천 데이터 소스

#### Market 데이터
- **Statista**: 국가별 이커머스/물류 통계
- **McKinsey/BCG**: 산업 리포트
- **정부 통계**: KOTRA, JETRO, US Census Bureau
- **업계 리포트**: Gartner, Forrester

#### Regulation 데이터
- **정부 사이트**:
  - 한국: law.go.kr, customs.go.kr
  - 일본: e-gov.go.jp
  - 미국: federalregister.gov
- **변호사 자문**: 현지 법률 사무소 리포트
- **KOTRA**: 국가별 진출 가이드

#### Competition 데이터
- **회사 웹사이트**: 경쟁사 공식 홈페이지
- **Crunchbase**: 스타트업 정보
- **LinkedIn**: 회사 규모/직원 수
- **SimilarWeb**: 웹 트래픽 분석

---

## 파일 추가 방법

### 1. Competition CSV 추가
```bash
# data/rag_corpus/competition/logistics_kr.csv
echo "company,target_market,competitor,category,homepage
ShipBob,KR,CJ Logistics,3PL,https://www.cjlogistics.com
ShipBob,KR,Lotte Global,3PL,https://www.lotteglogis.com" > data/rag_corpus/competition/logistics_kr.csv
```

### 2. Market PDF 추가
```bash
# PDF 파일을 다운로드하여 저장
cp ~/Downloads/korea_ecommerce_2024.pdf data/rag_corpus/market/KR_ecommerce_market_2024.pdf
```

### 3. Regulation JSON 추가
```bash
# JSON 파일 생성
cat > data/rag_corpus/regulation/KR_regulations.json << 'EOF'
{
  "country": "KR",
  "items": [...]
}
EOF
```

---

## 보안 주의사항

⚠️ **절대 커밋 금지**:
- 유료 리포트 PDF (저작권 위반)
- 내부 법률 자문 문서 (기밀)
- 고객사 계약 정보

✅ **커밋 가능**:
- 공개 정부 자료 (출처 명시)
- 자체 작성한 JSON/CSV
- 공개 통계 데이터

현재 `.gitignore`에 `*.pdf` 제외 규칙이 없으므로, 민감한 PDF는 수동으로 제외하거나 `.gitignore`에 추가하세요.

---

## 향후 로드맵

### Phase 1 (현재) ✅
- [x] Competition CSV 파싱 및 지도 생성
- [x] 해시 기반 Market 데이터 생성 (케이스별 차별화)
- [x] 템플릿 기반 Regulation 데이터 생성
- [x] 기본 Evidence 블록 (플레이스홀더)

### Phase 2 (계획) 🚧
- [ ] PDF 파서 추가 (PyPDF2, pdfplumber)
  - Market 리서치 리포트 자동 추출
  - Regulation 문서 파싱 및 체크리스트 생성
- [ ] JSON 기반 데이터 오버라이드
  - 케이스별 시장 지표 커스터마이징
  - 규제 항목 외부 파일로 관리
- [ ] LLM 기반 PDF → 구조화 데이터 변환

### Phase 3 (미래) 🔮
- [ ] RAG 벡터 DB 연동 (ChromaDB, FAISS)
  - PDF 임베딩 및 시맨틱 검색
  - 질의 기반 Evidence 자동 추출
- [ ] 웹 크롤러 (Selenium, Scrapy)
  - 경쟁사 웹사이트 자동 수집
  - 시장 통계 자동 업데이트
- [ ] Evidence Citation 자동화
  - URL 유효성 검증
  - 발행일 자동 추출
  - 출처 신뢰도 평가

---

## 참고사항

- 각 폴더의 `.gitkeep` 파일: 빈 폴더를 Git에 유지하기 위한 플레이스홀더
- 민감한 PDF 파일은 `.gitignore`에 수동 추가 권장
- 공개 데이터 소스 사용 시 출처 명시 필수

---

## 관련 파일

- **메인 README**: `../../README.md` - 프로젝트 전체 개요
- **Competition 로더**: `../../src/utils/competitor_data.py`
- **경쟁사 맵핑 에이전트**: `../../src/agents/competitor_mapping.py`
- **시장 조사 에이전트**: `../../src/agents/market_research.py`
- **규제 검토 에이전트**: `../../src/agents/regulation_check.py`
