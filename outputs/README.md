# 전략 카드 산출물 인덱스

> 이 파일은 `src/utils/output_index.py`에 의해 자동 생성됩니다.
>
> 파이프라인 실행 후 모든 케이스의 요약 정보를 테이블 형태로 제공합니다.

---

## 개요

이 폴더는 `src/app.py` 실행 결과로 생성된 전략 분석 산출물을 저장합니다.

**폴더 구조**:
```
outputs/
├── {Company}_{Country}/          # 케이스별 폴더 (예: ShipBob_KR)
│   ├── 01_market_summary_*.png
│   ├── 02_customs_flow_*.png
│   ├── 03_competition_heatmap_*.png
│   ├── 04_partner_map_*.png
│   ├── strategy_card_*.md        # Markdown 전략 카드
│   ├── strategy_card_*.html      # HTML 전략 카드
│   ├── summary.json              # 요약 데이터
│   └── case_state.json           # 전체 State 스냅샷
├── Final_Report.docx             # 통합 Word 리포트 (모든 케이스)
└── README.md                     # 이 문서 (자동 생성)
```

---

## 자동 생성된 전략 카드 요약

| Case | Decision | Final | Coverage | TBD | Risk | GTM | Card | HTML |
|---|---|---:|---:|---:|---|---|---|---|
| Locus.sh_KR | HOLD | 25 | 60% | 30% | None | high | [Locus.sh_KR\strategy_card_Locus.sh_KR.md](Locus.sh_KR\strategy_card_Locus.sh_KR.md) |  |
| Locus.sh_US | RECOMMEND | 65 | 60% | 30% | High | high | [Locus.sh_US\strategy_card_Locus.sh_US.md](Locus.sh_US\strategy_card_Locus.sh_US.md) | [Locus.sh_US\strategy_card_Locus.sh_US.html](Locus.sh_US\strategy_card_Locus.sh_US.html) |
| Ninja Van_JP | RECOMMEND | 65 | 60% | 30% | High | mid | [Ninja Van_JP\strategy_card_Ninja Van_JP.md](Ninja Van_JP\strategy_card_Ninja Van_JP.md) | [Ninja Van_JP\strategy_card_Ninja Van_JP.html](Ninja Van_JP\strategy_card_Ninja Van_JP.html) |
| ShipBob_JP | RECOMMEND | 65 | 60% | 30% | High | high | [ShipBob_JP\strategy_card_ShipBob_JP.md](ShipBob_JP\strategy_card_ShipBob_JP.md) | [ShipBob_JP\strategy_card_ShipBob_JP.html](ShipBob_JP\strategy_card_ShipBob_JP.html) |
| ShipBob_KR | RECOMMEND | 65 | 60% | 30% | High | mid | [ShipBob_KR\strategy_card_ShipBob_KR.md](ShipBob_KR\strategy_card_ShipBob_KR.md) | [ShipBob_KR\strategy_card_ShipBob_KR.html](ShipBob_KR\strategy_card_ShipBob_KR.html) |

---

## 컬럼 설명

- **Case**: 회사명_국가코드 (예: ShipBob_KR)
- **Decision**: 의사결정 결과 (RECOMMEND / HOLD)
- **Final**: 최종 스코어 (0~100)
- **Coverage**: 규제 커버리지 비율 (%)
- **TBD**: 미결정 규제 항목 비율 (%)
- **Risk**: 리스크 레벨 (낮음/보통/높음/None)
- **GTM**: 선택된 GTM 세그먼트 (high/mid/low)
- **Card**: Markdown 전략 카드 링크
- **HTML**: HTML 전략 카드 링크 (생성된 경우)

---

## 통합 리포트

**Final_Report.docx**: 모든 케이스를 하나의 Word 문서로 통합한 최종 리포트

- 각 케이스별로 섹션 구분
- 표, 이미지, Evidence 블록 포함
- 인쇄 및 공유 최적화

---

## 재생성 방법

```bash
# 전체 파이프라인 재실행
python src/app.py --input data/companies.json --out outputs/ --phase full

# 이 인덱스 파일만 재생성
python -c "from src.utils.output_index import build_outputs_index; build_outputs_index('outputs/')"
```

---

**주의**: 이 폴더는 `.gitignore`에 포함되어 Git에 커밋되지 않습니다.

