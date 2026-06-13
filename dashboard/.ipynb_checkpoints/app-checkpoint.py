import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np

st.set_page_config(page_title="Kenya Debt Warning Signals", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600&family=Source+Sans+3:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap');

    html, body, [class*="css"] {
        font-family: 'Source Sans 3', sans-serif;
        background-color: #ffffff;
        color: #1a1a1a;
    }

    h1, h2, h3, h4 {
        font-family: 'Lora', serif;
        color: #1a1a1a;
        font-weight: 600;
    }

    .stApp {
        background-color: #ffffff;
    }

    section[data-testid="stSidebar"] {
        background-color: #f9f9f9;
        border-right: 1px solid #e0e0e0;
    }

    .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #c0392b;
        margin-bottom: 4px;
    }

    .section-divider {
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 36px 0;
    }

    .warning-box {
        background-color: #fffbf0;
        border-left: 3px solid #e6a817;
        padding: 12px 16px;
        margin: 14px 0;
        font-size: 13px;
        color: #7a5a00;
    }

    .danger-box {
        background-color: #fff5f5;
        border-left: 3px solid #c0392b;
        padding: 12px 16px;
        margin: 14px 0;
        font-size: 13px;
        color: #7a0000;
    }

    .finding-box {
        background-color: #f5fff5;
        border-left: 3px solid #27ae60;
        padding: 12px 16px;
        margin: 14px 0;
        font-size: 13px;
        color: #1a5a1a;
    }

    .timeline-card {
        border-left: 2px solid #c0392b;
        padding: 10px 16px;
        margin-bottom: 14px;
    }

    .timeline-period {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        letter-spacing: 2px;
        color: #c0392b;
        margin-bottom: 3px;
    }

    .timeline-title {
        font-family: 'Lora', serif;
        font-size: 14px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 5px;
    }

    .timeline-text {
        font-size: 13px;
        color: #555;
        line-height: 1.7;
    }

    p {
        color: #333;
        line-height: 1.8;
        font-size: 15px;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
        margin: 16px 0;
    }

    th {
        text-align: left;
        border-bottom: 2px solid #1a1a1a;
        padding: 8px 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #555;
    }

    td {
        padding: 8px 12px;
        border-bottom: 1px solid #e8e8e8;
        color: #333;
    }

    tr:last-child td {
        border-bottom: none;
    }
    </style>
""", unsafe_allow_html=True)

df = pd.read_csv("data/cleaned/kenya_debt.csv")

WHITE = "#ffffff"
TEXT = "#1a1a1a"
RED = "#c0392b"
AMBER = "#e6a817"
MUTED = "#999999"
GRID = "#e8e8e8"

with st.sidebar:
    st.markdown("### Kenya Debt Analysis")
    st.markdown("---")
    st.markdown("Loreen Atenge")
    st.markdown("Economics and Statistics")
    st.markdown("University of Nairobi")
    st.markdown("---")
    st.markdown("Data: World Bank WDI")
    st.markdown("Period: 1980 to 2024")
    st.markdown("---")
    year_range = st.slider("Filter by year", int(df["year"].min()), int(df["year"].max()), (1980, 2024))
    df_filtered = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])].copy()
    st.markdown("---")
    st.markdown("IMF Thresholds")
    st.markdown("External debt to GNI: 40%")
    st.markdown("Debt service to exports: 15%")
    st.markdown("---")
    st.markdown("These thresholds apply to market access countries. Kenya's classification has shifted over time, which affects how strictly these benchmarks apply.")

latest = df[df["year"] == df["year"].max()].iloc[0]
peak_debt = df["external_debt_gni"].max()
peak_year = int(df.loc[df["external_debt_gni"].idxmax(), "year"])
warning_year = int(df[df["debt_service_exports"] > 15]["year"].min())

st.markdown('<p class="eyebrow">Portfolio Project — Fiscal and Debt Analysis</p>', unsafe_allow_html=True)
st.markdown("# Were the Warning Signs Visible?")
st.markdown("#### Evidence from Kenya's debt sustainability indicators, 1980–2024")

st.markdown("""
Kenya's public debt has attracted significant attention in recent years. The current pressures —
a weakening shilling, rising debt service costs, and a new IMF programme in 2024 — did not
emerge overnight. They developed over years, shaped by a combination of deliberate borrowing
decisions, structural vulnerabilities, and external shocks including the COVID-19 pandemic and
the Russia-Ukraine war.

