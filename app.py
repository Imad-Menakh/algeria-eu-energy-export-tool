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
    "Algeria's energy system", "Technical assessment", "Five-scenario comparison", "Export scenario comparison", "Economic assessment",
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
        ("Social","Employment, water access, regional equity and socioeconomic development"),
        ("Environmental","Land requirements, energy-related water demand and emissions")
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

    **Social implications** — employment creation, improved access to safe water, water security, regional equity and socioeconomic development.

    **Environmental implications** — land requirements, water consumption associated with energy production, and emissions.
    """)
    st.caption("Detailed indicators and numerical results will be integrated from the corresponding thesis chapters and appendices.")

elif page == "Renewable energy siting":
    st.header("Renewable energy siting assessment")
    st.write("The thesis applies a two-step process: preliminary spatial filtering, followed by a multi-criteria suitability assessment (MCDA).")

    st.subheader("Step 1 — Candidate development zones")
    st.write("The thesis manually delineates four large candidate zones after excluding mountainous and steep-slope areas, high-density urban zones, northern Algeria, small or isolated areas and protected regions.")
    map_path = Path(__file__).parent / "assets" / "thesis_site_selection_map.png"
    if map_path.exists():
        st.image(str(map_path), caption="Figure 2.1 from the thesis: Renewable energy development zones in Algeria (2050). The original thesis map is shown without redrawing or inventing site boundaries.", use_container_width=True)

    st.caption("The thesis map is retained as the geographic reference. The site polygons are manually delineated in the thesis; precise GIS boundary files or coordinates were not supplied, so this update does not create artificial map coordinates.")
    site_choice = st.selectbox("Explore a candidate site", sites["site"].tolist(), key="siting_site_detail")
    selected_site = sites.loc[sites["site"] == site_choice].iloc[0]
    a, b, c = st.columns(3)
    a.metric("Thesis-reported total score", int(selected_site["score"]))
    b.metric("Thesis-reported rank", int(selected_site["rank"]))
    c.metric("Region", selected_site["region"])
    st.write("**Provinces included:** " + ", ".join(selected_site["provinces"]))
    st.caption("The detailed province lists reproduce Appendix 2. The main-text description of Site 02 is shorter; the appendix list is shown here.")

    st.subheader("Step 2 — Original MCDA assessment")
    st.write("Fourteen indicators are assessed using Min–Max normalisation on a scale from 50 (least favourable) to 100 (most favourable). Reverse scoring is applied where lower values are preferred.")
    score_matrix = pd.DataFrame({"Criterion":criteria["criterion"],"Original weight":criteria["weight"],"Scoring preference":criteria["direction"]})
    for i, site in sites.iterrows():
        score_matrix[site["site"]] = criteria["scores"].apply(lambda values: values[i])
    st.markdown("**Original criterion scores — Appendix 2, Table 2.2**")
    st.dataframe(score_matrix, hide_index=True, use_container_width=True)

    st.subheader("Original thesis ranking")
    ranked = sites.sort_values("rank")
    fig = px.bar(ranked, x="site", y="score", text="score", title="Thesis-reported MCDA total scores",
                 labels={"site":"Candidate site","score":"Reported total score"})
    fig.update_traces(textposition="outside")
    fig.update_yaxes(range=[0,180])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Interactive weighting experiment")
    st.write("Change the importance assigned to each criterion and see how the relative site ranking responds. The underlying thesis criterion scores remain fixed.")
    st.info("This is an exploratory weighted-score calculation, not a rerun of the thesis MCDA or EnergyPLAN. The published thesis totals and ranking above remain unchanged. Because the weights printed in Appendix 2 sum to 2.00 and the published totals cannot be reconstructed exactly from the displayed table, this explorer reports a separate weighted-average index on the original 50–100 score scale.")

    if st.button("Reset weights to thesis values", key="reset_siting_weights"):
        for i, item in criteria.iterrows():
            st.session_state[f"siting_weight_{i}"] = float(item["weight"])
        st.rerun()

    weight_cols = st.columns(2)
    interactive_weights = []
    for i, item in criteria.iterrows():
        with weight_cols[i % 2]:
            value = st.slider(
                item["criterion"], min_value=0.0, max_value=0.5,
                value=float(item["weight"]), step=0.01,
                key=f"siting_weight_{i}", help=f"Original thesis weight: {item['weight']:.2f}. {item['direction']}"
            )
        interactive_weights.append(value)

    weight_total = sum(interactive_weights)
    if weight_total <= 0:
        st.warning("Increase at least one criterion weight to calculate a ranking.")
    else:
        score_values = [[float(v) for v in row] for row in criteria["scores"]]
        interactive_scores = []
        for site_index in range(len(sites)):
            weighted_score = sum(interactive_weights[i] * score_values[i][site_index] for i in range(len(criteria))) / weight_total
            interactive_scores.append(weighted_score)
        result = sites[["site", "region", "score", "rank"]].copy()
        result["Interactive weighted index"] = interactive_scores
        result = result.sort_values("Interactive weighted index", ascending=False).reset_index(drop=True)
        result["Interactive rank"] = range(1, len(result) + 1)
        result = result.rename(columns={"score":"Thesis total score", "rank":"Thesis rank"})
        st.caption(f"Current adjustable weight total: {weight_total:.2f}. Weights are normalised proportionally inside the weighted-average calculation; the original thesis weights remain unchanged in the source data.")
        st.dataframe(result[["site", "region", "Thesis total score", "Thesis rank", "Interactive weighted index", "Interactive rank"]].round({"Interactive weighted index":2}), hide_index=True, use_container_width=True)
        chart = px.bar(result, x="site", y="Interactive weighted index", color="Interactive rank", text="Interactive rank", title="Site ranking under your selected criteria weights", labels={"site":"Candidate site", "Interactive weighted index":"Weighted index (50–100)", "Interactive rank":"New rank"})
        chart.update_traces(textposition="outside")
        chart.update_yaxes(range=[45,105])
        st.plotly_chart(chart, use_container_width=True)
        winner = result.iloc[0]
        st.success(f"Under the current weighting choices, {winner['site']} ranks first with an interactive index of {winner['Interactive weighted index']:.2f}.")

    st.subheader("Explore an individual criterion")
    selected = st.selectbox("Choose an indicator", criteria["criterion"].tolist(), key="siting_criterion_detail")
    item = criteria.loc[criteria["criterion"] == selected].iloc[0]
    rows = [{"Candidate site":sites.iloc[i]["site"],"Reported raw value":item["raw"][i],"Reported score":item["scores"][i]} for i in range(len(sites))]
    st.write(f"**Original weight:** {item['weight']:.2f}  |  **Scoring preference:** {item['direction']}")
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    st.subheader("Scoring equations")
    st.latex(r"Score(x)=50+\left(\frac{x-x_{min}}{x_{max}-x_{min}}\right)\times 50")
    st.latex(r"Score_{reverse}(x)=100-\left(\frac{x-x_{min}}{x_{max}-x_{min}}\right)\times 50")

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
    st.caption("The map is the original thesis figure. The site selector and weighting experiment are interactive; exact clickable geographic polygons require the original GIS boundaries or site-coordinate data.")

elif page == "Algeria's energy system":
    st.header("Algeria's energy system")
    st.metric("2050 final energy demand", "908.72 TWh/year")
    st.info("Detailed generation mix, installed capacities, storage and energy-balance results will be populated from the final thesis tables. Final energy demand must not be confused with total electricity generation.")


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
    with st.expander("Important thesis data notes"):
        st.warning("The thesis reports base-scenario total electricity generation as 2,134.33 TWh in Table 9 but 2,177.83 TWh in the later narrative. For electricity exports, Table 10 reports 3,075.33 TWh while the later narrative reports 3,179.58 TWh. These differences are flagged rather than reconciled.")
        st.warning("Battery and gas storage values are transcribed from the thesis storage discussion and scenario tables. Where table and narrative figures differ, they should be interpreted with their source context; older workbooks are not used to overwrite thesis results.")
    st.caption("Sources: thesis Tables 9–18 and Section 4.2, approximately pp. 78–95.")

elif page == "Five-scenario comparison":
    st.header("Five-scenario comparison")
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
    st.dataframe(comparison, hide_index=True, use_container_width=True)
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

    st.subheader("E-methane export — supplementary pipeline capacity note")
    st.write("The thesis assumes that existing natural gas infrastructure can be used to transport e-methane without additional transport investment. A supplementary screening check compares the e-methane export target with the nominal Algeria–Europe pipeline capacity figures used in the thesis.")
    capacity_view = pd.DataFrame([
        {"Indicator":"TransMed nominal capacity (thesis reference)","Value":"33.5 bcm/year"},
        {"Indicator":"Medgaz nominal capacity (thesis reference)","Value":"12.0 bcm/year"},
        {"Indicator":"Combined nominal capacity","Value":"45.5 bcm/year"},
        {"Indicator":"Energy conversion used in thesis hydrogen pipeline table","Value":"10 TWh per bcm"},
        {"Indicator":"Indicative combined energy capacity","Value":"455 TWh/year"},
        {"Indicator":"Thesis e-methane export target","Value":"574 TWh/year"},
        {"Indicator":"Indicative additional capacity required","Value":"119 TWh/year (11.9 bcm/year)"},
    ])
    st.dataframe(capacity_view, hide_index=True, use_container_width=True)
    st.warning("This is a supplementary capacity-screening calculation, not a pipeline engineering study. The 45.5 bcm/year is nominal combined capacity, not necessarily capacity available exclusively for e-methane: conventional natural gas exports may already use part of it. Meeting the full 574 TWh/year target may therefore require expansion of existing pipelines, new transport infrastructure, or reallocation of existing flows. The thesis's reported e-methane revenue, costs, net profit and LCOX are retained unchanged and should be read under the original transport assumption.")
    st.caption("Basis: thesis pipeline capacity figures for TransMed and Medgaz and the thesis's 10 TWh/bcm conversion scale; the 119 TWh/year shortfall is a supplementary arithmetic comparison, not a revised thesis result.")

elif page == "Social assessment":
    st.header("Social assessment")
    se = load_data("social_environment.json")
    emp = pd.DataFrame(se["employment"])
    st.write("The thesis estimates employment across the domestic base and three export pathways. Permanent jobs and temporary job-years are shown separately because they represent different types and durations of employment.")
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
