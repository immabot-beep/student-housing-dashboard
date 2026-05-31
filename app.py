# =============================================================================
# app.py
# Student Housing Market Research & Pricing Dashboard
#
# Run with:  streamlit run app.py
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import our custom analysis functions from src/analysis.py
from src.analysis import run_full_analysis

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# Must be the very first Streamlit command called.
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Housing Market Dashboard",
    page_icon="🏘️",
    layout="wide",
)

# -----------------------------------------------------------------------------
# LOAD & PROCESS DATA
# @st.cache_data tells Streamlit to cache (remember) the result so the
# analysis doesn't re-run every time the user interacts with the dashboard.
# -----------------------------------------------------------------------------
@st.cache_data
def get_data() -> pd.DataFrame:
    """Load and process data, cached for performance."""
    return run_full_analysis("data/student_housing_market.csv")

df = get_data()

# -----------------------------------------------------------------------------
# SIDEBAR — City Selector
# -----------------------------------------------------------------------------
st.sidebar.title("🏘️ Dashboard Controls")
st.sidebar.markdown("Use the selector below to explore a specific market.")

# Build a list of cities sorted by rank for the dropdown
city_options = df["city"].tolist()   # already sorted best → worst
selected_city = st.sidebar.selectbox("Select a City", city_options)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**About this tool**\n\n"
    "This dashboard analyses student housing supply-demand dynamics "
    "across 10 major US university cities to support real estate "
    "investment research and pricing decisions."
)

# Filter the DataFrame to the selected city (returns a single-row DataFrame)
city_row = df[df["city"] == selected_city].iloc[0]

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.title("🏘️ Student Housing Market Research & Pricing Dashboard")
st.markdown(
    "Explore supply-demand dynamics, affordability metrics, and investment "
    "attractiveness scores across major US university markets."
)
st.markdown("---")

# -----------------------------------------------------------------------------
# SECTION 1 — City Spotlight (Key Metrics)
# -----------------------------------------------------------------------------
st.subheader(f"📍 City Spotlight: {selected_city}, {city_row['state']}")
st.caption(f"Home of **{city_row['major_university']}**")

# Display six KPI cards in a row using Streamlit columns
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric(
    label="Avg Monthly Rent",
    value=f"${city_row['average_monthly_rent']:,.0f}",
)
col2.metric(
    label="Occupancy Rate",
    value=f"{city_row['occupancy_rate']*100:.1f}%",
)
col3.metric(
    label="Annual Rent Growth",
    value=f"{city_row['annual_rent_growth']*100:.1f}%",
)
col4.metric(
    label="Demand-Supply Ratio",
    value=f"{city_row['demand_supply_ratio']:.2f}x",
    help="Student population ÷ available beds. >1 means undersupply.",
)
col5.metric(
    label="Affordability Ratio",
    value=f"{city_row['affordability_ratio']:.2f}",
    help="Annual rent ÷ median household income.",
)
col6.metric(
    label="Investment Score",
    value=f"{city_row['investment_score']:.1f} / 100",
    help="Composite score based on rent growth, occupancy, demand, and yield.",
)

st.markdown("---")

# -----------------------------------------------------------------------------
# SECTION 2 — Charts (three columns)
# -----------------------------------------------------------------------------
st.subheader("📊 Market Charts")

chart_col1, chart_col2, chart_col3 = st.columns(3)

