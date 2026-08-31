import math
import html
import textwrap

import numpy as np
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="팝업 전략 시뮬레이터",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_html(content):
    st.html(textwrap.dedent(content).strip())


def safe(value):
    return html.escape(str(value))


def fmt_int(value):
    return f"{int(round(value)):,}"


def fmt_currency(value, lang):
    if lang == "ko":
        return f"{int(round(value)):,}원"
    return f"₩{int(round(value)):,}"


render_html(
    """
    <style>
        :root {
            --bg: #F4F1EA;
            --paper: #FFFEFA;
            --ink: #1E1E1B;
            --muted: #6C6A63;
            --line: #D8D3C8;
            --sky: #84A9C8;
            --yellow: #D8B45B;
            --red: #B96A5E;
            --green: #6F8C74;
        }

        .stApp {
            background: var(--bg);
            color: var(--ink);
        }

        .block-container {
            max-width: 1220px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        h1, h2, h3, h4, p, div, span, label {
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Apple SD Gothic Neo",
                "Noto Sans KR",
                "Segoe UI",
                sans-serif;
        }

        [data-testid="stHeader"] {
            background: rgba(244, 241, 234, 0.94);
        }

        .hero {
            border-top: 1px solid var(--ink);
            border-bottom: 1px solid var(--ink);
            padding: 2.2rem 0 1.9rem 0;
            margin: 0.2rem 0 2.2rem 0;
        }

        .hero-kicker {
            font-size: 0.78rem;
            letter-spacing: 0.15em;
            color: var(--muted);
            margin-bottom: 0.7rem;
        }

        .hero-title {
            font-size: clamp(2.4rem, 5vw, 4.8rem);
            line-height: 0.98;
            font-weight: 800;
            letter-spacing: -0.055em;
            margin: 0;
            color: var(--ink);
        }

        .hero-sub {
            margin-top: 1rem;
            font-size: 1rem;
            line-height: 1.65;
            color: var(--muted);
            max-width: 800px;
        }

        .hero-note {
            margin-top: 1rem;
            font-size: 0.75rem;
            line-height: 1.5;
            color: #817D74;
        }

        .section-head {
            margin-top: 2.3rem;
            margin-bottom: 1rem;
        }

        .section-tag {
            font-size: 0.72rem;
            letter-spacing: 0.14em;
            color: var(--muted);
            margin-bottom: 0.3rem;
        }

        .section-title {
            font-size: 2rem;
            font-weight: 780;
            letter-spacing: -0.035em;
            margin-bottom: 0.35rem;
        }

        .section-copy {
            color: var(--muted);
            font-size: 0.93rem;
            line-height: 1.6;
            max-width: 860px;
        }

        .brief-card,
        .result-card,
        .strategy-card,
        .status-card,
        .sample-card,
        .formula-card {
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 10px;
            box-shadow: none;
        }

        .brief-card {
            padding: 1.45rem;
        }

        .brief-overline {
            font-size: 0.72rem;
            letter-spacing: 0.12em;
            color: var(--muted);
            margin-bottom: 0.7rem;
        }

        .brief-title {
            font-size: 1.7rem;
            line-height: 1.2;
            font-weight: 780;
            letter-spacing: -0.035em;
            margin-bottom: 0.3rem;
        }

        .brief-project {
            font-size: 0.92rem;
            color: var(--muted);
            margin-bottom: 1rem;
        }

        .brief-meta {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.8rem 1rem;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--line);
        }

        .label-small {
            font-size: 0.72rem;
            color: var(--muted);
            margin-bottom: 0.15rem;
        }

        .value-normal {
            font-size: 0.93rem;
            font-weight: 650;
            line-height: 1.4;
        }

        .concept-box {
            margin-top: 1rem;
            padding: 0.85rem 0.95rem;
            background: #F7F3E9;
            border-left: 3px solid var(--yellow);
            font-size: 0.9rem;
            line-height: 1.6;
        }

        .data-chip {
            display: inline-block;
            font-size: 0.74rem;
            color: var(--muted);
            border: 1px solid var(--line);
            background: var(--paper);
            border-radius: 999px;
            padding: 0.3rem 0.6rem;
            margin-bottom: 0.5rem;
        }

        .result-card {
            padding: 1.05rem 1.1rem;
            min-height: 125px;
        }

        .result-label {
            font-size: 0.78rem;
            color: var(--muted);
            margin-bottom: 0.45rem;
        }

        .result-number {
            font-size: 1.7rem;
            line-height: 1.05;
            font-weight: 790;
            letter-spacing: -0.04em;
        }

        .result-note {
            font-size: 0.73rem;
            color: var(--muted);
            line-height: 1.45;
            margin-top: 0.55rem;
        }

        .formula-card {
            padding: 1rem 1.15rem;
            margin: 0.6rem 0 1.1rem 0;
        }

        .formula {
            font-size: 1.05rem;
            line-height: 1.8;
            font-weight: 650;
        }

        .sample-card {
            padding: 0.85rem 0.9rem;
        }

        .sample-n {
            font-size: 0.74rem;
            color: var(--muted);
        }

        .sample-error {
            font-size: 1.25rem;
            font-weight: 760;
            margin-top: 0.2rem;
        }

        .status-card {
            padding: 1.25rem 1.35rem;
        }

        .badge {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 760;
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            margin-bottom: 0.8rem;
        }

        .badge-safe {
            background: #E7EFE8;
            color: #46614C;
        }

        .badge-caution {
            background: #F5ECD5;
            color: #735A1D;
        }

        .badge-adjust {
            background: #F2E1DE;
            color: #7A4038;
        }

        .status-number {
            font-size: 1.5rem;
            font-weight: 790;
            letter-spacing: -0.035em;
            margin-bottom: 0.35rem;
        }

        .status-copy {
            font-size: 0.9rem;
            line-height: 1.6;
            color: var(--muted);
        }

        .strategy-card {
            padding: 1.1rem 1.25rem;
        }

        .strategy-row {
            padding: 0.7rem 0;
            border-bottom: 1px solid #E8E3D8;
        }

        .strategy-row:last-child {
            border-bottom: 0;
        }

        .strategy-key {
            font-size: 0.72rem;
            color: var(--muted);
            margin-bottom: 0.15rem;
        }

        .strategy-value {
            font-size: 0.98rem;
            line-height: 1.45;
            font-weight: 660;
        }

        .dark-message {
            background: #1F1F1C;
            color: #FFFDF6;
            border-radius: 10px;
            padding: 1.4rem 1.5rem;
            margin-top: 1rem;
        }

        .dark-message-main {
            font-size: 1.2rem;
            font-weight: 730;
            line-height: 1.55;
            letter-spacing: -0.025em;
        }

        .dark-message-sub {
            color: #D0CCC3;
            font-size: 0.8rem;
            margin-top: 0.55rem;
        }

        div[data-baseweb="select"] > div,
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea {
            background: #FFFEFA !important;
            border-color: var(--line) !important;
        }

        .stButton > button {
            border-radius: 6px;
            background: var(--paper);
            color: var(--ink);
            border: 1px solid var(--ink);
            box-shadow: none;
        }

        @media (max-width: 760px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .hero-title {
                font-size: 2.6rem;
            }

            .brief-meta {
                grid-template-columns: 1fr;
            }

            .result-number {
                font-size: 1.4rem;
            }
        }
    </style>
    """
)


