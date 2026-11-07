import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from site_selection_map_component import render_site_admin_map

st.set_page_config(page_title="Algeria Energy Transition Explorer", page_icon="⚡", layout="wide")
DATA = Path(__file__).parent / "data"

def load_data(name):
    with (DATA / name).open(encoding="utf-8") as f:
        return json.load(f)

exports = pd.DataFrame(load_data("export_scenarios.json"))
criteria = pd.DataFrame(load_data("siting_criteria.json"))

# Exact normalized scores and weights transcribed from the user's original MCDA Excel table.
# The Excel matrix is the single source for the interactive weighted-sum calculation.
mcda_weights = [0.30, 0.25, 0.20, 0.20, 0.15, 0.15, 0.15, 0.10, 0.10, 0.10, 0.10, 0.10, 0.05, 0.05]
mcda_scores = [
    [96.34146, 87.80488, 100.0, 50.0],
    [75.38462, 50.0, 56.92308, 100.0],
    [82.59505, 100.0, 94.42911, 50.0],
    [57.84047, 100.0, 83.09228, 50.0],
    [100.0, 50.0, 76.01754, 60.91691],
    [63.04421, 100.0, 83.72216, 50.0],
    [57.61896, 100.0, 95.48547, 50.0],
    [73.39730, 100.0, 78.50094, 50.0],
    [50.0, 100.0, 100.0, 50.0],
    [100.0, 50.0, 50.27721, 50.29412],
    [57.04846, 100.0, 50.0, 55.06608],
    [100.0, 50.0, 50.0, 50.0],
    [93.75, 50.0, 87.5, 100.0],
    [88.30769, 50.0, 58.92308, 100.0],
]
mcda_criteria_names = [
    "Annual Wind Average speed at 100 m height",
    "Annual Solar Irradiation (GHI)",
    "Proximity to Mediterranean Coast",
    "Extent of Existing Natural Gas Infrastructure (H2 and E-Methane)",
    "Available Land Area",
    "Extent of Existing Road Network",
    "Proximity to Export Point Italy (HVDC)",
    "Proximity to Export Point Spain (HVDC)",
    "Distance to Existing Electricity Grid",
    "Environmental Protection Area distance",
    "Local Unemployment Rate",
    "Historical Rehabilitation Potential",
    "Administrative Complexity (Number of Provinces)",
    "Population Density",
]
criteria["criterion"] = mcda_criteria_names
criteria["weight"] = mcda_weights
criteria["scores"] = mcda_scores
sites = pd.DataFrame(load_data("siting_sites.json"))

st.title("Algeria Energy Transition Explorer")
st.caption("An interactive presentation of the findings of *Powering EU?* (2025)")
st.info("The final thesis is the primary reference for published results. Interactive sensitivities are separate and do not replace EnergyPLAN modelling.")

pages = [
    "Research overview",
    "Scenario comparison",
    "Renewable energy siting",
    "Technical assessment",
    "Social assessment",
    "Environmental assessment",
    "Interactive scenario explorer",
    "Methodology and sources",
    "Thesis limitations and critical considerations",
    "Future development",
]
page = st.sidebar.radio("Research modules", pages)

if page == "Research overview":
    st.header("Research overview")
    st.write("The thesis investigates how Algeria could transition towards a 100% renewable energy system by 2050 while potentially supplying energy to Europe through three export pathways: electricity, green hydrogen and e-methane.")
    st.subheader("Research objective")
    st.write("The research compares a domestic renewable-energy pathway with three export-oriented pathways. It assesses their energy-system configurations and considers their technical, economic, social and environmental implications.")
    st.subheader("The five scenarios and their purpose")
    scenario_overview = pd.DataFrame([
        {"Scenario": "Algeria 2019 baseline", "Purpose": "Historical reference for Algeria's energy system"},
        {"Scenario": "2050 Domestic Base", "Purpose": "100% renewable system designed to meet domestic demand"},
        {"Scenario": "2050 Electricity Export", "Purpose": "Domestic transition plus electricity exports through HVDC"},
        {"Scenario": "2050 Green Hydrogen Export", "Purpose": "Domestic transition plus green hydrogen exports"},
        {"Scenario": "2050 E-methane Export", "Purpose": "Domestic transition plus e-methane exports"},
    ])
    st.dataframe(scenario_overview, hide_index=True, use_container_width=True)

    st.subheader("Final energy demand: domestic requirement")
    st.write("The thesis reports final energy demand for Algeria's domestic use. The 2050 export scenarios retain this domestic demand requirement; the energy produced for export is additional to it.")
    demand_df = pd.DataFrame([
        {
            "Period": "2019",
            "Scenario(s)": "Algeria 2019 baseline",
            "Domestic final energy demand (TWh/year)": 465.95,
            "Reference": "Thesis Table 6, p. 63",
        },
        {
            "Period": "2050",
            "Scenario(s)": "Domestic Base; Electricity Export; Green Hydrogen Export; E-methane Export",
            "Domestic final energy demand (TWh/year)": 908.72,
            "Reference": "Same domestic demand assumption across all four 2050 scenarios",
        },
    ])
    st.dataframe(demand_df, hide_index=True, use_container_width=True)
    a, b, c = st.columns(3)
    a.metric("2050 domestic final demand", "908.72 TWh/year")
    b.metric("Export pathways assessed", "3")
    c.metric("Energy-system model", "EnergyPLAN 16.3")
    st.info("Domestic final energy demand is not the same as total energy generation. Electricity, hydrogen or e-methane produced for export is additional to the domestic final-demand requirement. The thesis gives the 2019 and 2050 demand totals in Table 6 (p. 63); the same 2050 domestic demand assumption is used when comparing the four 2050 pathways.")
    st.subheader("Research questions")
    st.write("To address its objectives, the thesis investigates three main questions:")
    st.markdown("""
    **1. Technical potential and infrastructure**  
    What is Algeria's potential to export renewable electricity, green hydrogen and e-methane to Europe, and what technical and infrastructure requirements would these pathways involve?

    **2. Economic competitiveness**  
    How do the costs and economic benefits of the three export pathways compare with one another and with Algeria's existing fossil-fuel-based export system?

    **3. Social and environmental implications**  
    What potential social and environmental benefits could renewable energy exports bring to Algerian communities and society more broadly?
    """)
    st.subheader("Four dimensions considered")
    st.markdown("""
    - **Technical:** energy-system configuration, renewable generation, storage, energy balances and export infrastructure.
    - **Economic:** investment and system costs, export revenues, profitability and levelised cost of export (LCOX).
    - **Social:** employment, water access, regional equity and socioeconomic development.
    - **Environmental:** land requirements, energy-related water demand and emissions.
    """)
    st.caption("The research questions provide the framework for the assessment sections below. The thesis is the primary reference for reported findings.")

