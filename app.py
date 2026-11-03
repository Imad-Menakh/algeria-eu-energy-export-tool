import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Algeria Energy Transition Explorer", page_icon="⚡", layout="wide")
DATA = Path(__file__).parent / "data"

def load_data(name):
    with (DATA / name).open(encoding="utf-8") as f:
        return json.load(f)

exports = pd.DataFrame(load_data("export_scenarios.json"))
criteria = pd.DataFrame(load_data("siting_criteria.json"))
sites = pd.DataFrame(load_data("siting_sites.json"))

st.title("Algeria Energy Transition Explorer")
st.caption("An interactive presentation of the findings of *Powering EU?* (2025)")
st.info("The final thesis is the primary reference for published results. Interactive sensitivities are separate and do not replace EnergyPLAN modelling.")

pages = [
    "Research overview", "Four assessment dimensions", "Renewable energy siting",
    "Algeria's energy system", "Export scenario comparison", "Economic assessment",
    "Social assessment", "Environmental assessment", "Interactive scenario explorer",
    "Methodology and sources"
]
page = st.sidebar.radio("Research modules", pages)

if page == "Research overview":
    st.header("Research overview")
    st.write("The thesis examines Algeria's energy transition towards 2050, including a fully renewable domestic energy system and three export pathways to Europe: electricity via HVDC, green hydrogen and e-methane.")
    a,b,c = st.columns(3)
    a.metric("2050 final energy demand", "908.72 TWh/year")
    b.metric("Export pathways", "3")
    c.metric("Modelling tool", "EnergyPLAN 16.3")
    st.subheader("Four dimensions of assessment")
    cols = st.columns(4)
    dimensions = [
        ("Technical","System configuration, generation, storage, energy balances and infrastructure"),
        ("Economic","Investment, system costs, revenues, profitability and LCOX"),
        ("Social","Employment and socioeconomic implications"),
        ("Environmental","Land, water and environmental implications")
    ]
    for col,(name,desc) in zip(cols,dimensions):
        with col:
            st.markdown(f"**{name}**")
            st.caption(desc)
    st.subheader("Five thesis scenarios")
    st.markdown("- Algeria 2019 baseline\n- 2050 domestic 100% renewable energy system\n- 2050 electricity export via HVDC\n- 2050 green hydrogen export\n- 2050 e-methane export")

elif page == "Four assessment dimensions":
    st.header("Four dimensions of the energy transition")
    st.write("The thesis evaluates the transition through four complementary dimensions.")
    st.markdown("""
    **Technical feasibility** — energy-system configuration, renewable generation, storage, energy balances and export infrastructure.

    **Economic viability** — investment requirements, system costs, export revenues, profitability and LCOX.

    **Social implications** — employment creation and socioeconomic considerations.

    **Environmental implications** — land and water requirements and environmental considerations.
    """)
    st.caption("Detailed indicators and numerical results will be integrated from the corresponding thesis chapters and appendices.")