TEXT = {
    "ko": {
        "hero_kicker": "STÜSSY × TOY STORY · 가상 협업 프로젝트 · 더현대 서울",
        "hero_title": "팝업 전략 시뮬레이터",
        "hero_sub": "창의적인 팝업 기획을 통계적 추정으로 실제 운영 가능한 규모까지 연결하는 교육용 시뮬레이션",
        "hero_note": "학교 통계 활동을 위해 제작한 가상의 협업 시뮬레이션 · Stüssy, Toy Story, Disney/Pixar 및 더현대 서울과 공식적인 관련 없음",
        "s1": "팝업 기획",
        "s1_copy": "협업 콘셉트와 운영 조건을 직접 설정하고 기획 요약을 한 화면에서 확인",
        "s2": "기준 데이터 설정",
        "s2_copy": "유사한 조건의 팝업스토어 데이터를 가정해 통계적 추정에 필요한 표본 정보를 설정",
        "s3": "통계적 추정",
        "s3_copy": "모표준편차를 알고 있다는 가정 아래 95% 신뢰구간과 오차범위를 계산",
        "s4": "운영 시뮬레이션",
        "s4_copy": "표본 크기가 달라질 때 추정의 정밀도가 어떻게 변하는지 비교",
        "s5": "운영 적정성 분석",
        "s5_copy": "추정된 평균 일 방문객 범위와 현재 일일 수용 가능 인원을 비교",
        "s6": "원하는 정확도에 필요한 표본",
        "s6_copy": "목표 오차범위를 정하고 그 정확도에 필요한 최소 표본 수를 계산",
        "s7": "전략 요약",
        "s7_copy": "기획 정보와 통계 분석 결과를 하나의 브랜드 전략 요약으로 정리",
        "brief": "기획 요약",
        "collab_project": "협업 프로젝트",
        "popup_name": "팝업명",
        "location": "장소",
        "collab_type": "협업 형태",
        "characters": "대표 캐릭터 / 테마",
        "products": "대표 판매 제품",
        "space_concept": "공간 콘셉트",
        "days": "운영 기간",
        "space_size": "공간 크기",
        "staff": "운영 인력",
        "capacity": "일일 수용 가능 인원",
        "budget": "전체 예산",
        "concept_line": "콘셉트 한 줄",
        "days_unit": "일",
        "staff_unit": "명",
        "visitors": "명",
        "samples": "개",
        "budget_note": "기획 정보로만 사용 · 통계 계산에는 포함하지 않음",
        "virtual_data": "교육용 가상 표본 데이터",
        "virtual_desc": "유사한 조건의 팝업스토어 운영 데이터를 가정",
        "sample_n": "표본 크기 n",
        "sample_mean": "표본평균 x̄",
        "sample_mean_help": "유사 팝업의 평균 일 방문객",
        "sigma": "모표준편차 σ",
        "sigma_help": "유사 팝업의 일 방문객 변동 정도",
        "formula_title": "사용 공식",
        "sample_mean_card": "표본평균",
        "moe": "오차범위",
        "ci": "95% 신뢰구간",
        "period": "운영기간 환산",
        "period_note": "평균 일 방문객 신뢰구간을 운영일수에 맞게 단순 환산한 참고값 · 특정 날짜 또는 전체 방문객의 예측구간은 아님",
        "ci_chart": "95% 신뢰구간",
        "mean": "평균",
        "lower": "하한",
        "upper": "상한",
        "sample_chart": "표본 크기에 따른 오차범위 변화",
        "sample_x": "표본 크기 n",
        "error_y": "오차범위",
        "sample_desc": "표본이 많아질수록 오차범위 감소 → 모평균을 더 정밀하게 추정",
        "compare": "표본 크기 비교",
        "current_n": "현재 n",
        "safe": "운영 안정",
        "caution": "수용량 주의",
        "adjust": "운영 조정 필요",
        "safe_copy": "추정된 평균 방문 규모가 현재 수용 범위 안",
        "caution_copy": "예상 방문 규모의 일부가 현재 운영 범위를 초과",
        "adjust_copy": "추정된 평균 방문 규모가 현재 수용량보다 높음",
        "risk": "주요 위험",
        "risk_safe": "큰 수용량 위험 신호 없음",
        "risk_caution": "피크 시간 혼잡 가능성",
        "risk_adjust": "지속적인 수용량 부족 가능성",
        "recommend": "권장 조정",
        "rec_safe": "현재 운영 규모 유지 · 실제 운영 전 시간대별 수요 추가 확인",
        "rec_caution": "입장 시간 분산 · 대기 동선 확보 · 피크타임 추가 인력 검토",
        "rec_adjust": "수용 인원 확대 · 예약제 또는 회차제 검토 · 운영 동선 재설계",
        "target_error": "목표 오차범위",
        "min_sample": "필요 최소 표본",
        "additional": "추가 필요 표본",
        "goal_met": "현재 표본으로 목표 정확도 충족",
        "need_sentence": "오차범위를 ±{error}명 이내로 줄이려면 최소 {n}개의 표본 필요",
        "project": "프로젝트",
        "operating_days": "운영 기간",
        "daily_demand": "예상 평균 일 방문 규모",
        "daily_capacity": "일일 수용 가능 인원",
        "status": "운영 상태",
        "precision": "데이터 정확도",
        "target_precision": "목표 정확도",
        "core": "창의적인 팝업 기획을 통계적 추정을 통해 실제 실행 가능한 전략으로 연결",
        "core_sub": "Creative Direction × Brand Analytics × Statistical Estimation",
        "warning": "통계 해석 시 주의",
        "w1": "본 앱의 데이터는 교육용 가상 데이터",
        "w2": "모표준편차를 알고 있다고 가정",
        "w3": "신뢰구간은 평균 일 방문객에 대한 추정",
        "w4": "특정 하루의 방문객 예측구간과는 다름",
        "w5": "실제 운영에는 비용, 안전, 시간대별 방문 패턴 등 추가 정보 필요",
        "w6": "모집단이 정규분포를 따르거나 표본이 충분히 큰 상황을 가정",
        "collab_values": {
            "limited": "한정 협업 컬렉션",
            "new": "신제품 공개",
            "film": "브랜드 × 영화 협업",
            "season": "시즌 한정 프로젝트",
        },
        "character_values": {
            "woody": "우디",
            "buzz": "버즈 라이트이어",
            "alien": "알린",
            "jessie": "제시",
            "all": "전체 캐릭터",
        },
        "product_values": {
            "tee": "티셔츠",
            "hoodie": "후디",
            "cap": "캡",
            "bag": "가방",
            "acc": "액세서리",
        },
        "space_values": {
            "andy": "앤디의 방",
            "space": "우주 테마",
            "toybox": "장난감 상자",
            "street": "스트리트 그래픽",
            "mixed": "혼합 콘셉트",
        },
    },

    "en": {
        "hero_kicker": "STÜSSY × TOY STORY · CONCEPT COLLABORATION · THE HYUNDAI SEOUL",
        "hero_title": "Pop-up Strategy Simulator",
        "hero_sub": "An educational simulator connecting creative pop-up planning with executable scale through statistical estimation",
        "hero_note": "Fictional collaboration simulator for a school statistics project · Not officially affiliated with Stüssy, Toy Story, Disney/Pixar, or The Hyundai Seoul",
        "s1": "Pop-up Planning",
        "s1_copy": "Set the collaboration concept and operating conditions and review the creative brief",
        "s2": "Reference Data",
        "s2_copy": "Set fictional sample information from comparable pop-up operations",
        "s3": "Statistical Estimation",
        "s3_copy": "Calculate the 95% confidence interval and margin of error assuming population standard deviation is known",
        "s4": "Operating Simulation",
        "s4_copy": "Compare how statistical precision changes as sample size changes",
        "s5": "Capacity Review",
        "s5_copy": "Compare estimated mean daily visitor demand with planned daily capacity",
        "s6": "Required Sample Size",
        "s6_copy": "Choose a target margin of error and calculate the minimum required sample",
        "s7": "Strategy Summary",
        "s7_copy": "Combine the creative brief and statistical results into one strategy summary",
        "brief": "Creative brief",
        "collab_project": "Collaboration project",
        "popup_name": "Pop-up name",
        "location": "Location",
        "collab_type": "Collaboration type",
        "characters": "Featured characters / theme",
        "products": "Featured products",
        "space_concept": "Space concept",
        "days": "Operating days",
        "space_size": "Space size",
        "staff": "Staff",
        "capacity": "Daily capacity",
        "budget": "Total budget",
        "concept_line": "Concept line",
        "days_unit": "days",
        "staff_unit": "staff",
        "visitors": "visitors",
        "samples": "obs.",
        "budget_note": "Planning information only · Not included in statistical calculations",
        "virtual_data": "Fictional educational sample data",
        "virtual_desc": "Assumed data from comparable pop-up operations",
        "sample_n": "Sample size n",
        "sample_mean": "Sample mean x̄",
        "sample_mean_help": "Average daily visitors from comparable pop-ups",
        "sigma": "Population standard deviation σ",
        "sigma_help": "Variation in daily visitors across comparable pop-ups",
        "formula_title": "Formula",
        "sample_mean_card": "Sample mean",
        "moe": "Margin of error",
        "ci": "95% confidence interval",
        "period": "Operating-period reference",
        "period_note": "Simple multiplication of the mean-daily-visitor confidence interval by operating days · Not a prediction interval for a specific day or total attendance",
        "ci_chart": "95% Confidence Interval",
        "mean": "Mean",
        "lower": "Lower",
        "upper": "Upper",
        "sample_chart": "Sample Size vs Margin of Error",
        "sample_x": "Sample size n",
        "error_y": "Margin of error",
        "sample_desc": "Larger sample → smaller margin of error → more precise estimation",
        "compare": "Sample-size comparison",
        "current_n": "Current n",
        "safe": "Capacity Stable",
        "caution": "Capacity Caution",
        "adjust": "Adjustment Needed",
        "safe_copy": "Estimated mean visitor demand remains within current capacity",
        "caution_copy": "Part of the estimated mean visitor range exceeds current capacity",
        "adjust_copy": "Estimated mean visitor demand is above current capacity",
        "risk": "Main risk",
        "risk_safe": "No major capacity warning",
        "risk_caution": "Possible peak-time congestion",
        "risk_adjust": "Possible persistent capacity shortage",
        "recommend": "Recommended adjustment",
        "rec_safe": "Keep current scale · Check time-of-day demand before launch",
        "rec_caution": "Distribute entry times · Secure queue flow · Review peak-time staffing",
        "rec_adjust": "Increase capacity · Review reservation/session entry · Redesign operating flow",
        "target_error": "Target margin of error",
        "min_sample": "Minimum sample required",
        "additional": "Additional samples needed",
        "goal_met": "Current sample meets the target precision",
        "need_sentence": "To keep the margin of error within ±{error} visitors, at least {n} observations are required",
        "project": "Project",
        "operating_days": "Operating days",
        "daily_demand": "Estimated mean daily visitors",
        "daily_capacity": "Daily capacity",
        "status": "Operating status",
        "precision": "Data precision",
        "target_precision": "Target precision",
        "core": "Connecting creative pop-up planning with executable strategy through statistical estimation",
        "core_sub": "Creative Direction × Brand Analytics × Statistical Estimation",
        "warning": "Statistical interpretation notes",
        "w1": "All app data are fictional and for educational use",
        "w2": "Population standard deviation is assumed to be known",
        "w3": "The confidence interval estimates mean daily visitors",
        "w4": "It is not a prediction interval for a specific day",
        "w5": "Real operations also require cost, safety, and time-of-day demand data",
        "w6": "A normal population or sufficiently large sample is assumed",
        "collab_values": {
            "limited": "Limited collaboration collection",
            "new": "New product launch",
            "film": "Brand × film collaboration",
            "season": "Seasonal limited project",
        },
        "character_values": {
            "woody": "Woody",
            "buzz": "Buzz Lightyear",
            "alien": "Aliens",
            "jessie": "Jessie",
            "all": "All characters",
        },
        "product_values": {
            "tee": "T-shirts",
            "hoodie": "Hoodies",
            "cap": "Caps",
            "bag": "Bags",
            "acc": "Accessories",
        },
        "space_values": {
            "andy": "Andy's room",
            "space": "Space theme",
            "toybox": "Toy box",
            "street": "Street graphics",
            "mixed": "Mixed concept",
        },
    },
}