elif page == "Renewable energy siting":
    st.header("Renewable energy siting assessment")
    st.write("The thesis applies a two-step process: preliminary spatial filtering, followed by a multi-criteria suitability assessment (MCDA).")

    st.subheader("Step 1 — Candidate development zones")
    st.write("The thesis manually delineates four large candidate zones after excluding mountainous and steep-slope areas, high-density urban zones, northern Algeria, small or isolated areas and protected regions.")
    st.markdown("**Interactive administrative reference map — satellite imagery**")
    st.write("Explore the historical 58-wilaya administrative layer over satellite imagery. The wilaya associations are indicative geographical references only; they are not the exact boundaries of the four manually delineated candidate zones.")
    render_site_admin_map()

    map_path = Path(__file__).parent / "assets" / "thesis_site_selection_map.png"
    if map_path.exists():
        with st.expander("View the original thesis map (Figure 2.1)"):
            st.image(str(map_path), caption="Original Figure 2.1 from the 2025 thesis, retained for reference.", use_container_width=True)

    st.warning("The four candidate zones were manually delineated in the thesis. Their exact GIS polygons or coordinates were not provided. The interactive map displays the administrative reference layer and should not be interpreted as a newly verified GIS boundary dataset. Pipeline lines and labels should also be read according to the thesis limitations discussed in the infrastructure assessment.")

    site_choice = st.selectbox("Explore a candidate site", sites["site"].tolist(), key="siting_site_detail")
    selected_site = sites.loc[sites["site"] == site_choice].iloc[0]
    a, b = st.columns(2)
    a.metric("Candidate zone", selected_site["site"])
    b.metric("Region", selected_site["region"])
    st.write("**Provinces listed in Appendix 2:** " + ", ".join(selected_site["provinces"]))
    st.caption("The detailed province lists reproduce Appendix 2. The association is indicative and is not a verified GIS definition of the candidate-zone boundaries.")

    st.subheader("Step 2 — Multi-criteria suitability assessment")
    st.write("The 14 criterion scores and weights below reproduce the normalized-score matrix and weights in the original MCDA Excel calculation supplied for this dashboard. Scores use the thesis Min–Max scale from 50 (least favourable) to 100 (most favourable).")

    score_matrix = pd.DataFrame({"Criterion": criteria["criterion"], "Thesis weight": criteria["weight"], "Scoring preference": criteria["direction"]})
    for i, site in sites.iterrows():
        score_matrix[site["site"]] = criteria["scores"].apply(lambda values: values[i])
    with st.expander("View the criterion scores and weights from Appendix 2, Table 2.2"):
        st.dataframe(score_matrix, hide_index=True, use_container_width=True)

    st.subheader("Adjust the criteria weights")
    st.write("Change the relative importance of the 14 criteria. The tool recalculates the weighted sum and ranking for all four candidate sites. The weights are applied exactly as entered; they are not automatically rescaled or converted into percentages.")

    if st.button("Reset weights to thesis values", key="reset_siting_weights"):
        for i, item in criteria.iterrows():
            st.session_state[f"siting_weight_{i}"] = float(item["weight"])
        st.rerun()

    weight_cols = st.columns(2)
    entered_weights = []
    for i, item in criteria.iterrows():
        with weight_cols[i % 2]:
            value = st.slider(
                item["criterion"], min_value=0.0, max_value=0.5,
                value=float(item["weight"]), step=0.01,
                key=f"siting_weight_{i}", help=f"Thesis weight: {item['weight']:.2f}. {item['direction']}"
            )
        entered_weights.append(value)

    entered_total = sum(entered_weights)
    thesis_weight_total = float(criteria["weight"].sum())
    if entered_total <= 0:
        st.warning("Increase at least one criterion weight to calculate a ranking.")
    else:
        applied_weights = entered_weights
        score_values = [[float(v) for v in row] for row in criteria["scores"]]
        weighted_scores = []
        for site_index in range(len(sites)):
            weighted_score = sum(applied_weights[i] * score_values[i][site_index] for i in range(len(criteria)))
            weighted_scores.append(weighted_score)

        result = sites[["site", "region"]].copy()
        result["Weighted score"] = weighted_scores
        result = result.sort_values(["Weighted score", "site"], ascending=[False, True]).reset_index(drop=True)
        result["Rank"] = range(1, len(result) + 1)
        st.dataframe(result[["Rank", "site", "region", "Weighted score"]].round({"Weighted score": 2}), hide_index=True, use_container_width=True)
        if abs(entered_total - thesis_weight_total) < 1e-9:
            st.caption("With the original Excel weights, the calculated totals are 156.08 (Site 01), 161.34 (Site 02), 158.22 (Site 03) and 119.67 (Site 04). These reproduce the Excel weighted-sum results and ranks 3, 1, 2 and 4.")
        else:
            st.caption(f"Current weight total: {entered_total:.2f}. The total changes when you adjust weights; this is intentional because the tool applies the entered coefficients directly.")

        chart = px.bar(
            result.sort_values("Rank"), x="site", y="Weighted score", text="Rank",
            title="Candidate-site ranking under the selected criteria weights",
            labels={"site": "Candidate site", "Weighted score": "Weighted score", "Rank": "Rank"}
        )
        chart.update_traces(textposition="outside")
        chart.update_yaxes(range=[0, 210])
        st.plotly_chart(chart, use_container_width=True)

        winner = result.iloc[0]
        st.success(f"Under the current weighting choices, {winner['site']} ranks first with a weighted score of {winner['Weighted score']:.2f}.")

        with st.expander("View the weights applied in this calculation"):
            weight_view = criteria[["criterion", "weight"]].copy()
            weight_view["Selected slider value"] = entered_weights
            weight_view["Applied weight"] = applied_weights
            weight_view = weight_view.rename(columns={"weight": "Thesis weight"})
            st.dataframe(weight_view.round({"Thesis weight": 3, "Selected slider value": 3, "Applied weight": 3}), hide_index=True, use_container_width=True)
            st.caption(f"Applied weights total: {sum(applied_weights):.2f}. No automatic normalization is applied.")

    st.subheader("Explore an individual criterion")
    selected = st.selectbox("Choose an indicator", criteria["criterion"].tolist(), key="siting_criterion_detail")
    item = criteria.loc[criteria["criterion"] == selected].iloc[0]
    rows = [{"Candidate site": sites.iloc[i]["site"], "Reported raw value": item["raw"][i], "Normalised criterion score": item["scores"][i]} for i in range(len(sites))]
    st.write(f"**Thesis weight:** {item['weight']:.2f}  |  **Scoring preference:** {item['direction']}")
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    st.subheader("Scoring equations")
    st.latex(r"Score(x)=50+\left(\frac{x-x_{min}}{x_{max}-x_{min}}\right)\times 50")
    st.latex(r"Score_{reverse}(x)=100-\left(\frac{x-x_{min}}{x_{max}-x_{min}}\right)\times 50")
    st.latex(r"Weighted\ score=\sum_i (weight_i\times criterion\ score_i)")

    with st.expander("Methodological notes and limitations reported in Appendix 2"):
        st.markdown("""
        - Wind and solar data are attributed to DTU Wind Energy & World Bank Group (2025) and World Bank Group (2025).
        - Distances, except for roads, are estimated as straight-line (Euclidean) values and do not reflect topographical terrain.
        - Desalination, grid connection and HVDC export proximity were prioritised because of their role in hydrogen production and electricity exports.
        - For Site 01 and Site 04, gas-infrastructure values of −200 and −500 represent approximate distances to the nearest connection point because no pipelines cross those zones. For Sites 02 and 03, the values represent existing gas-pipeline length within the site boundaries.
        - Road network coverage is based on the extent of major roads passing through the sites.
        - Electricity grid availability was qualitatively assessed from regional grid maps.
        - Unemployment and population density are based on 2019 provincial-level averages.
        - Environmental suitability is based on distance from protected or ecologically sensitive areas.
        """)
        st.info("The weights in the supplied Excel calculation sum to 2.00. They are importance coefficients, not percentages, and are intentionally preserved without normalization. The electricity-grid-distance scores (50 or 100) and historical-rehabilitation scores (100 for Site 01; 50 for Sites 02–04) are assumption-based inputs in the original calculation. They are retained as supplied.")

    st.caption("This interactive MCDA is a sensitivity analysis of the thesis criteria and weights. It does not rerun EnergyPLAN. Exact clickable site polygons would require original GIS boundaries or site-coordinate data, which were not provided in the thesis.")

