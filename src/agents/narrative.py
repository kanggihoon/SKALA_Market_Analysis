import os
from typing import Dict, Any, Tuple
from datetime import datetime

try:
    from jinja2 import Template
except Exception:  # pragma: no cover
    Template = None  # type: ignore


def clamp_chars(s: str, max_chars: int) -> str:
    s = (s or "").strip()
    if max_chars and len(s) > max_chars:
        cut = s[: max_chars].rstrip()
        # try to end on a sentence terminator
        for tok in (".", "!", "?", "다", "요"):
            idx = cut.rfind(tok)
            if idx >= 0 and (max_chars - idx) < 40:  # within tail
                return cut[: idx + len(tok)]
        return cut + "…"
    return s


def _render(tmpl: str, ctx: Dict[str, Any]) -> str:
    if Template is None:
        # naive fallback
        return tmpl
    return Template(tmpl).render(**ctx)


def _compact_table(gtm_table) -> str:
    try:
        rows = [f"{r.get('segment')} {r.get('score')}" for r in (gtm_table or [])]
        return "; ".join(rows)
    except Exception:
        return ""


def build_prompts(case: Dict[str, Any], limits: Dict[str, int]) -> Dict[str, str]:
    company = case.get("company", "")
    country = case.get("country", "")
    decision = case.get("decision", {}) or {}
    cov = float(case.get("coverage") or 0)
    tbd_ratio = float(case.get("tbd_ratio") or 0)
    risk_badge = case.get("risk_badge") or ""
    market = case.get("market", {}) or {}
    metrics = market.get("metrics", {}) or {}
    why_now = market.get("why_now", "")
    comp = case.get("competition", {}) or {}
    whitespaces = comp.get("whitespaces", []) or []
    partners = case.get("partners", []) or []
    gtm = case.get("gtm", {}) or {}
    gtm_table = gtm.get("table", []) or []
    gtm_selected = gtm.get("selected", "")

    ctx = {
        "company": company,
        "country": country,
        "decision": decision,
        "cov": cov,
        "cov_pct": round(cov * 100),
        "tbd_ratio": tbd_ratio,
        "tbd_pct": round(tbd_ratio * 100),
        "risk_badge": risk_badge,
        "TAM": metrics.get("TAM"),
        "CAGR": metrics.get("CAGR"),
        "Pen": metrics.get("Ecom Penetration"),
        "Infra": metrics.get("Infra Score"),
        "Ship": metrics.get("Avg Ship Cost"),
        "why_now": why_now,
        "whitespaces": whitespaces,
        "ws_count": len(whitespaces),
        "partners": partners,
        "table_compact": _compact_table(gtm_table),
        "selected": gtm_selected,
        "today": datetime.now().strftime("%Y-%m-%d"),
    }

    prompts = {}
    prompts["exec"] = _render(
        (
            "[역할] 당신은 전략 컨설턴트다. 아래 데이터를 바탕으로 Executive 요약을 {{limit}}자 이내로 작성하라.\n"
            "- 권고(status): {{decision.status}}, 최종점수: {{decision.scorecard.final}}\n"
            "- 커버리지: {{cov_pct}}%, TBD: {{tbd_pct}}%, 리스크: {{risk_badge}}\n"
            "- 화이트스페이스 수: {{whitespaces|length}}, 파트너 후보 수: {{partners|length}}\n"
            "[요구] 1문단으로 판단 근거와 핵심 수치(커버리지/TBD/화이트스페이스/파트너)를 포함하고, 보수적 리스크를 한 줄로 명시하라.\n"
            "[금지] 추상적 미사여구, 중복 문장"
        ),
        {**ctx, "limit": limits.get("exec", 500)},
    )

    prompts["market"] = _render(
        (
            "TAM={{TAM}}, CAGR={{CAGR}}, 침투율={{Pen}}, 인프라={{Infra}}, 평균배송비={{Ship}}를 해석해 "
            "초기 진입 난이도/수익성 관점의 함의를 {{limit}}자 이내 1문단으로 정리하라. 끝에 ‘Why Now: {{why_now}}’를 붙여라."
        ),
        {**ctx, "limit": limits.get("market", 500)},
    )

    prompts["regulation"] = _render(
        (
            "커버리지={{cov_pct}}%, TBD={{tbd_pct}}%, MUST 위반={{ '있음' if decision.get('scorecard',{}).get('blocker') else '없음' }}. "
            "규제 리스크 수준과 단기 조치(증빙/정책/계약)를 {{limit}}자 이내로 정리하라. HOLD면 보류 사유와 해소 조건, RECOMMEND면 잔여 리스크와 추적 포인트를 명시하라."
        ),
        {**ctx, "limit": limits.get("regulation", 500)},
    )

    prompts["competition"] = _render(
        (
            "화이트스페이스 {{ws_count}}개: {{whitespaces|join(', ')}}. "
            "경쟁 차별화 포인트(리드타임/신뢰성/연동 등)를 {{limit}}자 이내 1문단으로 작성하라. 데이터가 부족하면 보강 계획(비교표/PoC)을 간단히 포함하라."
        ),
        {**ctx, "limit": limits.get("competition", 500)},
    )

    prompts["gtm"] = _render(
        (
            "세그먼트별 점수: {{table_compact}}. 선택='{{selected}}'. 선택 사유(실행/수익성)와 초기 90일 우선순위 2가지(퍼널·파트너)를 {{limit}}자 이내 1문단으로 작성하라."
        ),
        {**ctx, "limit": limits.get("gtm", 500)},
    )

    prompts["partners"] = _render(
        (
            "파트너 후보 {{partners|length}}개. 역할/우선순위를 요약하라. 공백 영역(미확보 역할)이 있으면 보강 계획 1문장 포함. {{limit}}자 이내."
        ),
        {**ctx, "limit": limits.get("partners", 350)},
    )

    prompts["risks"] = _render(
        (
            "상위 리스크 2-3개를 확률/영향/완화책 중심으로 {{limit}}자 이내 1문단으로 요약하라."
        ),
        {**ctx, "limit": limits.get("risks", 400)},
    )

    prompts["overall"] = _render(
        (
            "최종 권고='{{decision.status}}' 근거(규제/경쟁/GTM/파트너)와 전제 조건을 {{limit}}자 이내 결론 문장으로 작성하라."
        ),
        {**ctx, "limit": limits.get("overall", 300)},
    )

    prompts["plan_30"] = "30일: 규제 증빙·파트너 계약·PoC 후보 확정(숫자 포함). 120자 이내."
    prompts["plan_60"] = "60일: PoC 진행·메시징/채널 정교화·1차 전환. 120자 이내."
    prompts["plan_90"] = "90일: 퍼널/OTD 검증·단가 최적화·확장 여부 판정. 120자 이내."

    prompts["evidence"] = (
        "규제/경쟁 근거 링크 최대 3개를 ‘영역: 제목/URL(날짜)’ 형식으로 한 줄씩 나열하라."
    )

    return prompts


def _call_openai(prompt: str, model: str, api_key: str, timeout: int = 60) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "당신은 간결하고 정확한 한국어 전략 컨설턴트다. 보고서 문체로 작성하라."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            timeout=timeout,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        return ""


def generate_texts(case: Dict[str, Any], model: str = None, limits: Dict[str, int] = None) -> Dict[str, str]:
    model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
    limits = limits or {}
    prompts = build_prompts(case, limits)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {}
    out: Dict[str, str] = {}
    for k, p in prompts.items():
        txt = _call_openai(p, model=model, api_key=api_key)
        if not txt:
            continue
        max_chars = limits.get(k, 500 if k not in ("partners", "risks", "overall") else {"partners": 350, "risks": 400, "overall": 300}[k] if k in ("partners","risks","overall") else 500)
        out[k] = clamp_chars(txt, max_chars)
    return out