if "language_selector" not in st.session_state:
    st.session_state.language_selector = "한국어"


_, language_col = st.columns([5.2, 1.3])

with language_col:
    selected_language = st.radio(
        "Language",
        ["한국어", "English"],
        horizontal=True,
        label_visibility="collapsed",
        key="language_selector",
    )


LANG = "ko" if selected_language == "한국어" else "en"


def t(key):
    return TEXT[LANG][key]


def section_header(number, title, copy):
    render_html(
        f"""
        <div class="section-head">
            <div class="section-tag">{safe(number)}</div>
            <div class="section-title">{safe(title)}</div>
            <div class="section-copy">{safe(copy)}</div>
        </div>
        """
    )


def result_card(label, value, detail=""):
    detail_html = ""

    if detail:
        detail_html = f'<div class="result-note">{safe(detail)}</div>'

    return f"""
    <div class="result-card">
        <div class="result-label">{safe(label)}</div>
        <div class="result-number">{safe(value)}</div>
        {detail_html}
    </div>
    """


render_html(
    f"""
    <div class="hero">
        <div class="hero-kicker">{safe(t("hero_kicker"))}</div>
        <div class="hero-title">{safe(t("hero_title"))}</div>
        <div class="hero-sub">{safe(t("hero_sub"))}</div>
        <div class="hero-note">{safe(t("hero_note"))}</div>
    </div>
    """
)


