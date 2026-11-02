import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Algeria Energy Transition Explorer", page_icon="⚡", layout="wide")
with (Path(__file__).parent / "data" / "export_scenarios.json").open(encoding="utf-8") as f:
    df = pd.DataFrame(json.load(f))

st.title("Algeria Energy Transition Explorer")
st.caption("An interactive presentation of the findings of *Powering EU?* (2025)")
st.info("Thesis reference results are kept separate from user-generated sensitivities. This prototype is not an EnergyPLAN replacement.")

page = st.sidebar.radio("Explore", ["Overview", "Export scenario comparison", "Scenario explorer", "Methodology"])

if page == "Overview":
    st.header("Research overview")
    st.write("The thesis examines alternative pathways for Algeria's energy system towards 2050 and compares electricity, green hydrogen and e-methane export options.")
    a,b,c = st.columns(3)
    a.metric("2050 final energy demand", "908.72 TWh/year")
    b.metric("Export pathways", "3")
    c.metric("Modelling tool", "EnergyPLAN 16.3")
    st.subheader("Five thesis scenarios")
    st.markdown("- Algeria 2019 baseline\n- 2050 domestic 100% renewable energy system\n- 2050 electricity export via HVDC\n- 2050 green hydrogen export\n- 2050 e-methane export")
    st.subheader("Dashboard structure")
    st.markdown("**Reference results:** published thesis findings.  \n**Interactive explorer:** selected sensitivities using clearly stated formulas.")

elif page == "Export scenario comparison":
    st.header("Export scenario comparison")
    view = df[["scenario","export_volume_TWh_year","market_price_EUR_MWh","annual_revenue_EUR_bn","reported_net_profit_EUR_bn","LCOX_EUR_MWh"]].copy()
    view.columns = ["Export pathway","Delivered exports (TWh/year)","Market price (€/MWh)","Revenue (€bn/year)","Reported net profit (€bn/year)","LCOX (€/MWh)"]
    st.dataframe(view, hide_index=True, use_container_width=True)
    x,y = st.columns(2)
    with x:
        st.plotly_chart(px.bar(df, x="scenario", y="annual_revenue_EUR_bn", title="Annual export revenue", labels={"scenario":"Pathway","annual_revenue_EUR_bn":"€bn/year"}), use_container_width=True)
    with y:
        st.plotly_chart(px.bar(df, x="scenario", y="LCOX_EUR_MWh", title="Levelised cost of export (LCOX)", labels={"scenario":"Pathway","LCOX_EUR_MWh":"€/MWh"}), use_container_width=True)
    with st.expander("How to interpret these indicators"):
        st.write("The thesis distinguishes the cost basis used for reported net profit from the incremental system cost used for LCOX. They are not interchangeable.")
        st.caption("The 2025 thesis is the authoritative source for published reference results.")

elif page == "Scenario explorer":
    st.header("Scenario explorer: financial sensitivity")
    st.write("Adjust market price and delivered export volume. The thesis cost assumption is held constant.")
    selected = st.selectbox("Select export pathway", df["scenario"].tolist())
    row = df.loc[df.scenario == selected].iloc[0]
    p = st.slider("Market price (€/MWh)", 10.0, 200.0, float(row.market_price_EUR_MWh), 0.5)
    v = st.slider("Delivered export volume (TWh/year)", 100, 1000, int(row.export_volume_TWh_year), 5)
    revenue = v * p / 1000
    cost = float(row.annual_export_cost_for_profit_EUR_bn)
    profit = revenue - cost
    a,b,c = st.columns(3)
    a.metric("Adjusted revenue", f"€{revenue:,.3f}bn/year", f"€{revenue-row.annual_revenue_EUR_bn:+.3f}bn vs thesis")
    b.metric("Fixed thesis cost assumption", f"€{cost:,.3f}bn/year")
    c.metric("Indicative net profit", f"€{profit:,.3f}bn/year", f"€{profit-row.reported_net_profit_EUR_bn:+.3f}bn vs thesis")
    st.warning("This is a financial sensitivity only: revenue = volume × price, and indicative profit = revenue − fixed thesis cost. It does not recalculate hourly generation, demand, storage, curtailment, transmission losses or system feasibility in EnergyPLAN. Changing export volume here does not prove that the system can physically deliver it.")

else:
    st.header("Methodology and source hierarchy")
    st.markdown("**Thesis modelling:** EnergyPLAN 16.3 hourly energy-system modelling; LUT-DEMAND for 2050 demand; PV profiles from PVGIS; technical, economic, social and environmental assessment.")
    st.markdown("**Source hierarchy:**\n1. The 2025 thesis is the primary source for published results.\n2. Updated supporting workbooks help interpret calculations where consistent.\n3. Older workbooks and earlier EnergyPLAN files are historical records.")
    st.write("Future modules can add infrastructure, renewable sites, technical system indicators and more advanced scenario calculations once their calculation methods are defined and validated.")

st.divider()
st.caption("Prototype — technical, infrastructure and renewable-site modules are planned next.")
