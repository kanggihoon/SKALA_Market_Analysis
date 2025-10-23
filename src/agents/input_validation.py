from ..state_schema import State, InputMeta, Company


def run(state: State, meta):
    # 회사 수==3, 필드 유효성, 국가코드 2자리 등 검증
    errors = []
    companies = meta.get("companies", [])
    if len(companies) != 3:
        errors.append("companies must be exactly 3")
    # 간단 필수 필드 체크
    required = {"name", "size", "hq_country", "target_countries", "sector"}
    for idx, c in enumerate(companies):
        miss = required - set(c.keys())
        if miss:
            errors.append(f"company[{idx}] missing fields: {sorted(list(miss))}")
        # 국가코드 2자리 체크
        for cc in c.get("target_countries", []):
            if not isinstance(cc, str) or len(cc) != 2:
                errors.append(f"company[{c.get('name','?')}]: invalid country code '{cc}'")

    state.input_meta = InputMeta(
        companies=[Company(**c) for c in companies],
        validated=(len(errors) == 0),
        errors=errors,
    )