section_header("01", t("s1"), t("s1_copy"))


planning_left, planning_right = st.columns(
    [1.1, 0.9],
    gap="large",
)


with planning_left:

    collab_project = st.text_input(
        t("collab_project"),
        value="Stüssy × Toy Story",
        key="collab_project",
    )

    if "popup_name" not in st.session_state:
        st.session_state.popup_name = "스투시 × 토이 스토리 협업 팝업"

    popup_name = st.text_input(
        t("popup_name"),
        key="popup_name",
    )

    if "popup_location" not in st.session_state:
        st.session_state.popup_location = "더현대 서울"

    popup_location = st.text_input(
        t("location"),
        key="popup_location",
    )

    form_left, form_right = st.columns(2)

    with form_left:

        collab_type = st.selectbox(
            t("collab_type"),
            options=[
                "limited",
                "new",
                "film",
                "season",
            ],
            index=2,
            format_func=lambda x: t("collab_values")[x],
            key="collab_type",
        )

        selected_characters = st.multiselect(
            t("characters"),
            options=[
                "woody",
                "buzz",
                "alien",
                "jessie",
                "all",
            ],
            default=["all"],
            format_func=lambda x: t("character_values")[x],
            key="characters",
        )

        selected_products = st.multiselect(
            t("products"),
            options=[
                "tee",
                "hoodie",
                "cap",
                "bag",
                "acc",
            ],
            default=[
                "tee",
                "hoodie",
                "cap",
                "bag",
            ],
            format_func=lambda x: t("product_values")[x],
            key="products",
        )

        space_concept = st.selectbox(
            t("space_concept"),
            options=[
                "andy",
                "space",
                "toybox",
                "street",
                "mixed",
            ],
            index=3,
            format_func=lambda x: t("space_values")[x],
            key="space_concept",
        )

    with form_right:

        operating_days = st.slider(
            t("days"),
            min_value=1,
            max_value=30,
            value=7,
            step=1,
            key="operating_days",
        )

        space_size = st.slider(
            t("space_size"),
            min_value=30,
            max_value=500,
            value=120,
            step=10,
            key="space_size",
        )

        staff_count = st.slider(
            t("staff"),
            min_value=2,
            max_value=50,
            value=8,
            step=1,
            key="staff_count",
        )

        daily_capacity = st.slider(
            t("capacity"),
            min_value=100,
            max_value=5000,
            value=1750,
            step=50,
            key="daily_capacity",
        )

    budget = st.number_input(
        t("budget"),
        min_value=1_000_000,
        max_value=500_000_000,
        value=35_000_000,
        step=1_000_000,
        key="budget",
    )

    st.caption(t("budget_note"))

    if "concept_line" not in st.session_state:
        st.session_state.concept_line = (
            "토이 스토리의 친숙한 세계관을 "
            "스투시의 스트리트 감성으로 재해석한 "
            "한정 협업 공간"
        )

    concept_line = st.text_area(
        t("concept_line"),
        key="concept_line",
        height=90,
    )


