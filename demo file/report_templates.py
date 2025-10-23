"""
다국적 시장 진출 전략 보고서 템플릿 생성기

HTML과 DOCX 형식으로 예쁜 보고서를 생성합니다.
"""

from typing import Dict, List, Optional
from datetime import datetime
import base64
from pathlib import Path


class StrategyReportTemplate:
    """전략 보고서 HTML 템플릿 생성기"""
    
    @staticmethod
    def encode_image(image_path: str) -> str:
        """이미지를 base64로 인코딩"""
        if not Path(image_path).exists():
            return ""
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    
    @staticmethod
    def get_risk_badge_color(risk_level: str) -> str:
        """리스크 레벨에 따른 색상 반환"""
        colors = {
            "낮음": "bg-green-100 text-green-800 border-green-300",
            "보통": "bg-yellow-100 text-yellow-800 border-yellow-300",
            "높음": "bg-red-100 text-red-800 border-red-300"
        }
        return colors.get(risk_level, "bg-gray-100 text-gray-800 border-gray-300")
    
    @staticmethod
    def get_decision_color(decision: str) -> str:
        """의사결정에 따른 색상 반환"""
        if "진행" in decision or "추천" in decision:
            return "bg-blue-600 text-white"
        elif "보류" in decision:
            return "bg-orange-600 text-white"
        else:
            return "bg-gray-600 text-white"
    
    @classmethod
    def generate_html_report(
        cls,
        company: str,
        country: str,
        market_summary: Dict,
        regulatory_data: Dict,
        competitor_data: Dict,
        partner_data: Dict,
        risk_data: Dict,
        decision_data: Dict,
        visualizations: Dict[str, str],  # {name: filepath}
    ) -> str:
        """완전한 HTML 보고서 생성"""
        
        # 이미지 인코딩
        encoded_images = {}
        for name, path in visualizations.items():
            if path and Path(path).exists():
                encoded_images[name] = cls.encode_image(path)
        
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company} × {country} 시장 진출 전략</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
        
        body {{
            font-family: 'Noto Sans KR', sans-serif;
        }}
        
        .gradient-bg {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        .card {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.15);
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.875rem;
            border: 2px solid;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #667eea;
        }}
        
        .score-circle {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            font-weight: bold;
            margin: 0 auto;
        }}
        
        .progress-bar {{
            height: 8px;
            background: #e2e8f0;
            border-radius: 9999px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s ease;
        }}
        
        @media print {{
            body {{
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }}
            .card {{
                break-inside: avoid;
            }}
        }}
    </style>