This project does not argue that Kenya's fiscal challenges were simply avoidable. External factors
played a real role, and the infrastructure investment that drove much of the borrowing had
legitimate development rationale. The question asked here is narrower: were the warning signs
visible in the data before the situation became critical, and if so, how early?

Using World Bank data from 1980 to 2024, this project tracks Kenya's performance against two
IMF debt sustainability thresholds and identifies when the indicators began signalling stress.
""")

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown('<p class="eyebrow">01 — Key Numbers</p>', unsafe_allow_html=True)

st.markdown(f"""
<table>
    <tr>
        <th>Indicator</th>
        <th>Value</th>
        <th>Note</th>
    </tr>
    <tr>
        <td>External debt to GNI (2024)</td>
        <td>{latest['external_debt_gni']:.1f}%</td>
        <td>Above the IMF threshold of 40%, crossed for the second time in 2023</td>
    </tr>
    <tr>
        <td>Peak external debt ({peak_year})</td>
        <td>{peak_debt:.1f}%</td>
        <td>Highest point reached, during the structural adjustment crisis</td>
    </tr>
    <tr>
        <td>Debt service to exports (2024)</td>
        <td>{latest['debt_service_exports']:.1f}%</td>
        <td>Kenya is spending over a quarter of export earnings on debt repayments</td>
    </tr>
    <tr>
        <td>First warning signal</td>
        <td>{warning_year}</td>
        <td>Debt service to exports crossed 15% threshold, five years before external debt did</td>
    </tr>
</table>
""", unsafe_allow_html=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown('<p class="eyebrow">02 — The Master Chart</p>', unsafe_allow_html=True)
st.markdown("### Kenya's full debt story in one chart")
st.markdown("""
The chart below shows Kenya's external debt as a percentage of GNI from 1980 to 2024.
The red dashed line marks the IMF sustainability threshold of 40%. Red shading shows years
when Kenya was above the threshold. Amber shading shows the warning zone where debt was
approaching but had not yet crossed it. Key events are annotated directly on the chart.
""")

events = {
    1993: "Structural\nadjustment peak",
    2000: "HIPC debt\nrelief begins",
    2014: "First\nEurobond",
    2020: "COVID\nborrowing spike",
}

fig, ax = plt.subplots(figsize=(13, 6))
fig.patch.set_facecolor(WHITE)
ax.set_facecolor(WHITE)

years = df_filtered["year"].values
debt = df_filtered["external_debt_gni"].values

ax.fill_between(years, 40, np.maximum(debt, 40),
                where=(debt >= 40),
                alpha=0.12, color=RED)

ax.fill_between(years, 30, np.minimum(debt, 40),
                where=((debt >= 30) & (debt < 40)),
                alpha=0.10, color=AMBER)

ax.axhline(y=40, color=RED, linestyle="--", linewidth=1.2)
ax.plot(years, debt, color=TEXT, linewidth=2, zorder=5)

for year, label in events.items():
    if year in list(years):
        idx = list(years).index(year)
        y_val = debt[idx]
        ax.annotate(label,
                    xy=(year, y_val),
                    xytext=(year, y_val + 16),
                    fontsize=7.5,
                    color="#666",
                    ha="center",
                    arrowprops=dict(arrowstyle="-", color="#bbb", lw=0.8))

danger_patch = mpatches.Patch(color=RED, alpha=0.2, label="Above IMF threshold (40%)")
warning_patch = mpatches.Patch(color=AMBER, alpha=0.2, label="Warning zone (30-40%)")
threshold_line = plt.Line2D([0], [0], color=RED, linestyle="--", label="IMF threshold (40%)")

ax.set_xlabel("Year", color=MUTED, fontsize=10)
ax.set_ylabel("External Debt (% of GNI)", color=MUTED, fontsize=10)
ax.tick_params(colors=MUTED)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color(GRID)
ax.spines["bottom"].set_color(GRID)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax.legend(handles=[danger_patch, warning_patch, threshold_line],
          facecolor=WHITE, edgecolor=GRID, labelcolor="#555", fontsize=9)
plt.tight_layout()
st.pyplot(fig)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown('<p class="eyebrow">03 — The Early Warning Signal</p>', unsafe_allow_html=True)
st.markdown("### Debt service to exports — the indicator that moved first")
st.markdown("""
While external debt to GNI only crossed the 40% threshold in 2023, a different indicator
was already signalling stress much earlier. Kenya's debt service to exports ratio crossed the
IMF warning threshold of 15% in 2018, five years before the external debt ratio breached its limit.