with planning_right:

    character_labels = (
        [
            t("character_values")[item]
            for item in selected_characters
        ]
        if selected_characters
        else ["-"]
    )

    product_labels = (
        [
            t("product_values")[item]
            for item in selected_products
        ]
        if selected_products
        else ["-"]
    )

    render_html(
        f"""
        <div class="brief-card">
            <div class="brief-overline">
                {safe(t("brief"))}
            </div>

            <div class="brief-title">
                {safe(popup_name)}
            </div>

            <div class="brief-project">
                {safe(collab_project)}
            </div>

            <div class="value-normal">
                {safe(popup_location)}
            </div>

            <div style="
                margin-top:0.35rem;
                color:#6C6A63;
                font-size:0.9rem;
            ">
                {operating_days} {safe(t("days_unit"))}
                · {space_size}㎡
                · {staff_count} {safe(t("staff_unit"))}
            </div>

            <div class="brief-meta">

                <div>
                    <div class="label-small">
                        {safe(t("collab_type"))}
                    </div>
                    <div class="value-normal">
                        {safe(t("collab_values")[collab_type])}
                    </div>
                </div>

                <div>
                    <div class="label-small">
                        {safe(t("capacity"))}
                    </div>
                    <div class="value-normal">
                        {fmt_int(daily_capacity)}
                        {safe(t("visitors"))} / {safe(t("days_unit"))}
                    </div>
                </div>

                <div>
                    <div class="label-small">
                        {safe(t("products"))}
                    </div>
                    <div class="value-normal">
                        {safe(" · ".join(product_labels))}
                    </div>
                </div>

                <div>
                    <div class="label-small">
                        {safe(t("space_concept"))}
                    </div>
                    <div class="value-normal">
                        {safe(t("space_values")[space_concept])}
                    </div>
                </div>

                <div>
                    <div class="label-small">
                        {safe(t("characters"))}
                    </div>
                    <div class="value-normal">
                        {safe(" · ".join(character_labels))}
                    </div>
                </div>

                <div>
                    <div class="label-small">
                        {safe(t("budget"))}
                    </div>
                    <div class="value-normal">
                        {safe(fmt_currency(budget, LANG))}
                    </div>
                </div>

            </div>

            <div class="concept-box">
                {safe(concept_line)}
            </div>
        </div>
        """
    )