</head>
<body class="bg-gray-50 p-8">
    <!-- 헤더 -->
    <div class="gradient-bg text-white p-8 rounded-2xl mb-8">
        <div class="max-w-6xl mx-auto">
            <h1 class="text-4xl font-bold mb-2">{company} × {country}</h1>
            <p class="text-xl opacity-90">다국적 시장 진출 전략 보고서</p>
            <p class="text-sm opacity-75 mt-4">생성일: {datetime.now().strftime('%Y년 %m월 %d일')}</p>
        </div>
    </div>
    
    <div class="max-w-6xl mx-auto space-y-8">
        
        <!-- Executive Summary -->
        <div class="card p-8">
            <h2 class="section-title">📋 Executive Summary</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <h3 class="font-bold text-lg mb-3">최종 의사결정</h3>
                    <div class="flex items-center gap-4">
                        <span class="badge {cls.get_decision_color(decision_data.get('decision', '보류'))}">{decision_data.get('decision', '보류')}</span>
                        <div class="score-circle {cls._get_score_bg_color(decision_data.get('final_score', 0))}">
                            {decision_data.get('final_score', 0)}점
                        </div>
                    </div>
                    <p class="mt-4 text-gray-700">{decision_data.get('rationale', '분석 중...')}</p>
                </div>
                <div>
                    <h3 class="font-bold text-lg mb-3">주요 지표</h3>
                    <div class="space-y-3">
                        <div>
                            <div class="flex justify-between mb-1">
                                <span class="text-sm font-medium">규제 커버리지</span>
                                <span class="text-sm font-bold">{regulatory_data.get('coverage_score', 0):.0%}</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {regulatory_data.get('coverage_score', 0) * 100}%"></div>
                            </div>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium">규제 리스크</span>
                            <span class="badge {cls.get_risk_badge_color(regulatory_data.get('risk_badge', '보통'))}">{regulatory_data.get('risk_badge', '보통')}</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium">파트너 후보</span>
                            <span class="font-bold text-lg">{len(partner_data.get('candidates', []))}개사</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 시장 조사 -->
        <div class="card p-8">
            <h2 class="section-title">🌍 시장 조사</h2>
            <div class="mb-6">
                <h3 class="font-bold text-lg mb-3">핵심 지표</h3>
                <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
                    {cls._generate_metric_cards(market_summary.get('metrics', {}))}
                </div>
            </div>
            
            <div class="mb-6">
                <h3 class="font-bold text-lg mb-3">Why Now?</h3>
                <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                    <p class="text-gray-800">{market_summary.get('why_now', '시장 분석 중...')}</p>
                </div>
            </div>
            
            {cls._generate_image_section('수요 히트맵', encoded_images.get('demand_heatmap'))}
        </div>
        
        <!-- 규제 검토 -->
        <div class="card p-8">
            <h2 class="section-title">✅ 규제 검토</h2>
            <div class="mb-6">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-lg font-semibold">커버리지: {regulatory_data.get('coverage_score', 0):.0%}</span>
                    <span class="badge {cls.get_risk_badge_color(regulatory_data.get('risk_badge', '보통'))}">
                        리스크: {regulatory_data.get('risk_badge', '보통')}
                    </span>
                </div>
                {cls._generate_regulatory_table(regulatory_data.get('checklist', []))}
            </div>
            
            {cls._generate_image_section('통관·관세 플로우', encoded_images.get('customs_flow'))}
        </div>
        
        <!-- 경쟁사 지도 -->
        <div class="card p-8">
            <h2 class="section-title">🗺️ 경쟁사 분석</h2>
            
            <div class="mb-6">
                <h3 class="font-bold text-lg mb-3">화이트스페이스 (기회 영역)</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {cls._generate_whitespace_cards(competitor_data.get('whitespace_gaps', []))}
                </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {cls._generate_image_section('경쟁 밀집 지도', encoded_images.get('competition_density'))}
                {cls._generate_image_section('포지셔닝 매트릭스', encoded_images.get('positioning'))}
            </div>
        </div>
        
        <!-- 파트너 발굴 -->
        <div class="card p-8">
            <h2 class="section-title">🤝 파트너 발굴</h2>
            
            <div class="mb-6">
                <h3 class="font-bold text-lg mb-3">파트너 후보 ({len(partner_data.get('candidates', []))}개사)</h3>
                {cls._generate_partner_table(partner_data.get('candidates', []))}
            </div>
            
            {cls._generate_image_section('파트너 연결 맵', encoded_images.get('partner_map'))}
            
            <div class="mt-6">
                <h3 class="font-bold text-lg mb-3">PoC 제안서 초안</h3>
                <div class="bg-gray-50 p-6 rounded-lg border border-gray-200">
                    <pre class="whitespace-pre-wrap font-sans text-sm text-gray-700">{partner_data.get('poc_proposal', 'PoC 제안서 작성 중...')}</pre>
                </div>
            </div>
        </div>
        
        <!-- 리스크 시나리오 -->
        <div class="card p-8">
            <h2 class="section-title">⚠️ 리스크 시나리오</h2>
            
            <div class="mb-6">
                <h3 class="font-bold text-lg mb-3">리스크 레지스터</h3>
                {cls._generate_risk_table(risk_data.get('register', []))}
            </div>
            
            <div class="mt-6">
                <h3 class="font-bold text-lg mb-3">시나리오별 KPI 범위</h3>
                {cls._generate_scenario_table(risk_data.get('scenarios', {}))}
            </div>
        </div>
        
        <!-- 의사결정 스코어카드 -->
        <div class="card p-8">
            <h2 class="section-title">🎯 의사결정 스코어카드</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {cls._generate_scorecard(decision_data.get('scorecard', {}))}
            </div>
            
            <div class="mt-6 p-6 {cls._get_decision_banner_color(decision_data.get('decision', '보류'))} rounded-lg">
                <h3 class="font-bold text-2xl mb-2">최종 결론</h3>
                <p class="text-xl mb-4">{decision_data.get('decision', '보류')}</p>
                <p class="text-lg opacity-90">{decision_data.get('rationale', '분석 중...')}</p>
                {cls._generate_next_steps(decision_data)}
            </div>
        </div>
        
    </div>
    
    <!-- 푸터 -->
    <div class="max-w-6xl mx-auto mt-8 text-center text-gray-500 text-sm">
        <p>Generated by Multi-Market Entry Strategy Agent v1.0</p>
        <p class="mt-2">이 보고서는 자동 생성된 전략 분석 결과입니다. 최종 의사결정 시 전문가 검토를 권장합니다.</p>
    </div>