elif page == "Renewable energy siting":
    st.header("Renewable energy siting assessment")
    st.write("The thesis applies a two-step process: preliminary spatial filtering, followed by a multi-criteria suitability assessment (MCDA).")

    st.subheader("Step 1 — Preliminary spatial filtering")
    st.write("The thesis excludes mountainous and steep-slope areas, high-density urban zones, northern Algeria, small or isolated areas and protected regions. Four large candidate development zones were manually delineated.")

    st.subheader("Four candidate development zones")
    site_cols = st.columns(2)
    for i, site in sites.iterrows():
        with site_cols[i % 2]:
            st.markdown(f"### {site['site']} — {site['region']}")
            st.write(", ".join(site["provinces"]))
            st.metric("Original MCDA score", int(site["score"]), f"Rank {int(site['rank'])}")

    st.caption("The detailed province lists reproduce Appendix 2. The main-text description of Site 02 is shorter; the appendix list is shown here.")

    st.subheader("Step 2 — Multi-criteria suitability assessment")
    st.write("Fourteen indicators are assessed using Min–Max normalisation on a scale from 50 (least favourable) to 100 (most favourable). Reverse scoring is applied where lower values are preferred.")

    score_matrix = pd.DataFrame({"Criterion":criteria["criterion"],"Weight":criteria["weight"],"Scoring preference":criteria["direction"]})
    for i, site in sites.iterrows():
        score_matrix[site["site"]] = criteria["scores"].apply(lambda values: values[i])
    st.markdown("**Original criterion scores — Appendix 2, Table 2.2**")
    st.dataframe(score_matrix, hide_index=True, use_container_width=True)

    st.subheader("Original overall ranking")
    ranked = sites.sort_values("rank")
    fig = px.bar(ranked, x="site", y="score", text="score", title="Thesis-reported MCDA total scores",
                 labels={"site":"Candidate site","score":"Reported total score"})
    fig.update_traces(textposition="outside")
    fig.update_yaxes(range=[0,180])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Explore an individual criterion")
    selected = st.selectbox("Choose an indicator", criteria["criterion"].tolist())
    item = criteria.loc[criteria["criterion"] == selected].iloc[0]
    rows = [{"Candidate site":sites.iloc[i]["site"],"Reported raw value":item["raw"][i],"Reported score":item["scores"][i]} for i in range(len(sites))]
    st.write(f"**Weight:** {item['weight']:.2f}  |  **Scoring preference:** {item['direction']}")
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    st.subheader("Scoring equations")
    st.latex(r"Score(x)=50+\\left(\\frac{x-x_{min}}{x_{max}-x_{min}}\\right)\\times 50")
    st.latex(r"Score_{reverse}(x)=100-\\left(\\frac{x-x_{min}}{x_{max}-x_{min}}\\right)\\times 50")

    with st.expander("Methodological notes and limitations reported in Appendix 2"):
        st.markdown("""
        - Wind and solar data are attributed to DTU Wind Energy & World Bank Group (2025) and World Bank Group (2025).
        - Distances, except for roads, are estimated as straight-line (Euclidean) values and do not reflect topographical terrain.
        - Desalination, grid connection and HVDC export proximity were prioritised because of their role in hydrogen production and electricity exports.
        - For Site 01 and Site 04, gas-infrastructure values of −200 and −500 represent approximate distances to the nearest connection point because no pipelines cross those zones. For Sites 02 and 03, values represent existing gas-pipeline length within the site boundaries.
        - Road network coverage is based on the extent of major roads passing through the sites.
        - Electricity grid availability was qualitatively assessed from regional grid maps.
        - Unemployment and population density are based on 2019 provincial-level averages.
        - Environmental suitability is based on distance from protected or ecologically sensitive areas.
        """)
        st.warning("Appendix 2 Table 2.1 reports weights that sum to 2.00, not 1.00. The original weights and thesis-reported totals are preserved without normalisation. Some raw-value unit labels in the table appear misaligned or unclear, so ambiguous units are flagged rather than silently corrected.")

    st.success("Site 02 is the highest-ranked candidate in the thesis, with a reported score of 161 and rank 1.")
    st.info("This is the original thesis reference assessment. Interactive weight changes and alternative rankings are not enabled until the weighting and aggregation procedure has been independently checked.")

elif page == "Algeria's energy system":
    st.header("Algeria's energy system")
    st.metric("2050 final energy demand", "908.72 TWh/year")
    st.info("Detailed generation mix, installed capacities, storage and energy-balance results will be populated from the final thesis tables. Final energy demand must not be confused with total electricity generation.")

elif page == "Export scenario comparison":
    st.header("Export scenario comparison")
    view = exports[["scenario","export_volume_TWh_year","market_price_EUR_MWh","annual_revenue_EUR_bn","reported_net_profit_EUR_bn","LCOX_EUR_MWh"]].copy()
    view.columns = ["Export pathway","Delivered exports (TWh/year)","Market price (€/MWh)","Revenue (€bn/year)","Reported net profit (€bn/year)","LCOX (€/MWh)"]
    st.dataframe(view, hide_index=True, use_container_width=True)
    x,y = st.columns(2)
    with x:
        st.plotly_chart(px.bar(exports,x="scenario",y="annual_revenue_EUR_bn",title="Annual export revenue",labels={"scenario":"Pathway","annual_revenue_EUR_bn":"€bn/year"}),use_container_width=True)
    with y:
        st.plotly_chart(px.bar(exports,x="scenario",y="LCOX_EUR_MWh",title="Levelised cost of export (LCOX)",labels={"scenario":"Pathway","LCOX_EUR_MWh":"€/MWh"}),use_container_width=True)