section_header("02", t("s2"), t("s2_copy"))


render_html(
    f"""
    <span class="data-chip">
        {safe(t("virtual_data"))}
    </span>

    <div style="
        color:#6C6A63;
        font-size:0.78rem;
        margin-bottom:0.9rem;
    ">
        {safe(t("virtual_desc"))}
    </div>
    """
)


data_1, data_2, data_3 = st.columns(3)


with data_1:
    sample_n = st.number_input(
        t("sample_n"),
        min_value=10,
        max_value=300,
        value=36,
        step=1,
        key="sample_n",
    )


with data_2:
    sample_mean = st.number_input(
        t("sample_mean"),
        min_value=0.0,
        max_value=10000.0,
        value=1800.0,
        step=50.0,
        format="%.0f",
        help=t("sample_mean_help"),
        key="sample_mean",
    )


with data_3:
    sigma = st.number_input(
        t("sigma"),
        min_value=1.0,
        max_value=5000.0,
        value=300.0,
        step=10.0,
        format="%.0f",
        help=t("sigma_help"),
        key="sigma",
    )


Z95 = 1.96

margin_error = Z95 * sigma / math.sqrt(sample_n)

ci_lower = sample_mean - margin_error
ci_upper = sample_mean + margin_error

period_lower = ci_lower * operating_days
period_upper = ci_upper * operating_days


section_header("03", t("s3"), t("s3_copy"))


render_html(
    f"""
    <div class="formula-card">
        <div class="label-small">
            {safe(t("formula_title"))}
        </div>

        <div class="formula">
            E = 1.96 × σ / √n
            <br>
            x̄ − E ≤ μ ≤ x̄ + E
        </div>
    </div>
    """
)


r1, r2, r3, r4 = st.columns(
    4,
    gap="small",
)


with r1:
    render_html(
        result_card(
            t("sample_mean_card"),
            f"{fmt_int(sample_mean)} {t('visitors')}",
        )
    )


with r2:
    render_html(
        result_card(
            t("moe"),
            f"±{fmt_int(margin_error)} {t('visitors')}",
        )
    )


with r3:
    render_html(
        result_card(
            t("ci"),
            f"{fmt_int(ci_lower)} – {fmt_int(ci_upper)}",
            t("visitors"),
        )
    )


with r4:
    render_html(
        result_card(
            t("period"),
            f"{fmt_int(period_lower)} – {fmt_int(period_upper)}",
            t("period_note"),
        )
    )


fig_ci = go.Figure()

fig_ci.add_trace(
    go.Scatter(
        x=[ci_lower, ci_upper],
        y=[0, 0],
        mode="lines+markers",
        line=dict(
            color="#1E1E1B",
            width=5,
        ),
        marker=dict(
            size=9,
            color="#84A9C8",
        ),
        hovertemplate="%{x:,.0f}<extra></extra>",
        showlegend=False,
    )
)

fig_ci.add_trace(
    go.Scatter(
        x=[sample_mean],
        y=[0],
        mode="markers+text",
        marker=dict(
            size=15,
            color="#D8B45B",
            line=dict(
                color="#1E1E1B",
                width=1,
            ),
        ),
        text=[t("mean")],
        textposition="top center",
        hovertemplate="%{x:,.0f}<extra></extra>",
        showlegend=False,
    )
)