elif page == "Technical assessment":
    st.header("Technical assessment")
    st.write("This section addresses the first research question: Algeria's potential to export renewable electricity, green hydrogen and e-methane to Europe, together with the energy-system configurations, storage and export infrastructure considered in the thesis.")
    st.info("The figures below are thesis scenario results and technical assumptions. They describe modelled configurations; they do not by themselves demonstrate that the projects or export infrastructure have been built or are ready for implementation.")
    tech = load_data("technical_results.json")
    tech_df = pd.DataFrame(tech["scenarios"])
    selected = st.selectbox("Select a scenario", tech_df["name"].tolist())
    row = tech_df.loc[tech_df["name"] == selected].iloc[0]
    a,b,c = st.columns(3)
    a.metric("Onshore wind capacity", f"{row['wind_MW']:,.0f} MW")
    b.metric("Solar PV capacity", f"{row['pv_MW']:,.0f} MW")
    c.metric("Electrolyser capacity", f"{row['electrolyser_MW']:,.0f} MW")
    st.subheader("Scenario configuration")
    st.caption("Installed capacities are power ratings (MW); annual wind and solar generation are energy quantities (TWh/year). Storage capacities are shown separately in GWh. These units describe different aspects of the system and should not be compared as if they were interchangeable.")
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
    st.dataframe(tech_df[["name","battery_GWh","hydrogen_GWh","gas_GWh"]].rename(columns={"name":"Scenario","battery_GWh":"Battery storage (GWh)","hydrogen_GWh":"Hydrogen storage (GWh)","gas_GWh":"Gas storage (GWh)"}),hide_index=True,use_container_width=True)
    st.caption("Storage capacities represent stored-energy capacity, not annual generation. Electricity discharged from storage is not new primary generation and should not be counted again as additional energy production.")
    st.metric("Critical excess electricity production — electricity export",f"{tech['notes']['electricity_export_CEEP_TWh']} TWh/year")
    st.write(f"The electricity export case models {tech['notes']['electricity_export_input_TWh']} TWh/year entering the export chain. The thesis assumes {tech['notes']['electricity_export_losses_TWh']} TWh of losses, leaving {tech['notes']['electricity_export_net_TWh']} TWh/year delivered. Flexible demand is estimated at {tech['notes']['flexible_demand_TWh']} TWh/year.")
    with st.expander("Electricity HVDC routes — thesis Tables 15–16"):
        st.dataframe(pd.DataFrame(tech["hvdc"]),hide_index=True,use_container_width=True)
    with st.expander("Hydrogen pipeline routes — thesis Table 18"):
        st.dataframe(pd.DataFrame(tech["hydrogen_routes"]),hide_index=True,use_container_width=True)
    st.caption("Sources: thesis Tables 9–18 and Section 4.2, approximately pp. 78–95.")

