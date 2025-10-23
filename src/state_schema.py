from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class Company(BaseModel):
    name: str
    size: str
    hq_country: str
    target_countries: List[str]
    sector: str
    # Accept free-text or structured metadata
    notes: Optional[Union[str, Dict[str, Any]]] = None


class InputMeta(BaseModel):
    companies: List[Company]
    validated: bool = False
    errors: List[str] = []


class MarketSummary(BaseModel):
    metrics: Dict[str, Any]      # {"TAM":..., "growth":..., "infra":...}
    why_now: str
    market_summary_png: Optional[str] = None


class SegmentCard(BaseModel):
    icp: str
    offer: str
    price_hint: str
    channel: str
    kpi: Dict[str, str]
    risks: List[str] = []
    evidence: List[str] = []


class RegulationItem(BaseModel):
    id: str
    category: str
    title: str
    criticality: str  # MUST/SHOULD/NICE
    applicability: str  # APPLIES/NA
    status: str  # PASS/WARN/TBD/FAIL
    evidence: List[Dict[str, str]] = []
    notes: str = ""


class RegulationCompliance(BaseModel):
    items: List[RegulationItem]
    coverage: float = 0.0
    blocker: bool = False
    customs_flow_png: Optional[str] = None
    tbd_ratio: float = 0.0
    risk_badge: Optional[str] = None  # 낮음/보통/높음


class Competition(BaseModel):
    heatmap_png: Optional[str]
    markers_map_png: Optional[str] = None
    positioning: Dict[str, Any]
    whitespaces: List[str]


class GTMMerged(BaseModel):
    table: List[Dict[str, Any]]
    selected: str
    reason: str


class Partners(BaseModel):
    candidates: List[Dict[str, Any]]
    partner_map_png: Optional[str] = None


class Risks(BaseModel):
    register_items: List[Dict[str, Any]]
    thresholds: Dict[str, Any]


class Decision(BaseModel):
    status: str  # RECOMMEND/HOLD
    scorecard: Dict[str, Any]
    reason: str


class State(BaseModel):
    input_meta: Optional[InputMeta] = None
    market_summary: Optional[MarketSummary] = None
    segments_initial: Optional[List[str]] = None
    reg_compliance: Optional[RegulationCompliance] = None
    competition: Optional[Competition] = None
    gtm_high: Optional[SegmentCard] = None
    gtm_mid: Optional[SegmentCard] = None
    gtm_low: Optional[SegmentCard] = None
    gtm_merged: Optional[GTMMerged] = None
    partners: Optional[Partners] = None
    risks: Optional[Risks] = None
    decision: Optional[Decision] = None
    artifacts: Dict[str, str] = {}