Between 2017 and 2019, this ratio jumped from 14.6% to 38.4% — an increase of 23.8 percentage
points in just two years. By 2019, Kenya was spending nearly 40 cents of every dollar earned
from exports on debt repayments. This deterioration coincided with the maturation of early
Eurobond obligations and rising commercial debt service costs.

External shocks — particularly COVID in 2020 and global commodity price increases from 2022 —
compounded the pressure. But the underlying stress in the debt service ratio was already visible
before those shocks arrived.
""")

st.markdown('<div class="warning-box">Debt service to exports crossed the 15% IMF threshold in 2018 — five years before external debt to GNI crossed its 40% limit in 2023.</div>', unsafe_allow_html=True)
st.markdown('<div class="danger-box">By 2019, debt service to exports had reached 38.4% — more than double the IMF threshold — driven largely by Eurobond repayments and SGR loan obligations.</div>', unsafe_allow_html=True)

fig2, ax2 = plt.subplots(figsize=(13, 5))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)

ax2.plot(df_filtered["year"], df_filtered["debt_service_exports"], color=TEXT, linewidth=2)
ax2.axhline(y=15, color=RED, linestyle="--", linewidth=1.2, label="IMF threshold (15%)")
ax2.fill_between(df_filtered["year"], df_filtered["debt_service_exports"], 15,
                 where=(df_filtered["debt_service_exports"] > 15),
                 alpha=0.12, color=RED, label="Above threshold")

ax2.annotate("Warning signal\n2018: 23.7%",
             xy=(2018, 23.7),
             xytext=(2015, 30),
             fontsize=8,
             color="#7a5a00",
             arrowprops=dict(arrowstyle="->", color=AMBER, lw=0.8))

ax2.annotate("Peak: 38.4%\n2019",
             xy=(2019, 38.4),
             xytext=(2016, 38),
             fontsize=8,
             color="#7a0000",
             arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))

ax2.set_xlabel("Year", color=MUTED, fontsize=10)
ax2.set_ylabel("Debt Service (% of Exports)", color=MUTED, fontsize=10)
ax2.tick_params(colors=MUTED)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_color(GRID)
ax2.spines["bottom"].set_color(GRID)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax2.legend(facecolor=WHITE, edgecolor=GRID, labelcolor="#555", fontsize=9)
plt.tight_layout()
st.pyplot(fig2)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown('<p class="eyebrow">04 — All Indicators Together</p>', unsafe_allow_html=True)
st.markdown("### A complete picture of Kenya's fiscal health")

fig3, axes = plt.subplots(3, 1, figsize=(13, 12))
fig3.patch.set_facecolor(WHITE)

indicator_configs = [
    ("external_debt_gni", "External Debt to GNI (%)", 40, "IMF threshold: 40%"),
    ("debt_service_exports", "Debt Service to Exports (%)", 15, "IMF threshold: 15%"),
    ("gdp_growth", "GDP Growth (%)", 0, "Zero growth line"),
]

for i, (col, label, threshold, threshold_label) in enumerate(indicator_configs):
    ax = axes[i]
    ax.set_facecolor(WHITE)
    valid = df_filtered[df_filtered[col].notna()]
    ax.plot(valid["year"], valid[col], color=TEXT, linewidth=1.8)
    ax.axhline(y=threshold, color=RED, linestyle="--", linewidth=1, label=threshold_label)
    ax.fill_between(valid["year"], valid[col], threshold,
                    where=(valid[col] > threshold),
                    alpha=0.1, color=RED)
    ax.set_title(label, color=TEXT, fontsize=10, fontweight="600", pad=8)
    ax.set_xlabel("Year", color=MUTED, fontsize=8)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.legend(facecolor=WHITE, edgecolor=GRID, labelcolor="#555", fontsize=8)

plt.tight_layout()
st.pyplot(fig3)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown('<p class="eyebrow">05 — Key Events Timeline</p>', unsafe_allow_html=True)
st.markdown("### What drove Kenya's debt at each stage")

timeline = [
    ("1980s", "Debt buildup begins", "Kenya borrowed heavily from multilateral creditors to fund development programmes and stabilize a struggling economy. External debt rose from 48% of GNI in 1980 to over 85% by 1990, well above the IMF threshold throughout the decade."),
    ("1993", "First crisis peak", "External debt reached 132% of GNI at the height of the structural adjustment period. The combination of heavy multilateral borrowing, a depreciating shilling, and the removal of price controls under IMF conditionality created severe fiscal stress."),
    ("Early 2000s", "HIPC debt relief", "Kenya benefited from the Heavily Indebted Poor Countries initiative, receiving significant debt cancellation from multilateral and bilateral creditors. External debt fell sharply through the 2000s, reaching 21% of GNI by 2013."),
    ("2014", "Shift to commercial borrowing", "Kenya issued its first sovereign Eurobond, raising USD 2 billion at commercial interest rates. This marked a structural shift away from concessional loans toward market-rate debt. The SGR railway loan from China added further commercial obligations."),
    ("2018", "Debt service warning signal", "Debt service to exports crossed the 15% IMF threshold for the first time since the early 2000s, reaching 23.7%. This was the earliest clear indicator of emerging stress, driven by maturing Eurobond obligations and rising commercial debt service costs."),
    ("2019", "Debt service peaks", "Debt service to exports reached 38.4% — more than double the threshold. The full weight of early Eurobond repayments and infrastructure loan servicing was now visible in the data."),
    ("2020", "COVID compounds pressure", "The pandemic caused a revenue shortfall and increased spending needs simultaneously. Kenya's GDP contracted for the first time in the dataset. Emergency borrowing from the IMF and World Bank added to the debt stock."),
    ("2023 to 2024", "External debt threshold crossed", "External debt to GNI crossed the 40% threshold in 2023, five years after the debt service warning signal first appeared. Kenya entered a new IMF programme in 2024 to address accumulated fiscal pressures."),
]

for period, title, description in timeline:
    st.markdown(f"""
    <div class="timeline-card">
        <div class="timeline-period">{period}</div>
        <div class="timeline-title">{title}</div>
        <div class="timeline-text">{description}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown('<p class="eyebrow">06 — Findings</p>', unsafe_allow_html=True)