elif page == "Economic assessment":
    st.header("Economic assessment")
    st.write("Published thesis reference values.")
    st.dataframe(exports[["scenario","annual_revenue_EUR_bn","annual_export_cost_for_profit_EUR_bn","reported_net_profit_EUR_bn","incremental_system_cost_for_LCOX_EUR_bn","LCOX_EUR_MWh"]].rename(columns={
        "scenario":"Export pathway","annual_revenue_EUR_bn":"Revenue (€bn/year)",
        "annual_export_cost_for_profit_EUR_bn":"Cost used for reported profit (€bn/year)",
        "reported_net_profit_EUR_bn":"Reported net profit (€bn/year)",
        "incremental_system_cost_for_LCOX_EUR_bn":"Incremental system cost for LCOX (€bn/year)",
        "LCOX_EUR_MWh":"LCOX (€/MWh)"
    }),hide_index=True,use_container_width=True)
    with st.expander("Why are there two cost figures?"):
        st.write("The thesis distinguishes the export cost used in the net-profit calculation from the incremental system cost used for LCOX. These are separate calculations and must not be treated as interchangeable.")
        st.write("Incremental export system cost = total export-scenario system cost − total domestic base-scenario system cost.")
        st.write("LCOX = incremental annual system cost ÷ net annual export energy delivered.")
        st.caption("The final thesis is the authoritative source for published results. Supporting workbooks help explain calculations and discrepancies; they do not silently overwrite thesis values.")

elif page == "Social assessment":
    st.header("Social assessment")
    st.info("Employment and socioeconomic findings will be integrated from the thesis's social-impact assessment. No unsupported estimates are introduced in this version.")

elif page == "Environmental assessment":
    st.header("Environmental assessment")
    st.info("Land, water and environmental findings will be integrated from the thesis's environmental assessment. No unsupported estimates are introduced in this version.")

elif page == "Interactive scenario explorer":
    st.header("Interactive scenario explorer — financial sensitivity")
    st.write("Adjust market price and delivered export volume while holding the thesis cost assumption constant.")
    chosen = st.selectbox("Select export pathway",exports["scenario"].tolist())
    row = exports.loc[exports["scenario"]==chosen].iloc[0]
    price = st.slider("Market price (€/MWh)",10.0,200.0,float(row["market_price_EUR_MWh"]),0.5)
    volume = st.slider("Delivered export volume (TWh/year)",100,1000,int(row["export_volume_TWh_year"]),5)
    revenue = volume*price/1000
    cost = float(row["annual_export_cost_for_profit_EUR_bn"])
    profit = revenue-cost
    a,b,c = st.columns(3)
    a.metric("Adjusted revenue",f"€{revenue:,.3f}bn/year")
    b.metric("Fixed thesis cost assumption",f"€{cost:,.3f}bn/year")
    c.metric("Indicative net profit",f"€{profit:,.3f}bn/year")
    st.warning("Financial sensitivity only. This does not rerun EnergyPLAN or recalculate hourly generation, demand, storage, curtailment, transmission losses or physical system feasibility. Changing export volume does not demonstrate that the energy system can deliver it.")

else:
    st.header("Methodology and sources")
    st.markdown("""
    **Modelling approach:** EnergyPLAN 16.3 hourly energy-system modelling; LUT-DEMAND for 2050 demand; PV profiles from PVGIS; technical, economic, social and environmental assessment.

    **Source hierarchy:**
    1. Final 2025 master's thesis — primary reference for published results.
    2. Updated supporting Excel workbooks — detailed calculations and inputs where consistent with the thesis.
    3. Earlier workbooks and EnergyPLAN scenario files — historical development records.

    Discrepancies are documented. Supporting workbooks do not silently overwrite thesis reference values.
    """)
    st.write("For the siting assessment, the principal reference is Appendix 2, including Tables 2.1 and 2.2 and Figure 2.1.")

st.divider()
st.caption("Reference: Imadeddine Menakh (2025), *Powering EU? – Energy scenarios for exporting electricity, green hydrogen and e-methane from Algeria to Europe*.")