elif page == "Scenario comparison":
    st.header("Scenario comparison: domestic transition and energy exports")
    st.write("Compare the 2019 baseline and four 2050 pathways across the thesis’s technical, economic, social and environmental assessment dimensions.")
    st.info("The comparison preserves the thesis’s source coverage. Where the thesis dataset supplied for this dashboard does not provide a comparable indicator for a scenario, the table shows ‘Not reported’ rather than estimating or filling the gap.")

    tech = load_data("technical_results.json")
    social_env = load_data("social_environment.json")
    tech_df = pd.DataFrame(tech["scenarios"])
    emp_df = pd.DataFrame(social_env["employment"])
    water_df = pd.DataFrame(social_env["water_demand"])
    land_df = pd.DataFrame(social_env["solar_land_use"])
    econ_df = exports.copy()

    scenario_names = [
        "Algeria 2019 baseline",
        "2050 Domestic Base",
        "2050 Electricity Export",
        "2050 Green Hydrogen Export",
        "2050 E-methane Export",
    ]
    tech_names = {
        "2050 Domestic Base": "2050 Domestic Base",
        "2050 Electricity Export": "2050 Electricity Export",
        "2050 Green Hydrogen Export": "2050 Green Hydrogen Export",
        "2050 E-methane Export": "2050 E-methane Export",
    }
    emp_map = emp_df.set_index("scenario").to_dict("index")
    water_map = water_df.set_index("scenario").to_dict("index")
    land_map = land_df.set_index("scenario").to_dict("index")
    tech_map = tech_df.set_index("name").to_dict("index")
    econ_map = econ_df.set_index("scenario").to_dict("index")

    # At-a-glance comparison. Thesis results remain primary; additional 2019 figures
    # supplied in the comparison workbook are explicitly labelled supplementary.
    supplementary_2019 = {
        "wind_pv_generation_TWh_year": 0.70,
        "battery_storage_GWh": 0,
        "total_water_demand_Gm3_year": 0.002,
        "pv_land_km2": 3.0,
    }
    rows = []
    for label in scenario_names:
        is_2019 = label == "Algeria 2019 baseline"
        t = tech_map.get(label, {})
        e = emp_map.get(label, {})
        w = water_map.get(label, {})
        l = land_map.get(label, {})
        econ_key = {"2050 Electricity Export":"Electricity", "2050 Green Hydrogen Export":"Green hydrogen", "2050 E-methane Export":"E-methane"}.get(label)
        ec = econ_map.get(econ_key, {}) if econ_key else {}

        if is_2019:
            rows.append({
                "Scenario": label,
                "Domestic final energy demand (TWh/y)": 465.95,
                "Technical — wind + PV generation (TWh/y)": supplementary_2019["wind_pv_generation_TWh_year"],
                "Technical — battery storage (GWh)": supplementary_2019["battery_storage_GWh"],
                "Economic — export product": "Not reported for 2019 baseline",
                "Economic — export volume (TWh/y)": "Not reported",
                "Economic — revenue (€bn/y)": "Not reported",
                "Economic — reported net profit (€bn/y)": "Not reported",
                "Social — permanent jobs": "Not available",
                "Social — temporary job-years": "Not available",
                "Environmental — total water demand (Gm³/y)": supplementary_2019["total_water_demand_Gm3_year"],
                "Environmental — PV land (km²)": supplementary_2019["pv_land_km2"],
                "Data provenance": "Supplementary 2019 figures from user-provided comparison; source/method notes required",
            })
            continue

        product = "No exports" if not econ_key else {"Electricity":"Electricity", "Green hydrogen":"Green hydrogen", "E-methane":"E-methane"}[econ_key]
        rows.append({
            "Scenario": label,
            "Domestic final energy demand (TWh/y)": 908.72,
            "Technical — wind + PV generation (TWh/y)": round(t.get("wind_TWh", 0) + t.get("pv_TWh", 0), 2) if t else "Not reported",
            "Technical — battery storage (GWh)": t.get("battery_GWh", "Not reported"),
            "Economic — export product": product,
            "Economic — export volume (TWh/y)": ec.get("export_volume_TWh_year", "Not applicable" if not econ_key else "Not reported"),
            "Economic — revenue (€bn/y)": ec.get("annual_revenue_EUR_bn", "Not applicable" if not econ_key else "Not reported"),
            "Economic — reported net profit (€bn/y)": ec.get("reported_net_profit_EUR_bn", "Not applicable" if not econ_key else "Not reported"),
            "Social — permanent jobs": e.get("permanent_jobs", "Not reported"),
            "Social — temporary job-years": e.get("temporary_job_years", "Not reported"),
            "Environmental — total water demand (Gm³/y)": w.get("total_water_demand_Gm3_year", "Not reported"),
            "Environmental — PV land (km²)": l.get("land_km2", "Not reported"),
            "Data provenance": "Thesis reference results / supporting workbook where noted",
        })
    comparison = pd.DataFrame(rows)

    st.subheader("At-a-glance comparison across the four dimensions")
    st.write("Use the tabs to compare each assessment dimension separately. This keeps the scenario comparison readable without combining unrelated units in one very wide table.")
    tab_tech, tab_econ, tab_social, tab_environment = st.tabs(["Technical", "Economic", "Social", "Environmental"])
    with tab_tech:
        st.dataframe(comparison[["Scenario", "Domestic final energy demand (TWh/y)", "Technical — wind + PV generation (TWh/y)", "Technical — battery storage (GWh)", "Data provenance"]], hide_index=True, use_container_width=True)
    with tab_econ:
        st.dataframe(comparison[["Scenario", "Economic — export product", "Economic — export volume (TWh/y)", "Economic — revenue (€bn/y)", "Economic — reported net profit (€bn/y)"]], hide_index=True, use_container_width=True)
    with tab_social:
        st.dataframe(comparison[["Scenario", "Social — permanent jobs", "Social — temporary job-years"]], hide_index=True, use_container_width=True)
    with tab_environment:
        st.dataframe(comparison[["Scenario", "Environmental — total water demand (Gm³/y)", "Environmental — PV land (km²)"]], hide_index=True, use_container_width=True)
    st.caption("The thesis is the primary reference for the comparison. Selected 2019 technical, water-demand and land figures are supplementary information from the user's comparison table; they are not presented as thesis-reported results. 2024 trade statistics are excluded from this scenario table because they fall outside its 2019 baseline and 2050 thesis-scenario scope.")
    with st.expander("How to read the data and supplementary 2019 figures"):
        st.markdown("""
        - **Thesis:** published findings and scenario results from the 2025 master's thesis.
        - **Supplementary:** additional figures supplied in the comparison table and supporting workbook material; these extend the thesis explanation but are not presented as thesis findings.
        - The supplementary 2019 wind + PV generation figure is **0.70 TWh/year** (0.03 TWh wind + 0.67 TWh PV).
        - 2019 electricity export volume and export value are shown as **Not reported** in this comparison because the available 0.67 TWh and €0.294bn figures refer to a separate 2024 trade-data reference, not the 2019 baseline. The 2024 figures are therefore excluded to keep the thesis comparison focused and avoid mixing years.
        - The 2024 trade figures are not used as net profit or as 2050 thesis results.
        - For hydrogen and e-methane, export volume refers to the named export product, not electricity.
        - Permanent jobs and temporary job-years are different measures and must not be added together.
        - Household water access is a social benefit; water demand by the energy system is an environmental indicator.
        - The 2019 water-demand and PV-land figures are supplementary and need a clearly stated source, scope and calculation method before being treated as directly comparable with 2050 results.
        """)

    st.subheader("Technical dimension")
    st.write("Installed wind and PV generation and battery storage are compared for the four 2050 configurations. The 2019 baseline wind + PV generation and battery figures are supplementary historical/model values supplied in the comparison table; the four 2050 configurations use thesis reference results and supporting workbook data.")
    if not tech_df.empty:
        gen = tech_df[["name", "wind_TWh", "pv_TWh"]].melt(id_vars="name", var_name="Technology", value_name="Generation (TWh/year)")
        gen["Technology"] = gen["Technology"].map({"wind_TWh":"Wind", "pv_TWh":"Solar PV"})
        st.plotly_chart(px.bar(gen, x="name", y="Generation (TWh/year)", color="Technology", barmode="group", title="Annual wind and PV generation — 2050 scenarios"), use_container_width=True)
        st.plotly_chart(px.bar(tech_df, x="name", y="battery_GWh", title="Battery storage requirements — 2050 scenarios", labels={"name":"2050 scenario", "battery_GWh":"Battery storage (GWh)"}), use_container_width=True)

    st.subheader("Economic dimension")
    st.write("Economic values are available for the three export pathways. The domestic scenarios have no export revenue or export profit in this comparison.")
    econ_view = exports[["scenario", "export_volume_TWh_year", "annual_revenue_EUR_bn", "reported_net_profit_EUR_bn", "LCOX_EUR_MWh"]].rename(columns={
        "scenario":"Export pathway", "export_volume_TWh_year":"Delivered exports (TWh/year)",
        "annual_revenue_EUR_bn":"Revenue (€bn/year)", "reported_net_profit_EUR_bn":"Reported net profit (€bn/year)",
        "LCOX_EUR_MWh":"LCOX (€/MWh)"})
    st.dataframe(econ_view, hide_index=True, use_container_width=True)
    st.plotly_chart(px.bar(exports, x="scenario", y="reported_net_profit_EUR_bn", title="Reported net profit by export pathway", labels={"scenario":"Export pathway", "reported_net_profit_EUR_bn":"€bn/year"}), use_container_width=True)
    st.markdown("**Cost calculation detail**")
    cost_view = exports[["scenario", "annual_export_cost_for_profit_EUR_bn", "incremental_system_cost_for_LCOX_EUR_bn", "LCOX_EUR_MWh"]].rename(columns={
        "scenario":"Export pathway",
        "annual_export_cost_for_profit_EUR_bn":"Cost used for reported profit (€bn/year)",
        "incremental_system_cost_for_LCOX_EUR_bn":"Incremental system cost for LCOX (€bn/year)",
        "LCOX_EUR_MWh":"LCOX (€/MWh)"
    })
    st.dataframe(cost_view, hide_index=True, use_container_width=True)
    st.caption("The export cost used for reported net profit and the incremental system cost used for LCOX are separate calculations and should not be treated as interchangeable.")

    st.subheader("Social dimension")
    st.write("Employment figures cover the four 2050 scenarios. Permanent jobs are ongoing positions; temporary employment is expressed in job-years. These units are not added together.")
    st.dataframe(emp_df.rename(columns={"scenario":"2050 scenario", "permanent_jobs":"Permanent jobs", "temporary_job_years":"Temporary job-years"}), hide_index=True, use_container_width=True)
    st.plotly_chart(px.bar(emp_df, x="scenario", y="permanent_jobs", title="Permanent employment — 2050 scenarios", labels={"scenario":"Scenario", "permanent_jobs":"Jobs"}), use_container_width=True)
    st.plotly_chart(px.bar(emp_df, x="scenario", y="temporary_job_years", title="Temporary employment — 2050 scenarios", labels={"scenario":"Scenario", "temporary_job_years":"Job-years"}), use_container_width=True)
    wa = social_env["water_access"]
    st.markdown("**Shared 2050 social water-access ambition (not a scenario-specific difference):** "
                f"{wa['water_access_current_percent']}% current access to {wa['water_access_2050_percent']}% target; "
                f"{wa['water_per_capita_current_m3_year']} to approximately {wa['water_per_capita_2050_m3_year']} m³/person/year; "
                f"over {wa['planned_water_pipeline_km']:,} km of planned pipelines and {wa['desalination_share_2050_percent']}% desalination share.")

    st.subheader("Environmental dimension")
    st.write("The table separates total water demand for the energy scenarios from PV land requirements. Household water access is treated as a social benefit, not an environmental indicator.")
    env_view = water_df.merge(land_df[["scenario", "land_km2", "share_site_02_percent"]], on="scenario", how="left")
    st.dataframe(env_view.rename(columns={"scenario":"2050 scenario", "total_water_demand_Gm3_year":"Total water demand (Gm³/year)", "non_energy_use_Gm3_year":"Non-energy water use (Gm³/year)", "hydrogen_production_water_Gm3_year":"Hydrogen production (Gm³/year)", "pv_wind_operations_water_Gm3_year":"PV/wind operations (Gm³/year)", "land_km2":"PV land estimate (km²)", "share_site_02_percent":"Share of Site 02 (%)"}), hide_index=True, use_container_width=True)
    st.plotly_chart(px.bar(water_df, x="scenario", y="total_water_demand_Gm3_year", title="Total water demand — 2050 scenarios", labels={"scenario":"Scenario", "total_water_demand_Gm3_year":"Gm³/year"}), use_container_width=True)
    st.plotly_chart(px.bar(land_df, x="scenario", y="land_km2", title="Estimated solar PV land requirements — 2050 scenarios", labels={"scenario":"Scenario", "land_km2":"Land (km²)"}), use_container_width=True)
    em = social_env["emissions"]
    emissions_rows = [
        {"Scenario":"Algeria 2019 baseline", "Reported CO₂ (Mt/year)":em["domestic_2019"], "Accounting scope":"Domestic energy-related emissions"},
        {"Scenario":"2050 Domestic Base", "Reported CO₂ (Mt/year)":em["domestic_2050_all_scenarios"], "Accounting scope":"Domestic energy-system scenario"},
        {"Scenario":"2050 Electricity Export", "Reported CO₂ (Mt/year)":em["including_exports_2050"]["Electricity Export"], "Accounting scope":"Including exports"},
        {"Scenario":"2050 Green Hydrogen Export", "Reported CO₂ (Mt/year)":em["including_exports_2050"]["Green Hydrogen Export"], "Accounting scope":"Including exports"},
        {"Scenario":"2050 E-methane Export", "Reported CO₂ (Mt/year)":em["including_exports_2050"]["E-methane Export"], "Accounting scope":"Including exports"},
    ]
    st.markdown("**Thesis-reported CO₂ comparison**")
    st.dataframe(pd.DataFrame(emissions_rows), hide_index=True, use_container_width=True)
    st.warning("The negative e-methane value is a thesis accounting result linked to the allocation of captured CO₂ to importing countries. It is not a verified full lifecycle net-negative emissions result. The thesis also notes that non-CO₂ greenhouse gases are not fully eliminated.")

    with st.expander("How to interpret this comparison"):
        st.markdown("""
        - The 2019 baseline is included in the five-scenario framework, but not every indicator is available in the current extracted reference dataset for direct comparison.
        - Technical, employment and environmental scenario indicators shown here are the thesis reference values currently integrated for the four 2050 scenarios.
        - Economic indicators are shown only for the three export pathways.
        - Water access, per-capita availability, pipeline length and desalination share are shared 2050 social targets/assumptions, not differentiated scenario outcomes.
        - This page compares published reference values; it does not run EnergyPLAN or establish new system-feasibility results.
        """)