# ── Chart 1: Investment Score by City (horizontal bar chart) ─────────────────
with chart_col1:
    st.markdown("**Investment Attractiveness Score by City**")

    # Highlight the selected city in a different colour
    bar_colors = [
        "#2563eb" if city == selected_city else "#93c5fd"
        for city in df["city"]
    ]

    fig_bar = go.Figure(
        go.Bar(
            x=df["investment_score"],
            y=df["city"],
            orientation="h",             # horizontal bars
            marker_color=bar_colors,
            text=df["investment_score"],
            textposition="outside",
        )
    )
    fig_bar.update_layout(
        xaxis_title="Score (0–100)",
        yaxis=dict(autorange="reversed"),  # highest score at the top
        height=380,
        margin=dict(l=10, r=10, t=10, b=30),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Chart 2: Average Rent vs Student Population (scatter) ────────────────────
with chart_col2:
    st.markdown("**Avg Monthly Rent vs Student Population**")

    fig_scatter = px.scatter(
        df,
        x="student_population",
        y="average_monthly_rent",
        text="city",
        size="investment_score",          # bubble size = investment score
        color="investment_score",
        color_continuous_scale="Blues",
        labels={
            "student_population": "Student Population",
            "average_monthly_rent": "Avg Monthly Rent ($)",
        },
    )
    fig_scatter.update_traces(textposition="top center", textfont_size=10)
    fig_scatter.update_layout(
        height=380,
        margin=dict(l=10, r=10, t=10, b=30),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ── Chart 3: Demand-Supply Ratio by City ─────────────────────────────────────
with chart_col3:
    st.markdown("**Demand-Supply Ratio by City**")

    # Sort by ratio for this chart so it's easy to read
    df_sorted = df.sort_values("demand_supply_ratio", ascending=True)

    demand_colors = [
        "#2563eb" if city == selected_city else "#93c5fd"
        for city in df_sorted["city"]
    ]

    fig_demand = go.Figure(
        go.Bar(
            x=df_sorted["demand_supply_ratio"],
            y=df_sorted["city"],
            orientation="h",
            marker_color=demand_colors,
            text=df_sorted["demand_supply_ratio"],
            textposition="outside",
        )
    )
    # Add a vertical reference line at 1.0 (equilibrium)
    fig_demand.add_vline(
        x=1.0,
        line_dash="dash",
        line_color="red",
        annotation_text="Equilibrium (1.0)",
        annotation_position="top right",
    )
    fig_demand.update_layout(
        xaxis_title="Ratio (students per bed)",
        height=380,
        margin=dict(l=10, r=10, t=10, b=30),
    )
    st.plotly_chart(fig_demand, use_container_width=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# SECTION 3 — Full Rankings Table
# -----------------------------------------------------------------------------
st.subheader("🏆 Full Market Rankings")
st.markdown(
    "All 10 cities ranked from most to least attractive for student housing investment. "
    "Click a column header to sort."
)

# Choose which columns to display and give them friendly names
display_cols = {
    "rank": "Rank",
    "city": "City",
    "state": "State",
    "major_university": "University",
    "student_population": "Students",
    "average_monthly_rent": "Avg Rent ($)",
    "occupancy_rate": "Occupancy",
    "annual_rent_growth": "Rent Growth",
    "demand_supply_ratio": "Demand/Supply",
    "affordability_ratio": "Affordability",
    "investment_score": "Score",
}

table_df = df[list(display_cols.keys())].rename(columns=display_cols).copy()

# Format columns for readability
table_df["Occupancy"]    = table_df["Occupancy"].apply(lambda x: f"{x*100:.1f}%")
table_df["Rent Growth"]  = table_df["Rent Growth"].apply(lambda x: f"{x*100:.1f}%")
table_df["Avg Rent ($)"] = table_df["Avg Rent ($)"].apply(lambda x: f"${x:,.0f}")
table_df["Students"]     = table_df["Students"].apply(lambda x: f"{x:,}")

# Highlight the selected city row
def highlight_selected(row):
    """Return a list of CSS styles — blue background for the selected city."""
    if row["City"] == selected_city:
        return ["background-color: #dbeafe"] * len(row)
    return [""] * len(row)

styled_table = table_df.style.apply(highlight_selected, axis=1)
st.dataframe(styled_table, use_container_width=True, hide_index=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# SECTION 4 — Methodology Note
# -----------------------------------------------------------------------------
with st.expander("📖 Methodology & Metric Definitions"):
    st.markdown("""
    | Metric | Formula | Interpretation |
    |---|---|---|
    | **Demand-Supply Ratio** | Student Population ÷ Available Beds | >1 = undersupply (favours investors) |
    | **Affordability Ratio** | (Monthly Rent × 12) ÷ Median HH Income | Lower = more affordable for renters |
    | **Investment Score** | Average of 4 normalized sub-scores (0–100) | Higher = more attractive market |

    **Investment Score Components (equal weight, 25% each):**
    1. **Rent Growth** — higher annual rent growth scores higher
    2. **Occupancy Rate** — higher occupancy scores higher
    3. **Demand-Supply Ratio** — higher undersupply scores higher
    4. **Gross Yield Proxy** — Annual Rent ÷ Property Price; higher yield scores higher

    Each component is min-max normalized to a 0–1 range before averaging.

    > ⚠️ *Data is illustrative and for portfolio/learning purposes only.
    > Always validate with primary market sources before making investment decisions.*
    """)

# Footer
st.caption("Built with Python · Streamlit · Plotly | Student Housing Market Research Dashboard")