</body>
</html>
"""
        return html
    
    @staticmethod
    def _get_score_bg_color(score: int) -> str:
        """점수에 따른 배경색"""
        if score >= 80:
            return "bg-green-500 text-white"
        elif score >= 60:
            return "bg-blue-500 text-white"
        elif score >= 40:
            return "bg-yellow-500 text-white"
        else:
            return "bg-red-500 text-white"
    
    @staticmethod
    def _get_decision_banner_color(decision: str) -> str:
        """의사결정 배너 색상"""
        if "진행" in decision or "추천" in decision:
            return "bg-gradient-to-r from-blue-600 to-blue-800 text-white"
        elif "보류" in decision:
            return "bg-gradient-to-r from-orange-600 to-orange-800 text-white"
        else:
            return "bg-gradient-to-r from-gray-600 to-gray-800 text-white"
    
    @staticmethod
    def _generate_metric_cards(metrics: Dict) -> str:
        """핵심 지표 카드 생성"""
        cards = []
        for key, value in metrics.items():
            cards.append(f"""
                <div class="metric-card">
                    <div class="text-2xl font-bold text-gray-800 mb-1">{value}</div>
                    <div class="text-sm text-gray-600">{key}</div>
                </div>
            """)
        return "".join(cards) if cards else "<p class='text-gray-500'>지표 수집 중...</p>"
    
    @staticmethod
    def _generate_image_section(title: str, image_base64: Optional[str]) -> str:
        """이미지 섹션 생성"""
        if not image_base64:
            return f"""
                <div class="mb-6">
                    <h3 class="font-bold text-lg mb-3">{title}</h3>
                    <div class="bg-gray-100 rounded-lg p-8 text-center text-gray-500">
                        이미지 생성 중...
                    </div>
                </div>
            """
        
        return f"""
            <div class="mb-6">
                <h3 class="font-bold text-lg mb-3">{title}</h3>
                <div class="rounded-lg overflow-hidden border border-gray-200">
                    <img src="data:image/png;base64,{image_base64}" alt="{title}" class="w-full">
                </div>
            </div>
        """
    
    @staticmethod
    def _generate_regulatory_table(checklist: List[Dict]) -> str:
        """규제 체크리스트 테이블 생성"""
        if not checklist:
            return "<p class='text-gray-500'>체크리스트 작성 중...</p>"
        
        rows = []
        for item in checklist:
            status_badge = {
                "PASS": "bg-green-100 text-green-800",
                "WARN": "bg-yellow-100 text-yellow-800",
                "TBD": "bg-gray-100 text-gray-800",
                "NA": "bg-gray-50 text-gray-500"
            }.get(item.get('state', 'NA'), "bg-gray-100 text-gray-800")
            
            grade_badge = {
                "MUST": "bg-red-100 text-red-800 border-red-300",
                "SHOULD": "bg-orange-100 text-orange-800 border-orange-300",
                "NICE": "bg-blue-100 text-blue-800 border-blue-300"
            }.get(item.get('grade', 'NICE'), "bg-gray-100 text-gray-800")
            
            rows.append(f"""
                <tr class="border-b border-gray-200 hover:bg-gray-50">
                    <td class="py-3 px-4">{item.get('item', '-')}</td>
                    <td class="py-3 px-4 text-center">
                        <span class="badge {grade_badge}">{item.get('grade', '-')}</span>
                    </td>
                    <td class="py-3 px-4 text-center">
                        <span class="badge {status_badge}">{item.get('state', '-')}</span>
                    </td>
                    <td class="py-3 px-4 text-sm text-gray-600">{item.get('evidence', '-')}</td>
                </tr>
            """)
        
        return f"""
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="py-3 px-4 text-left font-semibold">항목</th>
                            <th class="py-3 px-4 text-center font-semibold">등급</th>
                            <th class="py-3 px-4 text-center font-semibold">상태</th>
                            <th class="py-3 px-4 text-left font-semibold">근거/출처</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(rows)}
                    </tbody>
                </table>
            </div>
        """
    
    @staticmethod
    def _generate_whitespace_cards(gaps: List[str]) -> str:
        """화이트스페이스 카드 생성"""
        if not gaps:
            return "<p class='text-gray-500 col-span-3'>기회 영역 분석 중...</p>"
        
        cards = []
        icons = ["💡", "🎯", "🚀"]
        for i, gap in enumerate(gaps[:3]):
            icon = icons[i] if i < len(icons) else "✨"
            cards.append(f"""
                <div class="bg-gradient-to-br from-purple-50 to-pink-50 p-6 rounded-lg border-2 border-purple-200">
                    <div class="text-3xl mb-2">{icon}</div>
                    <p class="text-gray-800 font-medium">{gap}</p>
                </div>
            """)
        return "".join(cards)
    
    @staticmethod
    def _generate_partner_table(candidates: List[Dict]) -> str:
        """파트너 후보 테이블 생성"""
        if not candidates:
            return "<p class='text-gray-500'>파트너 발굴 중...</p>"
        
        rows = []
        for partner in candidates:
            rows.append(f"""
                <tr class="border-b border-gray-200 hover:bg-gray-50">
                    <td class="py-3 px-4 font-medium">{partner.get('name', '-')}</td>
                    <td class="py-3 px-4">
                        <span class="badge bg-blue-100 text-blue-800 border-blue-300">{partner.get('role', '-')}</span>
                    </td>
                    <td class="py-3 px-4 text-sm text-gray-600">{partner.get('rationale', '-')}</td>
                    <td class="py-3 px-4 text-sm text-gray-500">{partner.get('alternative', '-')}</td>
                </tr>
            """)
        
        return f"""
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="py-3 px-4 text-left font-semibold">업체명</th>
                            <th class="py-3 px-4 text-left font-semibold">역할</th>
                            <th class="py-3 px-4 text-left font-semibold">선정 이유</th>
                            <th class="py-3 px-4 text-left font-semibold">대안</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(rows)}
                    </tbody>
                </table>
            </div>
        """
    
    @staticmethod
    def _generate_risk_table(risks: List[Dict]) -> str:
        """리스크 레지스터 테이블 생성"""
        if not risks:
            return "<p class='text-gray-500'>리스크 분석 중...</p>"
        
        rows = []
        for risk in risks:
            likelihood = risk.get('likelihood', '보통')
            impact = risk.get('impact', '보통')
            
            likelihood_color = {
                "높음": "text-red-600",
                "보통": "text-yellow-600",
                "낮음": "text-green-600"
            }.get(likelihood, "text-gray-600")
            
            impact_color = {
                "높음": "text-red-600",
                "보통": "text-yellow-600",
                "낮음": "text-green-600"
            }.get(impact, "text-gray-600")
            
            rows.append(f"""
                <tr class="border-b border-gray-200 hover:bg-gray-50">
                    <td class="py-3 px-4">{risk.get('risk', '-')}</td>
                    <td class="py-3 px-4 text-center {likelihood_color} font-semibold">{likelihood}</td>
                    <td class="py-3 px-4 text-center {impact_color} font-semibold">{impact}</td>
                    <td class="py-3 px-4 text-sm text-gray-600">{risk.get('early_sign', '-')}</td>
                    <td class="py-3 px-4 text-sm text-gray-700">{risk.get('mitigation', '-')}</td>
                </tr>
            """)
        
        return f"""
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="py-3 px-4 text-left font-semibold">리스크</th>
                            <th class="py-3 px-4 text-center font-semibold">가능성</th>
                            <th class="py-3 px-4 text-center font-semibold">영향</th>
                            <th class="py-3 px-4 text-left font-semibold">초기 징후</th>
                            <th class="py-3 px-4 text-left font-semibold">완화 전략</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(rows)}
                    </tbody>
                </table>
            </div>
        """
    
    @staticmethod
    def _generate_scenario_table(scenarios: Dict) -> str:
        """시나리오별 KPI 테이블 생성"""
        if not scenarios:
            return "<p class='text-gray-500'>시나리오 분석 중...</p>"
        
        return f"""
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-red-50 p-6 rounded-lg border-2 border-red-200">
                    <h4 class="font-bold text-lg mb-3 text-red-800">😰 비관 시나리오</h4>
                    <div class="space-y-2 text-sm text-gray-700">
                        {StrategyReportTemplate._format_kpi_list(scenarios.get('pessimistic', {}))}
                    </div>
                </div>
                <div class="bg-blue-50 p-6 rounded-lg border-2 border-blue-200">
                    <h4 class="font-bold text-lg mb-3 text-blue-800">😐 기준 시나리오</h4>
                    <div class="space-y-2 text-sm text-gray-700">
                        {StrategyReportTemplate._format_kpi_list(scenarios.get('base', {}))}
                    </div>
                </div>
                <div class="bg-green-50 p-6 rounded-lg border-2 border-green-200">
                    <h4 class="font-bold text-lg mb-3 text-green-800">😄 낙관 시나리오</h4>
                    <div class="space-y-2 text-sm text-gray-700">
                        {StrategyReportTemplate._format_kpi_list(scenarios.get('optimistic', {}))}
                    </div>
                </div>
            </div>
        """
    
    @staticmethod
    def _format_kpi_list(kpis: Dict) -> str:
        """KPI 리스트 포맷팅"""
        if not kpis:
            return "<p class='text-gray-500'>데이터 없음</p>"
        
        items = []
        for key, value in kpis.items():
            items.append(f"<p><span class='font-semibold'>{key}:</span> {value}</p>")
        return "".join(items)
    
    @staticmethod
    def _generate_scorecard(scorecard: Dict) -> str:
        """스코어카드 생성"""
        if not scorecard:
            return "<p class='text-gray-500 col-span-2'>스코어카드 계산 중...</p>"
        
        items = []
        for category, score in scorecard.items():
            # 점수를 0-100 범위로 정규화
            if isinstance(score, (int, float)):
                normalized = min(100, max(0, score))
                color = "bg-green-500" if normalized >= 70 else "bg-yellow-500" if normalized >= 40 else "bg-red-500"
            else:
                normalized = 50
                color = "bg-gray-500"
            
            items.append(f"""
                <div class="bg-white p-6 rounded-lg border-2 border-gray-200">
                    <h4 class="font-semibold mb-3 text-gray-700">{category}</h4>
                    <div class="flex items-end gap-4">
                        <div class="text-3xl font-bold text-gray-800">{score}</div>
                        <div class="flex-1">
                            <div class="h-3 bg-gray-200 rounded-full overflow-hidden">
                                <div class="{color} h-full transition-all duration-500" style="width: {normalized}%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            """)
        
        return "".join(items)
    
    @staticmethod
    def _generate_next_steps(decision_data: Dict) -> str:
        """다음 단계 생성"""
        next_steps = decision_data.get('next_steps', [])
        if not next_steps:
            return ""
        
        steps_html = []
        for i, step in enumerate(next_steps, 1):
            steps_html.append(f"<li class='flex items-start gap-3'><span class='font-bold'>{i}.</span><span>{step}</span></li>")
        
        return f"""
            <div class="mt-6 pt-6 border-t border-white/30">
                <h4 class="font-bold text-lg mb-3">📌 Next Steps</h4>
                <ul class="space-y-2">
                    {"".join(steps_html)}
                </ul>
            </div>
        """