chart_padding = max(
    (ci_upper - ci_lower) * 0.35,
    50,
)


fig_ci.update_layout(
    title=dict(
        text=t("ci_chart"),
        x=0,
        xanchor="left",
    ),
    height=240,
    margin=dict(
        l=20,
        r=20,
        t=55,
        b=30,
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#1E1E1B",
    ),
    xaxis=dict(
        range=[
            ci_lower - chart_padding,
            ci_upper + chart_padding,
        ],
        showgrid=False,
        zeroline=False,
        tickformat=",",
    ),
    yaxis=dict(
        visible=False,
        range=[-0.35, 0.45],
    ),
)


st.plotly_chart(
    fig_ci,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)


ci_col_1, ci_col_2, ci_col_3 = st.columns(3)


with ci_col_1:
    st.caption(
        f"{t('lower')}  {fmt_int(ci_lower)}"
    )


with ci_col_2:
    st.caption(
        f"{t('mean')}  {fmt_int(sample_mean)}"
    )


with ci_col_3:
    st.caption(
        f"{t('upper')}  {fmt_int(ci_upper)}"
    )


section_header("04", t("s4"), t("s4_copy"))


n_values = np.arange(10, 301)

error_values = Z95 * sigma / np.sqrt(n_values)


fig_error = go.Figure()

fig_error.add_trace(
    go.Scatter(
        x=n_values,
        y=error_values,
        mode="lines",
        line=dict(
            color="#1E1E1B",
            width=3,
        ),
        hovertemplate=(
            "n = %{x}<br>"
            "±%{y:.1f}"
            "<extra></extra>"
        ),
        showlegend=False,
    )
)


fig_error.add_trace(
    go.Scatter(
        x=[sample_n],
        y=[margin_error],
        mode="markers",
        marker=dict(
            size=13,
            color="#D8B45B",
            line=dict(
                color="#1E1E1B",
                width=1,
            ),
        ),
        hovertemplate=(
            f"{t('current_n')}: {sample_n}"
            f"<br>±{margin_error:.1f}"
            "<extra></extra>"
        ),
        showlegend=False,
    )
)


fig_error.update_layout(
    title=dict(
        text=t("sample_chart"),
        x=0,
        xanchor="left",
    ),
    height=360,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=45,
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#1E1E1B",
    ),
    xaxis=dict(
        title=t("sample_x"),
        gridcolor="#E4DED2",
        zeroline=False,
        range=[10, 300],
    ),
    yaxis=dict(
        title=t("error_y"),
        gridcolor="#E4DED2",
        zeroline=False,
    ),
)


st.plotly_chart(
    fig_error,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)


st.caption(t("sample_desc"))


render_html(
    f"""
    <div style="
        font-size:1rem;
        font-weight:730;
        margin:1.2rem 0 0.65rem 0;
    ">
        {safe(t("compare"))}
    </div>
    """
)


compare_sizes = [20, 50, 100, 200]

compare_cols = st.columns(4)


for column, n_compare in zip(
    compare_cols,
    compare_sizes,
):

    compare_error = Z95 * sigma / math.sqrt(n_compare)

    with column:
        render_html(
            f"""
            <div class="sample-card">
                <div class="sample-n">
                    n = {n_compare}
                </div>

                <div class="sample-error">
                    ±{fmt_int(compare_error)}
                    {safe(t("visitors"))}
                </div>
            </div>
            """
        )


section_header("05", t("s5"), t("s5_copy"))


if daily_capacity >= ci_upper:

    status_code = "safe"
    status_title = t("safe")
    status_copy = t("safe_copy")
    risk_text = t("risk_safe")
    recommendation = t("rec_safe")

elif daily_capacity >= ci_lower:

    status_code = "caution"
    status_title = t("caution")
    status_copy = t("caution_copy")
    risk_text = t("risk_caution")
    recommendation = t("rec_caution")

else:

    status_code = "adjust"
    status_title = t("adjust")
    status_copy = t("adjust_copy")
    risk_text = t("risk_adjust")
    recommendation = t("rec_adjust")


badge_class = {
    "safe": "badge-safe",
    "caution": "badge-caution",
    "adjust": "badge-adjust",
}[status_code]


status_left, status_right = st.columns(
    [0.9, 1.1],
    gap="large",
)


with status_left:

    render_html(
        f"""
        <div class="status-card">
            <span class="badge {badge_class}">
                {safe(status_title)}
            </span>

            <div class="status-number">
                {fmt_int(ci_lower)}
                –
                {fmt_int(ci_upper)}
                {safe(t("visitors"))}
            </div>

            <div class="status-copy">
                {safe(status_copy)}
            </div>

            <div style="
                margin-top:1rem;
                padding-top:0.9rem;
                border-top:1px solid #E8E3D8;
            ">
                <div class="label-small">
                    {safe(t("daily_capacity"))}
                </div>

                <div class="value-normal">
                    {fmt_int(daily_capacity)}
                    {safe(t("visitors"))}
                </div>
            </div>
        </div>
        """
    )


