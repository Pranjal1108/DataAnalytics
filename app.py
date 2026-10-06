"""Airport Data Insights. Launch: streamlit run app.py."""
from html import escape
import pandas as pd
import plotly.express as px
import streamlit as st
from data import FACILITIES, load_data

COLORS = ["#38bdf8", "#2dd4bf", "#a3e635", "#c4b5fd"]

def chart(df, metric, title, unit, line=False):
    kwargs = dict(data_frame=df, x="Phase", y=metric, title=title,
                  labels={metric: unit}, hover_data=["Year_Range"], color_discrete_sequence=COLORS)
    fig = px.line(**kwargs, markers=True) if line else px.bar(**kwargs, color="Phase", text_auto=".3s")
    fig.update_layout(height=350, showlegend=False, margin=dict(l=10,r=10,t=55,b=10),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#cbd5e1"), title_font_size=18)
    fig.update_xaxes(title=None, showgrid=False)
    fig.update_yaxes(rangemode="tozero", gridcolor="#243247")
    return fig

def main():
    st.set_page_config(page_title="Airport Data Insights", page_icon="✈", layout="wide")
    st.markdown("""<style>
    .stApp {background:#0b1220;color:#e2e8f0}
    .block-container {max-width:1320px;padding-top:2.4rem}
    h1 {letter-spacing:-1.5px} h2 {letter-spacing:-.5px}
    .eyebrow {color:#38bdf8;font-size:12px;letter-spacing:3px;font-weight:700}
    .facility {display:flex;align-items:center;gap:14px;padding:18px;background:#142033;border:1px solid #26364d;border-radius:12px;margin:10px 0}
    .facility img {width:30px;height:30px} .facility span {font-size:15px}
    </style>""", unsafe_allow_html=True)
    try:
        df = load_data()
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        st.error(f"Unable to load planning data: {exc}")
        st.stop()
    with st.sidebar:
        st.title("✈ Airport Insights")
        st.caption("NOIDA INTERNATIONAL AIRPORT")
        selected = st.multiselect("Compare construction phases", df.Phase.tolist(), default=df.Phase.tolist())
        st.divider()
        st.caption("MPPA = million passengers per annum. Costs: ₹ crore. Areas: square metres or hectares.")
        st.caption("Historical educational snapshot. Figures are not verified current airport facts.")
    st.markdown('<div class="eyebrow">INFRASTRUCTURE / PLANNING INTELLIGENCE</div>', unsafe_allow_html=True)
    st.title("Airport Data Insights")
    st.write("Explore how Noida’s airport development plan scales across four construction phases.")
    st.info("Historical planning snapshot • The original data has no dated source citations. Estimates, schedules, facility assignments and status labels are unverified and do not describe live operations.")
    if not selected:
        st.warning("Choose at least one phase in the sidebar to explore the dataset.")
        return
    filtered = df[df.Phase.isin(selected)]
    latest = filtered.iloc[-1]
    a,b,c = st.columns(3)
    a.metric("Highest selected capacity target", f'{latest.Passenger_Capacity_MPPA:g} MPPA')
    b.metric("Selected phase estimates combined", f'₹{filtered.Estimated_Cost_Cr.sum():,.0f} cr', help="Arithmetic sum of inherited estimates; accounting basis is unverified.")
    c.metric("Selected phases", len(filtered))
    overview, facilities, dataset = st.tabs(["Development overview", "Facilities by phase", "Data & methodology"])
    with overview:
        left,right = st.columns(2)
        left.plotly_chart(chart(filtered, "Passenger_Capacity_MPPA", "Capacity scales with each phase", "Cumulative capacity (MPPA)", True), width="stretch")
        right.plotly_chart(chart(filtered, "Estimated_Cost_Cr", "Estimated investment by phase", "Estimated cost (₹ crore)"), width="stretch")
        st.subheader("What the snapshot suggests")
        st.write(f'Across the full dataset, annual capacity targets rise from {df.Passenger_Capacity_MPPA.iloc[0]:g} to {df.Passenger_Capacity_MPPA.iloc[-1]:g} MPPA — {df.Passenger_Capacity_MPPA.iloc[-1] / df.Passenger_Capacity_MPPA.iloc[0]:.1f}× the initial target.')
        st.caption("Successive capacity targets are cumulative. They should not be summed or shown as slices of a total.")
        left,right = st.columns(2)
        left.plotly_chart(chart(filtered, "Additional_Capacity_MPPA", "Added capacity at each phase", "Increment from previous phase (MPPA)"), width="stretch")
        right.plotly_chart(chart(filtered, "Cargo_Area_sqm", "Cargo footprint expansion", "Cargo area (m²)"), width="stretch")
        st.caption("Added capacity uses the previous phase in the complete dataset, even when that phase is filtered out.")
        st.subheader("Development milestones")
        for _, row in filtered.iterrows():
            st.write(f'**{row.Phase} · {row.Year_Range}** — {row.Passenger_Capacity_MPPA:g} MPPA target · Recorded status: {row.Status}')
    with facilities:
        phase = st.selectbox("Explore a phase", filtered.Phase.tolist())
        st.caption("Original demonstration facility assignments. Icons load online; text remains readable without internet.")
        cols = st.columns(2)
        for i, (name, icon) in enumerate(FACILITIES[phase]):
            cols[i % 2].markdown(f'<div class="facility"><img src="https://api.iconify.design/lucide/{icon}.svg?color=%2338bdf8" alt="" loading="lazy"><span>{escape(name)}</span></div>', unsafe_allow_html=True)
        st.caption("Icons: Lucide via Iconify. Attribution in THIRD_PARTY_NOTICES.md.")
    with dataset:
        st.subheader("One dataset, explicit assumptions")
        st.dataframe(filtered, hide_index=True, width="stretch")
        st.download_button("Download selected phases · CSV", filtered.to_csv(index=False).encode("utf-8-sig"), "airport_selected_phases.csv", "text/csv")
        st.markdown("""- Every entry point reads the repository CSV. Launching the app never rewrites it.
- Original zeroes for later runway counts and land areas meant “not provided”; they are now missing values.
- Conflicting embedded datasets have been removed. Other CSV values are preserved.
- Costs, areas, years and status labels remain unverified historical estimates.
- Added capacity is the difference between successive cumulative targets.
- The raw workbook is a retained historical artifact, not a dashboard input.""")

if __name__ == "__main__":
    main()

