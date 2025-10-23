from loguru import logger
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor
from ..state_schema import State

# 각 노드 import
from ..agents.input_validation import run as input_validation
from ..agents.market_research import run as market_research
from ..agents.regulation_check import run as regulation_check
from ..agents.competitor_mapping import run as competitor_mapping
from ..agents.gtm_high import run as gtm_high
from ..agents.gtm_mid import run as gtm_mid
from ..agents.gtm_low import run as gtm_low
from ..agents.gtm_merge import run as gtm_merge
from ..agents.partner_sourcing import run as partner_sourcing
from ..agents.risk_scenarios import run as risk_scenarios
from ..agents.decision_maker import run as decision_maker
from ..agents.report_writer import run as report_writer
from ..utils.output_index import build_outputs_index
from ..agents.final_reporter import run as final_reporter
from ..agents.html_reporter import run as html_reporter


def run_pipeline(state: State, meta: Dict[str, Any], out_dir: str, phase: str = "phase1"):
    # 입력검증
    input_validation(state, meta)

    # 회사 루프
    for company in meta.get("companies", []):
        for country in company.get("target_countries", []):
            logger.info("Processing {} -> {}", company.get("name"), country)
            context = {"company": company, "country": country, "out_dir": out_dir}
            # Phase selection
            if phase == "phase1":
                market_research(state, context)
                regulation_check(state, context)
                decision_maker(state, context)
                report_writer(state, context)
                html_reporter(state, context)
                continue

            # Full pipeline
            market_research(state, context)
            regulation_check(state, context)
            competitor_mapping(state, context)
            with ThreadPoolExecutor(max_workers=3) as ex:
                ex.submit(gtm_high, state, context)
                ex.submit(gtm_mid, state, context)
                ex.submit(gtm_low, state, context)
            gtm_merge(state, context)
            partner_sourcing(state, context)
            risk_scenarios(state, context)
            decision_maker(state, context)
            report_writer(state, context)
            html_reporter(state, context)
    # Update outputs index at the end
    build_outputs_index(out_dir)
    # Build final Word report
    final_reporter(state, meta, out_dir)