st.markdown("### What the data tells us")
st.markdown("""
Kenya has experienced two distinct periods of debt stress since 1980. The first, running from
the early 1980s through to 2004, was driven primarily by multilateral borrowing and resolved
through HIPC debt relief. The second, currently unfolding, has a different character — rooted
in a deliberate shift toward commercial borrowing from 2014 onward, compounded by external shocks.

The data shows that warning signals were visible before the situation became critical. The debt
service to exports ratio crossed the IMF threshold in 2018, five years before external debt to
GNI did the same in 2023. Between 2017 and 2019, that ratio jumped by 23.8 percentage points
in just two years — a deterioration that was visible in publicly available data.

This does not mean the outcome was straightforwardly avoidable. The infrastructure investment
that drove much of the borrowing had genuine development rationale, and external shocks —
particularly COVID and the Russia-Ukraine war — accelerated the pressure in ways that were
difficult to anticipate. Political economy constraints also shape what governments can realistically
do with fiscal warning signals, even when those signals are clear.

What the data does suggest is that flow indicators like debt service to exports can provide
earlier and more actionable signals than stock indicators like debt to GNI. A country can
accumulate debt for years before the stock crosses a threshold, while the cost of servicing
that debt relative to export earnings may signal stress much sooner. For Kenya, that gap was
five years.

For policymakers and analysts monitoring debt sustainability in sub-Saharan Africa, this points
to the value of tracking multiple indicators simultaneously rather than relying on any single
threshold. The warning was there in the flow data, years before the stock data confirmed it.
""")

st.markdown('<div class="finding-box">Key finding: Debt service to exports signalled stress in 2018, five years before external debt to GNI crossed its IMF threshold in 2023. Flow indicators moved ahead of stock indicators.</div>', unsafe_allow_html=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown('<p class="eyebrow">Data: World Bank World Development Indicators | Analysis: Loreen Atenge, University of Nairobi</p>', unsafe_allow_html=True)