elif page == "Social assessment":
    st.header("Social assessment")
    se = load_data("social_environment.json")
    emp = pd.DataFrame(se["employment"])
    st.write("The thesis estimates employment across the domestic base and three export pathways. Permanent jobs and temporary job-years are shown separately because they represent different types and durations of employment.")
    st.info("Employment methodology: permanent jobs represent ongoing positions, while temporary employment is expressed in job-years. The two measures are calculated differently and should be interpreted separately, not added together.")
    a,b = st.columns(2)
    a.metric("Highest permanent employment", f"{emp['permanent_jobs'].max():,.0f} jobs", "Electricity export")
    b.metric("Highest temporary employment", f"{emp['temporary_job_years'].max():,.0f} job-years", "Electricity export")
    st.subheader("Employment estimates by scenario")
    st.dataframe(emp.rename(columns={"scenario":"Scenario","permanent_jobs":"Permanent jobs (annual)","temporary_job_years":"Temporary employment (job-years)"}),hide_index=True,use_container_width=True)
    chart = emp.melt(id_vars="scenario",value_vars=["permanent_jobs","temporary_job_years"],var_name="Employment type",value_name="Estimated total")
    chart["Employment type"] = chart["Employment type"].map({"permanent_jobs":"Permanent jobs","temporary_job_years":"Temporary job-years"})
    st.plotly_chart(px.bar(chart,x="scenario",y="Estimated total",color="Employment type",barmode="group",title="Employment estimates (different units; compare within each category)"),use_container_width=True)
    with st.expander("How the thesis estimates employment"):
        method = se["employment_method"]
        st.write("**Permanent:** " + method["permanent_jobs"])
        st.write("**Temporary:** " + method["temporary_jobs"])
        st.write("Adjustment factors: " + ", ".join(f"{k.replace('_',' ')} = {v}" for k,v in method["adjustment_factors"].items()) + ".")
        st.write(f"Desalination: {method['desalination_factor_jobs_per_million_m3_year']} jobs per million m³/year; the thesis says this relationship is valid up to {method['desalination_factor_limit_million_m3_year']} million m³/year and cautions against extrapolation beyond it.")
        st.write(f"HVDC transmission: {method['hvdc_jobs_per_billion_eur_investment']:,} jobs per €bn investment. Water infrastructure: {method['water_infrastructure_jobs_per_million_usd_investment']} jobs per US$ million investment.")
    st.subheader("Water security and access — a social benefit")
    w = se["water_access"]
    a,b,c = st.columns(3)
    a.metric("Water availability per capita", f"{w['water_per_capita_2050_m3_year']:,} m³/person/year", f"from {w['water_per_capita_current_m3_year']} m³/person/year")
    b.metric("Water access target", f"{w['water_access_2050_percent']}%", f"from {w['water_access_current_percent']}% in {w['current_reference_year']}")
    c.metric("Planned high-capacity pipelines", f">{w['planned_water_pipeline_km']:,} km")
    st.write(f"The thesis describes a 2050 water-production system in which desalination supplies {w['desalination_share_2050_percent']}% of production. Coastal desalination facilities would be connected to inland and southern regions through a high-capacity pipeline network.")
    st.caption("These are thesis projections and planned infrastructure, not achieved outcomes. Improved water access is presented here as a social benefit because it concerns household access, regional equity and quality of life.")

    st.subheader("Regional development and social equity in southern Algeria")
    st.write("The thesis argues that improved water and electricity services could help address long-standing regional inequalities, particularly in southern Algeria, where the quality and reliability of electricity supply and access to safe water are described as more limited.")
    st.markdown("""
    **Potential social and regional benefits identified in the thesis**
    - More reliable water supplies for households in remote and historically underserved areas.
    - Better conditions for local agriculture and livestock development.
    - Support for new population centres and a more balanced distribution of population and economic activity.
    - Improved logistics, lower transport costs and stronger local economic hubs.
    - Potential expansion of public services, including education and healthcare, as well as tourism and hospitality.
    - Vocational training and local workforce development to help residents access jobs created by the transition.
    """)
    st.info("These are expected co-benefits discussed in the thesis, not quantified or guaranteed outcomes. Their realisation depends on infrastructure delivery, local workforce development and the availability of public services.")

    st.subheader("Water stress and implementation risks")
    st.write(f"The thesis anticipates that {w['water_stressed_population_2050_description']} could be affected by water stress by 2050, alongside an anticipated {w['rainfall_decline_2050_percent']}% decline in national rainfall.")
    st.warning("The thesis also highlights a transition risk: if desalination and water-transmission infrastructure lag behind demand, some southern areas may remain dependent on groundwater in the short term. This could increase pressure on local aquifers. The timing and geographical coverage of water infrastructure therefore matter.")
    st.caption("The thesis reports national water access increasing from 70.6% to 100%. Its discussion of the southern regions separately describes current safe-water access as around 70%; these are retained as differently framed statements rather than treated as identical measurements.")
    st.warning("Employment values are modelled estimates, not guaranteed jobs. Permanent jobs are annual positions; temporary employment is measured in job-years. Do not add the two categories together.")

