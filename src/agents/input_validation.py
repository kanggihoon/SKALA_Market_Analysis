from ..state_schema import State, InputMeta, Company


def run(state: State, meta):
    # Validate required fields; allow variable company count
    errors = []
    companies = meta.get("companies", [])
    if not isinstance(companies, list) or len(companies) == 0:
        errors.append("companies must be a non-empty list")
    required = {"name", "size", "hq_country", "target_countries", "sector"}
    for idx, c in enumerate(companies):
        miss = required - set(c.keys())
        if miss:
            errors.append(f"company[{idx}] missing fields: {sorted(list(miss))}")
        # country code validation (ISO2-like)
        for cc in c.get("target_countries", []):
            if not isinstance(cc, str) or len(cc) != 2:
                errors.append(f"company[{c.get('name','?')}]: invalid country code '{cc}'")

    state.input_meta = InputMeta(
        companies=[Company(**c) for c in companies if set(required).issubset(c.keys())],
        validated=(len(errors) == 0),
        errors=errors,
    )

