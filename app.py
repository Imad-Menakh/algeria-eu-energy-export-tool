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
    "Algeria's energy system", "Technical assessment", "Export scenario comparison", "Economic assessment",
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
    st.info("The technical assessment provides the scenario-level generation, capacity and storage data. Final energy demand (908.72 TWh/year) is a different indicator from total electricity generation, because the model includes conversion processes, storage and export flows.")


elif page == "Technical assessment":
    st.header("Technical assessment")
    st.write("This module presents the EnergyPLAN reference configurations and the technical infrastructure described in the thesis.")
    tech = load_data("technical_results.json")
    tech_df = pd.DataFrame(tech["scenarios"])
    selected = st.selectbox("Select a scenario", tech_df["name"].tolist())
    row = tech_df.loc[tech_df["name"] == selected].iloc[0]
    a,b,c = st.columns(3)
    a.metric("Onshore wind capacity", f"{row['wind_MW']:,.0f} MW")
    b.metric("Solar PV capacity", f"{row['pv_MW']:,.0f} MW")
    c.metric("Electrolyser capacity", f"{row['electrolyser_MW']:,.0f} MW")
    st.subheader("Scenario configuration")
    st.dataframe(tech_df.rename(columns={
        "name":"Scenario","wind_MW":"Wind capacity (MW)","pv_MW":"PV capacity (MW)",
        "wind_TWh":"Wind generation (TWh)","pv_TWh":"PV generation (TWh)",
        "electrolyser_MW":"Electrolysers (MW)","battery_GWh":"Battery storage (GWh)",
        "hydrogen_GWh":"Hydrogen storage (GWh)","gas_GWh":"Gas storage (GWh)",
        "co2_tph":"CO₂ capture (tonnes/hour)","export":"Export target"
    }), hide_index=True, use_container_width=True)
    st.subheader("Installed wind and solar capacity")
    cap = tech_df.melt(id_vars="name",value_vars=["wind_MW","pv_MW"],var_name="Technology",value_name="Capacity (MW)")
    cap["Technology"] = cap["Technology"].map({"wind_MW":"Onshore wind","pv_MW":"Solar PV"})
    st.plotly_chart(px.bar(cap,x="name",y="Capacity (MW)",color="Technology",barmode="group",title="Installed generation capacity"),use_container_width=True)
    st.subheader("Annual wind and solar generation")
    gen = tech_df.melt(id_vars="name",value_vars=["wind_TWh","pv_TWh"],var_name="Technology",value_name="Generation (TWh/year)")
    gen["Technology"] = gen["Technology"].map({"wind_TWh":"Onshore wind","pv_TWh":"Solar PV"})
    st.plotly_chart(px.bar(gen,x="name",y="Generation (TWh/year)",color="Technology",barmode="group",title="Wind and PV generation"),use_container_width=True)
    st.subheader("Storage requirements")
    st.dataframe(tech_df[["name","battery_GWh","hydrogen_GWh","gas_GWh"]].rename(columns={"name":"Scenario","battery_GWh":"Battery (GWh)","hydrogen_GWh":"Hydrogen (GWh)","gas_GWh":"Gas (GWh)"}),hide_index=True,use_container_width=True)
    st.subheader("Electricity consumption indicators")
    st.dataframe(pd.DataFrame(tech["electricity_use"]),hide_index=True,use_container_width=True)
    st.metric("Critical excess electricity production — electricity export",f"{tech['notes']['electricity_export_CEEP_TWh']} TWh/year")
    st.write(f"The electricity export case models {tech['notes']['electricity_export_input_TWh']} TWh/year entering the export chain. The thesis assumes {tech['notes']['electricity_export_losses_TWh']} TWh of losses, leaving {tech['notes']['electricity_export_net_TWh']} TWh/year delivered. Flexible demand is estimated at {tech['notes']['flexible_demand_TWh']} TWh/year.")
    with st.expander("Electricity HVDC routes — thesis Tables 15–16"):
        st.dataframe(pd.DataFrame(tech["hvdc"]),hide_index=True,use_container_width=True)
    with st.expander("Hydrogen pipeline routes — thesis Table 18"):
        st.dataframe(pd.DataFrame(tech["hydrogen_routes"]),hide_index=True,use_container_width=True)
    with st.expander("Important thesis data notes and generation discrepancies"):
        st.markdown("**Domestic 2050 base scenario**")
        st.write("Thesis Table 9 reports 2,134.33 TWh/year of total electricity generation. This corresponds to the wind and PV figures plus the small hydro, geothermal and waste contributions shown in the supporting results. The later thesis narrative reports 2,177.83 TWh/year. The supporting workbook gives approximately 2,173.20 TWh/year when the 38.88 TWh/year condensing contribution is also included. These figures therefore have different scopes or versions; the dashboard retains the published Table 9 value as the thesis table reference and reports the workbook-inclusive calculation separately.")
        st.markdown("**2050 electricity-export scenario**")
        st.write("Thesis Table 10 reports 3,075.33 TWh/year. The EnergyPLAN results workbook identifies this as renewable electricity production. It separately reports 9.81 TWh/year from PP2 (condensing generation), giving approximately 3,085.14 TWh/year when those two indicators are combined. The later thesis narrative reports 3,179.58 TWh/year; this figure is not supported by the supplied EnergyPLAN results workbook and is retained here only as a documented discrepancy, not as a validated total.")
        st.markdown("**Storage units and interpretation**")
        st.write("The thesis reports battery energy capacity in TWh in its scenario tables. This dashboard converts those values to GWh for readability: for example, 1.33 TWh = 1,330 GWh in the domestic base case and 5.175 TWh = 5,175 GWh in the electricity-export case. Battery energy capacity is distinct from charging/discharging power (MW), and neither should be added to annual electricity generation.")
        st.info("Reference hierarchy: the final 2025 thesis is the primary source for published thesis results. Supporting EnergyPLAN workbooks are used to clarify indicator scope and arithmetic, not to silently overwrite thesis tables. The 908.72 TWh/year figure is final energy demand; it is not comparable to annual electricity-generation totals.")
    st.caption("Sources: thesis Tables 9–18 and Section 4.2, approximately pp. 78–95.")

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