elif page == "Environmental assessment":
    st.header("Environmental assessment")
    se = load_data("social_environment.json")
    st.caption("This section covers environmental pressures from the energy system. Household access to clean water and regional water security are presented under Social Assessment.")
    st.subheader("Water demand across scenarios")
    water = pd.DataFrame(se["water_demand"])
    st.dataframe(water.rename(columns={"scenario":"Scenario","non_energy_use_Gm3_year":"Non-energy use (Gm³/year)","hydrogen_production_water_Gm3_year":"Hydrogen production (Gm³/year)","pv_wind_operations_water_Gm3_year":"PV/wind operations (Gm³/year)","total_water_demand_Gm3_year":"Total demand (Gm³/year)"}),hide_index=True,use_container_width=True)
    st.caption("Values transcribed from thesis Table 13. The thesis table also includes TWh energy-use rows; those are not water volumes and are not included in this table.")
    st.subheader("Estimated solar PV land requirement")
    land = pd.DataFrame(se["solar_land_use"])
    st.dataframe(land.rename(columns={"scenario":"Scenario","pv_generation_GWh_year":"PV generation (GWh/year)","land_km2":"Estimated PV land (km²)","share_site_02_percent":"Share of Site 02 (%)","share_national_area_percent":"Share of national area (%)"}),hide_index=True,use_container_width=True)
    st.plotly_chart(px.bar(land,x="scenario",y="land_km2",title="Estimated land required for solar PV (km²)"),use_container_width=True)
    st.caption("The thesis estimates PV land using 211.64 GWh/km²/year, based on 20% panel efficiency, 0.84 system efficiency, 0.24 capacity factor and 0.6 ground coverage ratio. This is a PV land estimate, not a complete footprint for all infrastructure.")
    st.subheader("CO₂ emissions reported in the thesis")
    em = se["emissions"]
    a,b,c = st.columns(3)
    a.metric("Domestic 2019", f"{em['domestic_2019']:.2f} Mt")
    b.metric("Domestic 2050", f"{em['domestic_2050_all_scenarios']:.0f} Mt", "All modelled scenarios")
    c.metric("E-methane export balance", f"{em['including_exports_2050']['E-methane Export']:.2f} Mt")
    st.write("Including exports, the thesis reports 284.67 Mt in 2019, zero for electricity and hydrogen exports in 2050, and −116.18 Mt for e-methane exports.")
    st.warning(em["non_co2_note"])
    with st.expander("Interpretation and limitations"):
        for item in se["limitations"]:
            st.write("• " + item)

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

