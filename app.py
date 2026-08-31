import math
import html

import numpy as np
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="팝업 전략 시뮬레이터",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
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
            padding-top: 2.2rem;
            padding-bottom: 5rem;
        }

        h1, h2, h3, h4, p, div, span, label {
            font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo",
                         "Noto Sans KR", "Segoe UI", sans-serif;
        }

        h1, h2, h3 {
            color: var(--ink);
            letter-spacing: -0.02em;
        }

        [data-testid="stHeader"] {
            background: rgba(244, 241, 234, 0.92);
        }

        .hero {
            border-top: 1px solid var(--ink);
            border-bottom: 1px solid var(--ink);
            padding: 2.2rem 0 1.9rem 0;
            margin: 0.2rem 0 2.2rem 0;
        }

        .hero-kicker {
            font-size: 0.78rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 0.7rem;
        }

        .hero-title {
            font-size: clamp(2.35rem, 5vw, 4.9rem);
            line-height: 0.96;
            font-weight: 800;
            letter-spacing: -0.055em;
            margin: 0;
            color: var(--ink);
        }

        .hero-sub {
            margin-top: 1rem;
            font-size: 1.02rem;
            line-height: 1.65;
            color: var(--muted);
            max-width: 760px;
        }

        .hero-note {
            margin-top: 1.1rem;
            font-size: 0.78rem;
            line-height: 1.55;
            color: #7E7A71;
        }

        .section-tag {
            font-size: 0.75rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 0.3rem;
        }

        .section-title {
            font-size: 2rem;
            font-weight: 760;
            letter-spacing: -0.035em;
            margin-bottom: 0.45rem;
        }

        .section-copy {
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.65;
            margin-bottom: 1.15rem;
            max-width: 860px;
        }

        .brief-card,
        .result-card,
        .strategy-card,
        .sample-card {
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 10px;
            box-shadow: none;
        }

        .brief-card {
            padding: 1.45rem 1.55rem;
            min-height: 100%;
        }

        .brief-overline {
            font-size: 0.72rem;
            color: var(--muted);
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
        }

        .brief-title {
            font-size: 1.65rem;
            line-height: 1.2;
            font-weight: 780;
            letter-spacing: -0.035em;
            margin-bottom: 0.35rem;
        }

        .brief-project {
            font-size: 0.93rem;
            color: var(--muted);
            margin-bottom: 1.2rem;
        }

        .brief-meta {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem 1rem;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--line);
        }

        .brief-label {
            font-size: 0.72rem;
            color: var(--muted);
            margin-bottom: 0.12rem;
        }

        .brief-value {
            font-size: 0.92rem;
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

        .result-card {
            padding: 1.05rem 1.1rem;
            min-height: 128px;
        }

        .result-label {
            font-size: 0.78rem;
            color: var(--muted);
            margin-bottom: 0.45rem;
        }

        .result-number {
            font-size: 1.75rem;
            line-height: 1.05;
            font-weight: 780;
            letter-spacing: -0.045em;
            color: var(--ink);
        }

        .result-note {
            font-size: 0.76rem;
            color: var(--muted);
            margin-top: 0.55rem;
            line-height: 1.45;
        }

        .status-wrap {
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 1.25rem 1.35rem;
        }

        .status-badge {
            display: inline-block;
            padding: 0.35rem 0.62rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 760;
            letter-spacing: 0.02em;
            margin-bottom: 0.85rem;
        }

        .status-safe {
            background: #E8EFE8;
            color: #45604A;
        }

        .status-caution {
            background: #F6EED9;
            color: #765D20;
        }

        .status-adjust {
            background: #F3E3E0;
            color: #7A4038;
        }

        .status-title {
            font-size: 1.45rem;
            font-weight: 780;
            letter-spacing: -0.03em;
            margin-bottom: 0.4rem;
        }

        .status-copy {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.6;
        }

        .strategy-card {
            padding: 1.15rem 1.25rem;
        }

        .strategy-row {
            padding: 0.72rem 0;
            border-bottom: 1px solid #E8E3D8;
        }

        .strategy-row:last-child {
            border-bottom: 0;
        }

        .strategy-key {
            font-size: 0.74rem;
            color: var(--muted);
            margin-bottom: 0.16rem;
        }

        .strategy-value {
            font-size: 1rem;
            font-weight: 670;
            line-height: 1.45;
        }

        .strategy-hero {
            background: #1F1F1C;
            color: #FFFDF6;
            border-radius: 10px;
            padding: 1.4rem 1.5rem;
            margin-top: 1rem;
        }

        .strategy-hero .big {
            font-size: 1.25rem;
            line-height: 1.55;
            font-weight: 730;
            letter-spacing: -0.025em;
        }

        .strategy-hero .small {
            margin-top: 0.55rem;
            color: #CFCBC2;
            font-size: 0.82rem;
            line-height: 1.5;
        }

        .formula-box {
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 1rem 1.15rem;
            margin: 0.6rem 0 1.1rem 0;
        }

        .tiny-note {
            font-size: 0.76rem;
            color: var(--muted);
            line-height: 1.55;
        }

        .data-label {
            display: inline-block;
            font-size: 0.74rem;
            border: 1px solid var(--line);
            padding: 0.3rem 0.55rem;
            border-radius: 999px;
            color: var(--muted);
            background: var(--paper);
            margin-bottom: 0.65rem;
        }

        .sample-card {
            padding: 0.85rem 0.9rem;
            text-align: left;
        }

        .sample-n {
            font-size: 0.75rem;
            color: var(--muted);
        }

        .sample-e {
            font-size: 1.25rem;
            margin-top: 0.18rem;
            font-weight: 760;
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
            border: 1px solid var(--ink);
            background: var(--paper);
            color: var(--ink);
            box-shadow: none;
        }

        .stButton > button:hover {
            border-color: var(--ink);
            color: var(--ink);
            background: #EEE9DE;
        }

        hr {
            border-color: var(--line) !important;
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
                font-size: 1.45rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
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
        "s4_copy": "표본 크기와 운영 조건을 바꾸며 추정의 정밀도와 운영 규모 변화를 비교",

        "s5": "운영 적정성 분석",
        "s5_copy": "추정된 평균 일 방문객 범위와 현재 일일 수용 가능 인원을 비교",

        "s6": "원하는 정확도에 필요한 표본",
        "s6_copy": "목표 오차범위를 정하면 그 정확도를 얻기 위해 필요한 최소 표본 수를 계산",

        "s7": "전략 요약",
        "s7_copy": "기획 정보와 통계 분석 결과를 하나의 브랜드 전략 요약으로 정리",

        "virtual_data": "교육용 가상 표본 데이터",
        "virtual_desc": "유사한 조건의 팝업스토어 데이터를 가정",

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
        "brief": "기획 요약",

        "days_unit": "일",
        "staff_unit": "명",
        "capacity_unit": "명 / 일",

        "budget_note": "기획 정보로만 표시 · 통계 계산에는 사용하지 않음",

        "sample_n": "표본 크기 n",
        "sample_mean": "표본평균 x̄",
        "sample_mean_help": "유사 팝업의 평균 일 방문객",
        "sigma": "모표준편차 σ",
        "sigma_help": "유사 팝업의 일 방문객 변동 정도",

        "sample_mean_card": "표본평균",
        "moe": "오차범위",
        "ci95": "95% 신뢰구간",
        "period_reference": "운영기간 환산",
        "period_note": "평균 일 방문객 신뢰구간을 운영일수에 맞게 단순 환산한 참고값 · 특정 날짜 또는 전체 방문객의 예측구간은 아님",

        "ci_chart": "95% 신뢰구간",
        "lower": "하한",
        "mean": "평균",
        "upper": "상한",

        "sample_vs_error": "표본 크기에 따른 오차범위 변화",
        "sample_x": "표본 크기 n",
        "error_y": "오차범위",
        "sample_interpret": "표본이 많아질수록 오차범위 감소 → 모평균을 더 정밀하게 추정",
        "compare_title": "표본 크기 비교",

        "status_safe": "운영 안정",
        "status_caution": "수용량 주의",
        "status_adjust": "운영 조정 필요",

        "status_safe_copy": "추정된 평균 방문 규모가 현재 수용 범위 안",
        "status_caution_copy": "예상 방문 규모의 일부가 현재 운영 범위를 초과",
        "status_adjust_copy": "추정된 평균 방문 규모가 현재 수용량보다 높음",

        "main_risk": "주요 위험",
        "risk_safe": "큰 수용량 위험 신호 없음",
        "risk_caution": "피크 시간 혼잡 가능성",
        "risk_adjust": "지속적인 수용량 부족 가능성",

        "recommend": "권장 조정",
        "rec_safe": "현재 운영 규모 유지 · 실제 운영 전 시간대별 수요 추가 확인",
        "rec_caution": "입장 시간 분산 · 대기 동선 확보 · 피크타임 추가 인력 검토",
        "rec_adjust": "수용 인원 확대 · 예약제 또는 회차제 검토 · 운영 동선 재설계",

        "target_error": "목표 오차범위",
        "min_sample": "필요 최소 표본",
        "more_needed": "추가 필요 표본",
        "goal_met": "현재 표본으로 목표 정확도 충족",
        "need_copy": "오차범위를 ±{e}명 이내로 줄이려면 최소 {n}개의 표본 필요",

        "project": "프로젝트",
        "operation_days": "운영 기간",
        "daily_demand": "예상 평균 일 방문 규모",
        "daily_capacity": "일일 수용 가능 인원",
        "operation_status": "운영 상태",
        "data_precision": "데이터 정확도",
        "target_precision": "목표 정확도",
        "needed_sample": "필요 최소 표본",
        "key_adjustment": "권장 조정",

        "core_message": "창의적인 팝업 기획을 통계적 추정을 통해 실제 실행 가능한 전략으로 연결",
        "core_sub": "Creative Direction × Brand Analytics × Statistical Estimation",

        "caution_title": "통계 해석 시 주의",
        "c1": "본 앱의 데이터는 교육용 가상 데이터",
        "c2": "모표준편차를 알고 있다고 가정",
        "c3": "신뢰구간은 평균 일 방문객에 대한 추정",
        "c4": "특정 하루 방문객의 예측구간과는 다름",
        "c5": "실제 팝업 운영에는 비용, 안전, 시간대별 방문 패턴 등 추가 정보 필요",
        "c6": "모집단이 정규분포를 따르거나 표본이 충분히 큰 상황을 가정",

        "formula_title": "사용 공식",
        "current_marker": "현재 n",

        "visitors": "명",
        "observations": "개",

        "project_type_values": {
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
        "hero_note": "A fictional collaboration simulator created for a school statistics project · Not officially affiliated with Stüssy, Toy Story, Disney/Pixar, or The Hyundai Seoul",

        "s1": "Pop-up Planning",
        "s1_copy": "Set the collaboration concept and operating conditions, then review the creative brief in one view",

        "s2": "Reference Data",
        "s2_copy": "Set sample information using fictional data from comparable pop-up operations",

        "s3": "Statistical Estimation",
        "s3_copy": "Calculate the 95% confidence interval and margin of error assuming the population standard deviation is known",

        "s4": "Operating Simulation",
        "s4_copy": "Change sample size and operating conditions to compare statistical precision and planned scale",

        "s5": "Capacity Review",
        "s5_copy": "Compare the estimated mean daily visitor range with planned daily capacity",

        "s6": "Required Sample Size",
        "s6_copy": "Choose a target margin of error and calculate the minimum sample size required",

        "s7": "Strategy Summary",
        "s7_copy": "Combine the creative brief and statistical analysis into one concise strategy view",

        "virtual_data": "Fictional educational sample data",
        "virtual_desc": "Assumed data from comparable pop-up operations",

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
        "brief": "Creative brief",

        "days_unit": "days",
        "staff_unit": "staff",
        "capacity_unit": "visitors / day",

        "budget_note": "Planning information only · Not used in statistical calculations",

        "sample_n": "Sample size n",
        "sample_mean": "Sample mean x̄",
        "sample_mean_help": "Average daily visitors from comparable pop-ups",
        "sigma": "Population standard deviation σ",
        "sigma_help": "Variation in daily visitors across comparable pop-ups",

        "sample_mean_card": "Sample mean",
        "moe": "Margin of error",
        "ci95": "95% confidence interval",
        "period_reference": "Operating-period reference",
        "period_note": "A simple multiplication of the mean daily visitor confidence interval by operating days · Not a prediction interval for a specific day or total attendance",

        "ci_chart": "95% Confidence Interval",
        "lower": "Lower",
        "mean": "Mean",
        "upper": "Upper",

        "sample_vs_error": "Sample Size vs Margin of Error",
        "sample_x": "Sample size n",
        "error_y": "Margin of error",
        "sample_interpret": "Larger sample → smaller margin of error → more precise estimation of the population mean",
        "compare_title": "Sample-size comparison",

        "status_safe": "Capacity Stable",
        "status_caution": "Capacity Caution",
        "status_adjust": "Adjustment Needed",

        "status_safe_copy": "Estimated mean visitor demand remains within current capacity",
        "status_caution_copy": "Part of the estimated mean visitor range exceeds current capacity",
        "status_adjust_copy": "Estimated mean visitor demand is above current capacity",

        "main_risk": "Main risk",
        "risk_safe": "No major capacity warning",
        "risk_caution": "Possible peak-time congestion",
        "risk_adjust": "Possible persistent capacity shortage",

        "recommend": "Recommended adjustment",
        "rec_safe": "Keep current scale · Check time-of-day demand before launch",
        "rec_caution": "Distribute entry times · Secure queue flow · Review peak-time staffing",
        "rec_adjust": "Increase capacity · Review reservation/session entry · Redesign operating flow",

        "target_error": "Target margin of error",
        "min_sample": "Minimum sample required",
        "more_needed": "Additional samples needed",
        "goal_met": "Current sample meets the target precision",
        "need_copy": "To keep the margin of error within ±{e} visitors, at least {n} observations are required",

        "project": "Project",
        "operation_days": "Operating days",
        "daily_demand": "Estimated mean daily visitors",
        "daily_capacity": "Daily capacity",
        "operation_status": "Operating status",
        "data_precision": "Data precision",
        "target_precision": "Target precision",
        "needed_sample": "Minimum sample required",
        "key_adjustment": "Recommended adjustment",

        "core_message": "Connecting creative pop-up planning with executable strategy through statistical estimation",
        "core_sub": "Creative Direction × Brand Analytics × Statistical Estimation",

        "caution_title": "Statistical interpretation notes",
        "c1": "All data in this app are fictional and for educational use",
        "c2": "The population standard deviation is assumed to be known",
        "c3": "The confidence interval estimates the mean daily visitor count",
        "c4": "It is not a prediction interval for a specific day",
        "c5": "Real pop-up operations also require cost, safety, and time-of-day demand data",
        "c6": "A normal population or a sufficiently large sample is assumed",

        "formula_title": "Formula",
        "current_marker": "Current n",

        "visitors": "visitors",
        "observations": "obs.",

        "project_type_values": {
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


_, language_column = st.columns([5.2, 1.3])

with language_column:
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


def safe(value):
    return html.escape(str(value))


def fmt_int(value):
    return f"{int(round(value)):,}"


def fmt_currency(value):
    if LANG == "ko":
        return f"{int(round(value)):,}원"
    return f"₩{int(round(value)):,}"


def section_header(number, title, copy):
    st.markdown(
        f"""
        <div style="margin-top:2.2rem;margin-bottom:0.9rem">
            <div class="section-tag">{safe(number)}</div>
            <div class="section-title">{safe(title)}</div>
            <div class="section-copy">{safe(copy)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def result_card(label, number, note=""):
    note_html = (
        f'<div class="result-note">{safe(음표)}</div>'
        if note
        else ""
    )

    return f"""
        <div class="result-card">
            <div class="result-label">{safe(label)}</div>
            <div class="result-number">{safe(number)}</div>
            {note_html}
        </div>
    """


st.markdown(
    f"""
    <div class="hero">
        <div class="hero-kicker">{safe(t("hero_kicker"))}</div>
        <div class="hero-title">{safe(t("hero_title"))}</div>
        <div class="hero-sub">{safe(t("hero_sub"))}</div>
        <div class="hero-note">{safe(t("hero_note"))}</div>
    </div>
    """,
    unsafe_allow_html=True,
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

    plan_col_1, plan_col_2 = st.columns(2)

    with plan_col_1:

        collab_type = st.selectbox(
            t("collab_type"),
            options=[
                "limited",
                "new",
                "film",
                "season",
            ],
            index=2,
            format_func=lambda value: t("project_type_values")[value],
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
            format_func=lambda value: t("character_values")[value],
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
            format_func=lambda value: t("product_values")[value],
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
            format_func=lambda value: t("space_values")[value],
            key="space_concept",
        )

    with plan_col_2:

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
            "스투시의 스트리트 감성으로 재해석한 한정 협업 공간"
        )

    concept_line = st.text_area(
        t("concept_line"),
        key="concept_line",
        height=90,
    )


with planning_right:

    character_labels = (
        [
            t("character_values")[value]
            for value in selected_characters
        ]
        if selected_characters
        else ["-"]
    )

    product_labels = (
        [
            t("product_values")[value]
            for value in selected_products
        ]
        if selected_products
        else ["-"]
    )

    st.markdown(
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

            <div style="font-size:0.95rem;font-weight:650">
                {safe(popup_location)}
            </div>

            <div style="font-size:0.9rem;color:#6C6A63;margin-top:0.3rem">
                {operating_days} {safe(t("days_unit"))}
                · {space_size}㎡
                · {staff_count} {safe(t("staff_unit"))}
            </div>

            <div class="brief-meta">

                <div>
                    <div class="brief-label">
                        {safe(t("collab_type"))}
                    </div>
                    <div class="brief-value">
                        {safe(t("project_type_values")[collab_type])}
                    </div>
                </div>

                <div>
                    <div class="brief-label">
                        {safe(t("capacity"))}
                    </div>
                    <div class="brief-value">
                        {fmt_int(daily_capacity)}
                        {safe(t("capacity_unit"))}
                    </div>
                </div>

                <div>
                    <div class="brief-label">
                        {safe(t("products"))}
                    </div>
                    <div class="brief-value">
                        {safe(" · ".join(product_labels))}
                    </div>
                </div>

                <div>
                    <div class="brief-label">
                        {safe(t("space_concept"))}
                    </div>
                    <div class="brief-value">
                        {safe(t("space_values")[space_concept])}
                    </div>
                </div>

                <div>
                    <div class="brief-label">
                        {safe(t("characters"))}
                    </div>
                    <div class="brief-value">
                        {safe(" · ".join(character_labels))}
                    </div>
                </div>

                <div>
                    <div class="brief-label">
                        {safe(t("budget"))}
                    </div>
                    <div class="brief-value">
                        {safe(fmt_currency(budget))}
                    </div>
                </div>

            </div>

            <div class="concept-box">
                {safe(concept_line)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


section_header("02", t("s2"), t("s2_copy"))


st.markdown(
    f"""
    <span class="data-label">
        {safe(t("virtual_data"))}
    </span>

    <div class="tiny-note" style="margin-bottom:0.9rem">
        {safe(t("virtual_desc"))}
    </div>
    """,
    unsafe_allow_html=True,
)


data_col_1, data_col_2, data_col_3 = st.columns(3)


with data_col_1:

    sample_n = st.number_input(
        t("sample_n"),
        min_value=10,
        max_value=300,
        value=36,
        step=1,
        key="sample_n",
    )


with data_col_2:

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


with data_col_3:

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


margin_error = (
    Z95
    * sigma
    / math.sqrt(sample_n)
)


ci_lower = (
    sample_mean
    - margin_error
)


ci_upper = (
    sample_mean
    + margin_error
)


period_lower = (
    ci_lower
    * operating_days
)


period_upper = (
    ci_upper
    * operating_days
)


section_header("03", t("s3"), t("s3_copy"))


st.markdown(
    f"""
    <div class="formula-box">

        <div style="
            font-size:0.78rem;
            color:#6C6A63;
            margin-bottom:0.45rem
        ">
            {safe(t("formula_title"))}
        </div>

        <div style="
            font-size:1.08rem;
            font-weight:650;
            line-height:1.8
        ">
            E = 1.96 × σ / √n
            <br>
            x̄ − E ≤ μ ≤ x̄ + E
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


result_1, result_2, result_3, result_4 = st.columns(
    4,
    gap="small",
)


with result_1:

    st.markdown(
        result_card(
            t("sample_mean_card"),
            f"{fmt_int(sample_mean)} {t('visitors')}",
        ),
        unsafe_allow_html=True,
    )


with result_2:

    st.markdown(
        result_card(
            t("moe"),
            f"±{fmt_int(margin_error)} {t('visitors')}",
        ),
        unsafe_allow_html=True,
    )


with result_3:

    st.markdown(
        result_card(
            t("ci95"),
            f"{fmt_int(ci_lower)} – {fmt_int(ci_upper)}",
            t("visitors"),
        ),
        unsafe_allow_html=True,
    )


with result_4:

    st.markdown(
        result_card(
            t("period_reference"),
            f"{fmt_int(period_lower)} – {fmt_int(period_upper)}",
            t("period_note"),
        ),
        unsafe_allow_html=True,
    )


st.write("")


fig_ci = go.Figure()


fig_ci.add_trace(
    go.Scatter(
        x=[
            ci_lower,
            ci_upper,
        ],
        y=[
            0,
            0,
        ],
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
        x=[
            sample_mean,
        ],
        y=[
            0,
        ],
        mode="markers+text",
        marker=dict(
            size=15,
            color="#D8B45B",
            line=dict(
                color="#1E1E1B",
                width=1,
            ),
        ),
        text=[
            t("mean"),
        ],
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
        title="",
        tickformat=",",
    ),
    yaxis=dict(
        visible=False,
        range=[
            -0.35,
            0.45,
        ],
    ),
)


st.plotly_chart(
    fig_ci,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)


ci_text_1, ci_text_2, ci_text_3 = st.columns(3)


with ci_text_1:
    st.caption(
        f"{t('lower')}  {fmt_int(ci_lower)}"
    )


with ci_text_2:
    st.caption(
        f"{t('mean')}  {fmt_int(sample_mean)}"
    )


with ci_text_3:
    st.caption(
        f"{t('upper')}  {fmt_int(ci_upper)}"
    )


section_header("04", t("s4"), t("s4_copy"))


n_values = np.arange(
    10,
    301,
)


error_values = (
    Z95
    * sigma
    / np.sqrt(n_values)
)


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
            "n = %{x}<br>±%{y:.1f}"
            "<extra></extra>"
        ),
        showlegend=False,
    )
)


fig_error.add_trace(
    go.Scatter(
        x=[
            sample_n,
        ],
        y=[
            margin_error,
        ],
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
            f"{t('current_marker')}: "
            f"{sample_n}<br>"
            f"±{margin_error:.1f}"
            "<extra></extra>"
        ),
        showlegend=False,
    )
)


fig_error.update_layout(
    title=dict(
        text=t("sample_vs_error"),
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
        range=[
            10,
            300,
        ],
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


st.caption(
    t("sample_interpret")
)


st.markdown(
    f"""
    <div style="
        font-weight:730;
        margin:1.3rem 0 0.65rem 0
    ">
        {safe(t("compare_title"))}
    </div>
    """,
    unsafe_allow_html=True,
)


compare_values = [
    20,
    50,
    100,
    200,
]


compare_columns = st.columns(4)


for column, compare_n in zip(
    compare_columns,
    compare_values,
):

    compare_error = (
        Z95
        * sigma
        / math.sqrt(compare_n)
    )

    with column:

        st.markdown(
            f"""
            <div class="sample-card">

                <div class="sample-n">
                    n = {compare_n}
                </div>

                <div class="sample-e">
                    ±{fmt_int(compare_error)}
                    {safe(t("visitors"))}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


section_header("05", t("s5"), t("s5_copy"))


if daily_capacity >= ci_upper:

    status_code = "safe"
    status_title = t("status_safe")
    status_copy = t("status_safe_copy")
    risk_text = t("risk_safe")
    recommendation = t("rec_safe")


elif daily_capacity >= ci_lower:

    status_code = "caution"
    status_title = t("status_caution")
    status_copy = t("status_caution_copy")
    risk_text = t("risk_caution")
    recommendation = t("rec_caution")


else:

    status_code = "adjust"
    status_title = t("status_adjust")
    status_copy = t("status_adjust_copy")
    risk_text = t("risk_adjust")
    recommendation = t("rec_adjust")


status_class = {
    "safe": "status-safe",
    "caution": "status-caution",
    "adjust": "status-adjust",
}[status_code]


status_left, status_right = st.columns(
    [0.85, 1.15],
    gap="large",
)


with status_left:

    st.markdown(
        f"""
        <div class="status-wrap">

            <span class="status-badge {status_class}">
                {safe(status_title)}
            </span>

            <div class="status-title">
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
                border-top:1px solid #E8E3D8
            ">

                <div class="brief-label">
                    {safe(t("daily_capacity"))}
                </div>

                <div class="brief-value">
                    {fmt_int(daily_capacity)}
                    {safe(t("visitors"))}
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with status_right:

    st.markdown(
        f"""
        <div class="strategy-card">

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("main_risk"))}
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
        """,
        unsafe_allow_html=True,
    )


section_header("06", t("s6"), t("s6_copy"))


required_left, required_right = st.columns(
    [0.9, 1.1],
    gap="large",
)


with required_left:

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


with required_right:

    if additional_needed > 0:

        required_subcopy = (
            f"{t('more_needed')} "
            f"{additional_needed} "
            f"{t('observations')}"
        )

    else:

        required_subcopy = (
            t("goal_met")
        )

    st.markdown(
        f"""
        <div class="status-wrap">

            <div class="brief-label">
                {safe(t("min_sample"))}
            </div>

            <div style="
                font-size:2.5rem;
                font-weight:820;
                letter-spacing:-0.05em;
                margin:0.2rem 0 0.5rem 0
            ">
                {required_n:,}
            </div>

            <div class="status-copy">
                {
                    safe(
                        t("need_copy").format(
                            e=fmt_int(target_error),
                            n=f"{required_n:,}",
                        )
                    )
                }
            </div>

            <div style="
                margin-top:0.9rem;
                padding-top:0.8rem;
                border-top:1px solid #E8E3D8;
                font-weight:670
            ">
                {safe(required_subcopy)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    f"""
    <div class="formula-box">

        <div style="
            font-size:0.78rem;
            color:#6C6A63;
            margin-bottom:0.45rem
        ">
            {safe(t("formula_title"))}
        </div>

        <div style="
            font-size:1.08rem;
            font-weight:650
        ">
            n ≥ (1.96σ / E)²
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


section_header("07", t("s7"), t("s7_copy"))


summary_left, summary_right = st.columns(
    2,
    gap="large",
)


with summary_left:

    st.markdown(
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
                    {safe(t("operation_days"))}
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
        """,
        unsafe_allow_html=True,
    )


with summary_right:

    if additional_needed > 0:

        additional_summary = (
            f"{t('more_needed')} "
            f"{additional_needed} "
            f"{t('observations')}"
        )

    else:

        additional_summary = (
            t("goal_met")
        )

    st.markdown(
        f"""
        <div class="strategy-card">

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("operation_status"))}
                </div>
                <div class="strategy-value">
                    {safe(status_title)}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("data_precision"))}
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
                    {safe(t("needed_sample"))}
                </div>
                <div class="strategy-value">
                    {required_n:,}
                    ·
                    {safe(additional_summary)}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("main_risk"))}
                </div>
                <div class="strategy-value">
                    {safe(risk_text)}
                </div>
            </div>

            <div class="strategy-row">
                <div class="strategy-key">
                    {safe(t("key_adjustment"))}
                </div>
                <div class="strategy-value">
                    {safe(recommendation)}
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    f"""
    <div class="strategy-hero">

        <div class="big">
            {safe(t("core_message"))}
        </div>

        <div class="small">
            {safe(t("core_sub"))}
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


st.write("")


with st.expander(
    t("caution_title")
):

    st.markdown(
        f"""
- {t("c1")}
- {t("c2")}
- {t("c3")}
- {t("c4")}
- {t("c5")}
- {t("c6")}
        """
    )