with status_right:

    render_html(
        f"""
        <div class="strategy-card">

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("risk"))}
                </div>
                <div class="strategy-value">
                    {safe(risk_text)}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("recommend"))}
                </div>
                <div class="strategy-value">
                    {safe(recommendation)}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("staff"))}
                </div>
                <div class="strategy-value">
                    {staff_count}
                    {safe(t("staff_unit"))}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("space_size"))}
                </div>
                <div class="strategy-value">
                    {space_size}㎡
                </div>
            </div>

        </div>
        """
    )


section_header("06", t("s6"), t("s6_copy"))


sample_left, sample_right = st.columns(
    [0.9, 1.1],
    gap="large",
)


with sample_left:

    target_error = st.number_input(
        t("target_error"),
        min_value=20.0,
        max_value=300.0,
        value=50.0,
        step=10.0,
        format="%.0f",
        key="target_error",
    )


required_n = math.ceil(
    (
        Z95
        * sigma
        / target_error
    ) ** 2
)


additional_needed = max(
    0,
    required_n - sample_n,
)


with sample_right:

    if additional_needed > 0:
        sample_sub = (
            f"{t('additional')} "
            f"{additional_needed} "
            f"{t('samples')}"
        )
    else:
        sample_sub = t("goal_met")

    required_sentence = (
        t("need_sentence").format(
            error=fmt_int(target_error),
            n=f"{required_n:,}",
        )
    )

    render_html(
        f"""
        <div class="status-card">

            <div class="label-small">
                {safe(t("min_sample"))}
            </div>

            <div style="
                font-size:2.5rem;
                font-weight:820;
                letter-spacing:-0.05em;
                margin:0.2rem 0 0.5rem 0;
            ">
                {required_n:,}
            </div>

            <div class="status-copy">
                {safe(required_sentence)}
            </div>

            <div style="
                margin-top:0.9rem;
                padding-top:0.8rem;
                border-top:1px solid #E8E3D8;
                font-weight:670;
            ">
                {safe(sample_sub)}
            </div>

        </div>
        """
    )


render_html(
    f"""
    <div class="formula-card">
        <div class="label-small">
            {safe(t("formula_title"))}
        </div>

        <div class="formula">
            n ≥ (1.96σ / E)²
        </div>
    </div>
    """
)


section_header("07", t("s7"), t("s7_copy"))


summary_left, summary_right = st.columns(
    2,
    gap="large",
)


with summary_left:

    render_html(
        f"""
        <div class="strategy-card">

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("project"))}
                </div>
                <div class="strategy-value">
                    {safe(popup_name)}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("location"))}
                </div>
                <div class="strategy-value">
                    {safe(popup_location)}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("operating_days"))}
                </div>
                <div class="strategy-value">
                    {operating_days}
                    {safe(t("days_unit"))}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("daily_demand"))}
                </div>
                <div class="strategy-value">
                    {fmt_int(ci_lower)}
                    –
                    {fmt_int(ci_upper)}
                    {safe(t("visitors"))}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("daily_capacity"))}
                </div>
                <div class="strategy-value">
                    {fmt_int(daily_capacity)}
                    {safe(t("visitors"))}
                </div>
            </div>

        </div>
        """
    )


with summary_right:

    if additional_needed > 0:
        sample_summary = (
            f"{t('additional')} "
            f"{additional_needed} "
            f"{t('samples')}"
        )
    else:
        sample_summary = t("goal_met")

    render_html(
        f"""
        <div class="strategy-card">

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("status"))}
                </div>
                <div class="strategy-value">
                    {safe(status_title)}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("precision"))}
                </div>
                <div class="strategy-value">
                    ±{fmt_int(margin_error)}
                    {safe(t("visitors"))}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("target_precision"))}
                </div>
                <div class="strategy-value">
                    ±{fmt_int(target_error)}
                    {safe(t("visitors"))}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("min_sample"))}
                </div>
                <div class="strategy-value">
                    {required_n:,}
                    ·
                    {safe(sample_summary)}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("risk"))}
                </div>
                <div class="strategy-value">
                    {safe(risk_text)}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("recommend"))}
                </div>
                <div class="strategy-value">
                    {safe(recommendation)}
                </div>
            </div>

        </div>
        """
    )


render_html(
    f"""
    <div class="dark-message">
        <div class="dark-message-main">
            {safe(t("core"))}
        </div>

        <div class="dark-message-sub">
            {safe(t("core_sub"))}
        </div>
    </div>
    """
)


st.write("")


with st.expander(
    t("warning")
):
    st.markdown(
        "\n".join(
            [
                f"- {t('w1')}",
                f"- {t('w2')}",
                f"- {t('w3')}",
                f"- {t('w4')}",
                f"- {t('w5')}",
                f"- {t('w6')}",
            ]
        )
    )