elif page == "Methodology and sources":
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

elif page == "Thesis limitations and critical considerations":
    st.header("Thesis limitations and critical considerations")
    st.write("This section brings together qualifications that affect how the thesis results should be interpreted. It separates information documented in the thesis from additional observations identified during our review.")

    st.subheader("1. Technical modelling")
    st.markdown("**Interpretation of the thesis results**")
    st.write("The EnergyPLAN 16.3 scenarios are modelled energy-system configurations for 2050. Their results describe the performance of the modelled scenarios under the stated inputs and assumptions; they should not be read as proof that the systems have already been implemented or that every technical, regulatory and operational condition for implementation has been resolved.")
    st.markdown("**Additional critical consideration from our review**")
    st.write("The dashboard's interactive scenario explorer changes financial assumptions only. It does not rerun EnergyPLAN or recalculate hourly generation, storage, curtailment, transmission losses or physical system feasibility.")
    st.markdown("**Data discrepancies in the thesis**")
    st.write("The thesis reports domestic-base electricity generation as 2,134.33 TWh in Table 9 and 2,177.83 TWh in later narrative text. For the electricity-export scenario, Table 10 reports 3,075.33 TWh, while later narrative text reports 3,179.58 TWh. These figures are retained as reported and are not reconciled here.")

    st.subheader("2. Export infrastructure")
    st.markdown("**E-methane pipeline-capacity limitation — thesis figures**")
    st.write("The thesis reports a combined nominal capacity of 45.5 bcm/year for the operational TransMed and Medgaz pipelines (Table 4, p. 24). Using the thesis conversion of 10 TWh per bcm (Table 17, p. 83), this corresponds to 455 TWh/year. However, the 2050 e-methane scenario assumes exports of 574 TWh/year (Section 4.1.4), exceeding this capacity by 119 TWh/year, or approximately 11.9 bcm/year.")
    st.warning("The thesis does not include the additional pipeline capacity or investment costs that may be required to transport this difference. Consequently, its reported e-methane export costs and profitability do not account for the potential need to expand or construct pipeline infrastructure. This comparison is a capacity screening, not a pipeline engineering study.")
    st.caption("References: thesis Table 4 (p. 24), Table 17 (p. 83) and Section 4.1.4. The 119 TWh/year difference is calculated from the thesis figures; it is not a separately modelled thesis result.")

    st.subheader("3. Economic assessment")
    st.markdown("**Assumptions and interpretation**")
    st.write("Revenues and profitability depend on the thesis's assumed market prices, export volumes, costs and infrastructure arrangements. They are scenario results, not guaranteed commercial outcomes. Reported net profit and LCOX use different cost calculations.")

    st.subheader("4. Renewable-energy site selection")
    st.markdown("**Limitations documented in the thesis material**")
    st.write("The four candidate renewable-energy zones were manually delineated. Precise GIS polygons or coordinates for the zones are not provided in the thesis material used for this dashboard, so their exact boundaries cannot be independently reproduced from those sources.")
    st.markdown("**MCDA weighting note**")
    st.write("The original criterion weights sum to 2.00 rather than 1.00. They are retained as importance coefficients, without normalisation.")

    st.subheader("5. Environmental assessment")
    st.markdown("**Interpretation of the thesis results**")
    st.write("The land-use figures estimate solar PV land requirements under the thesis's stated assumptions; they do not represent the complete land footprint of all energy, transmission, water and export infrastructure. Water-demand estimates also depend on the scope and assumptions used in the thesis tables.")
    st.markdown("**Additional critical consideration from our review**")
    st.write("The negative e-methane CO₂ balance reported by the thesis (−116.18 Mt) reflects its accounting treatment, including allocation of captured CO₂ to importing countries. It should not be interpreted on its own as proof that the full e-methane value chain is lifecycle net-negative. Methane leakage and non-CO₂ greenhouse-gas emissions also remain relevant to the overall environmental assessment.")

elif page == "Future development":
    st.header("Future development")
    st.write("This section identifies possible directions for extending the research beyond the scope of the original thesis. These are proposals for further work, not findings or recommendations tested by the thesis.")
    st.markdown("""
    - **Renewable-energy siting:** develop precise GIS boundaries and conduct a more detailed spatial assessment of the four candidate zones.
    - **Export infrastructure:** examine pipeline and HVDC capacity, technical requirements, operating conditions and investment needs in greater detail.
    - **Economic assessment:** test alternative European market prices, financing arrangements and infrastructure-cost assumptions.
    - **Water resources:** assess water availability, desalination requirements and distribution infrastructure at regional scale.
    - **Implementation feasibility:** investigate regulatory, institutional, operational and investment conditions for each export pathway.
    - **Social and environmental impacts:** develop more detailed assessments of local employment, community impacts, land use, water resources and lifecycle emissions.
    """)


st.divider()
st.caption("Reference: Imadeddine Menakh (2025), *Powering EU? – Energy scenarios for exporting electricity, green hydrogen and e-methane from Algeria to Europe*.")