# 사용 예시
if __name__ == "__main__":
    # 예시 데이터
    sample_data = {
        "company": "스타트업A",
        "country": "베트남",
        "market_summary": {
            "metrics": {
                "TAM": "$2.5B",
                "성장률": "15% YoY",
                "택배량": "500M건/년",
                "평균 배송비": "$2.50",
                "리드타임": "2-3일"
            },
            "why_now": "이커머스 급성장(35% YoY)과 중산층 확대로 빠른 배송 수요 증가. 정부의 물류 인프라 투자로 진입 장벽 완화."
        },
        "regulatory_data": {
            "coverage_score": 0.76,
            "risk_badge": "보통",
            "checklist": [
                {"item": "택배업 등록", "grade": "MUST", "state": "PASS", "evidence": "국토부 고시 확인"},
                {"item": "개인정보 국외이전", "grade": "MUST", "state": "TBD", "evidence": "DPA 근거 미확인"},
                {"item": "환불·반품 고지", "grade": "SHOULD", "state": "PASS", "evidence": "공정위 고시"},
            ]
        },
        "competitor_data": {
            "whitespace_gaps": [
                "농촌 지역 당일배송 서비스 부재",
                "프리미엄 콜드체인 물류 미개척",
                "중소기업 전용 통합 플랫폼 없음"
            ]
        },
        "partner_data": {
            "candidates": [
                {"name": "VietPost", "role": "라스트마일", "rationale": "전국 네트워크", "alternative": "Giao Hang Nhanh"},
                {"name": "TechCorp", "role": "시스템 통합", "rationale": "현지 경험 풍부", "alternative": "FPT Software"}
            ],
            "poc_proposal": "1단계: 호치민 시범 운영 (3개월)\n2단계: 하노이 확장\n3단계: 전국 네트워크"
        },
        "risk_data": {
            "register": [
                {"risk": "규제 변경", "likelihood": "보통", "impact": "높음", "early_sign": "정부 발표", "mitigation": "로비스트 고용"},
                {"risk": "파트너 이탈", "likelihood": "낮음", "impact": "높음", "early_sign": "SLA 미달", "mitigation": "복수 파트너 확보"}
            ],
            "scenarios": {
                "pessimistic": {"월 거래량": "10K건", "수익": "-$50K"},
                "base": {"월 거래량": "30K건", "수익": "$20K"},
                "optimistic": {"월 거래량": "100K건", "수익": "$150K"}
            }
        },
        "decision_data": {
            "decision": "진행(추천)",
            "rationale": "시장 성장성과 실행 가능성 높음. 규제 리스크는 관리 가능한 수준.",
            "final_score": 72,
            "scorecard": {
                "시장 매력도": 85,
                "규제 리스크": 65,
                "경쟁 강도": 60,
                "실행 가능성": 75,
                "파트너 가용성": 80
            },
            "next_steps": [
                "DPA 협약 체결 (2주)",
                "VietPost와 MOU 체결 (1개월)",
                "호치민 파일럿 준비 (2개월)"
            ]
        },
        "visualizations": {}
    }
    
    template = StrategyReportTemplate()
    html = template.generate_html_report(**sample_data)
    
    with open("/tmp/test_report.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("테스트 보고서 생성 완료: /tmp/test_report.html")
