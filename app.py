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
sites = pd.DataFrame(load_data("siting_sites.json"))

st.title("Algeria Energy Transition Explorer")
st.caption("An interactive presentation of the findings of *Powering EU? — Energy scenarios for exporting electricity, green hydrogen and e-methane from Algeria to Europe* (Menakh, 2025).")
st.caption(
    "Interpretation note: thesis scenario results, modelled estimates and potential co-benefits "
    "are projections or analytical estimates, not observed or guaranteed outcomes. Their "
    "realisation depends on implementation, infrastructure delivery and relevant enabling conditions."
)

pages = [
    "Research overview", "Renewable energy siting", "Technical assessment",
    "Social assessment", "Environmental assessment", "Scenario comparison",
    "Interactive scenario explorer", "Methodology and sources",
    "Thesis limitations and critical considerations", "Future development"
]
page = st.sidebar.radio("Research modules", pages)

if page == "Research overview":
    st.header("Research overview")
    st.write(
        "This dashboard presents the findings of Imadeddine Menakh's 2025 master's thesis, "
        "*Powering EU? — Energy scenarios for exporting electricity, green hydrogen and "
        "e-methane from Algeria to Europe*. The thesis investigates how Algeria could "
        "transition towards a 100% renewable energy system by 2050 while potentially "
        "supplying energy to Europe through three export pathways."
    )
    st.markdown("**Download the full master's thesis:** [Powering EU? — LUT Research Portal](https://lutpub.lut.fi/handle/10024/170205)")

    st.subheader("Research objective")
    st.write(
        "The research compares a domestic renewable-energy pathway with three "
        "export-oriented pathways. It assesses their energy-system configurations and "
        "considers their technical, economic, social and environmental implications."
    )
    st.write(
        "The five energy-system scenarios were simulated using EnergyPLAN 16.3. The "
        "model was used to examine system operation, energy balances, generation, "
        "storage, costs and emissions under the thesis's scenario assumptions."
    )

    st.subheader("Research questions")
    st.write("To achieve its objectives, the thesis investigates three main research questions:")
    st.markdown(
        "**1. Technical potential and infrastructure**  \n"
        "What is the potential for Algeria to export renewable electricity, green hydrogen "
        "and e-methane to Europe, and what are the key technical and infrastructural "
        "requirements for enabling these exports?"
    )
    st.markdown(
        "**2. Economic competitiveness**  \n"
        "How do the economic costs and benefits of exporting these renewable energy "
        "carriers compare with one another and with Algeria's current fossil-fuel-based "
        "export system?"
    )
    st.markdown(
        "**3. Social and environmental benefits**  \n"
        "What are the potential social and environmental benefits of transitioning to "
        "renewable energy exports for Algeria's local communities and broader society?"
    )

    st.subheader("Four dimensions considered in the research")
    st.write(
        "The thesis approaches these questions by evaluating the different pathways "
        "across four complementary dimensions:"
    )
    cols = st.columns(4)
    dimensions = [
        ("Technical", "Energy-system configuration, renewable generation, storage, energy balances and export infrastructure."),
        ("Economic", "Investment and system costs, export revenues, profitability and levelised cost of export (LCOX)."),
        ("Social", "Employment, water access, regional equity and socioeconomic development."),
        ("Environmental", "Land requirements, energy-related water demand and emissions."),
    ]
    for col, (name, description) in zip(cols, dimensions):
        with col:
            st.markdown(f"**{name}**")
            st.write(description)

    st.subheader("The five scenarios and their purpose")
    st.write(
        "The thesis examines five scenarios to compare Algeria's existing energy system "
        "with different possible configurations for 2050."
    )
    scenarios = [
        ("Algeria 2019 — Baseline", "Represents the existing energy system and provides the reference point for the transition scenarios.", "Domestic final demand: 465.95 TWh/year", None),
        ("2050 — Domestic Base", "A 100% renewable system designed to meet Algeria's projected domestic demand, without an additional export pathway.", "Domestic final demand: 908.72 TWh/year", None),
        ("2050 — Electricity Export", "Meets domestic demand while exporting electricity to Europe through HVDC interconnections.", "Domestic demand: 908.72 TWh/year", "Planned export: 640 TWh/year"),
        ("2050 — Green Hydrogen Export", "Produces green hydrogen using renewable electricity alongside domestic energy supply.", "Domestic demand: 908.72 TWh/year", "Planned export: 662 TWh/year"),
        ("2050 — E-methane Export", "Produces synthetic methane using renewable hydrogen and captured CO₂ alongside domestic energy supply.", "Domestic demand: 908.72 TWh/year", "Planned export: 574 TWh/year"),
    ]
    scenario_cols = st.columns(5)
    for col, (name, purpose, domestic_demand, export_volume) in zip(scenario_cols, scenarios):
        with col:
            st.markdown(f"**{name}**")
            st.caption(purpose)
            st.markdown(f"`{domestic_demand}`")
            if export_volume:
                st.markdown(f"**{export_volume}**")
            elif name == "2050 — Domestic Base":
                st.caption("No energy-export pathway")
    st.info(
        "The four 2050 scenarios share the same projected domestic final energy demand "
        "of 908.72 TWh/year. Export production is additional to that domestic requirement. "
        "Domestic final energy demand must not be confused with total electricity generation "
        "or export production. Source: thesis Table 6, p. 63."
    )

    st.subheader("How to navigate the dashboard")
    st.write(
        "The following sections examine the research questions through the thesis's "
        "technical, economic, social and environmental findings. The scenario comparison "
        "brings the different pathways together, while the Interactive Scenario Explorer "
        "allows users to investigate selected assumptions and sensitivities."
    )
    st.caption(
        "Throughout the dashboard, thesis-reported findings are distinguished from "
        "additional calculations, interpretations and interactive sensitivities."
    )

elif page == "Renewable energy siting":
    st.header("Renewable energy siting assessment")
    st.write("The thesis applies a two-step process: preliminary spatial filtering, followed by a multi-criteria suitability assessment (MCDA).")

    st.subheader("Step 1 — Candidate development zones")
    st.write("The thesis manually delineates four large candidate zones after excluding mountainous and steep-slope areas, high-density urban zones, northern Algeria, small or isolated areas and protected regions.")
    map_path = Path(__file__).parent / "assets" / "thesis_site_selection_map.png"
    map_left, map_right = st.columns(2)
    with map_left:
        if map_path.exists():
            st.image(str(map_path), caption="Thesis Figure 2.1: Renewable energy development zones in Algeria (2050).", use_container_width=True)
        else:
            st.warning("The thesis site-selection map image was not found in the assets folder.")
    with map_right:
        render_site_admin_map()

    st.caption("The 58-wilaya map is an administrative reference showing wilayas named in Appendix 2; it does not reproduce the exact manually delineated candidate-zone polygons. The thesis does not provide precise GIS boundaries or coordinates for those zones.")
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
    st.caption("This is a direct weighted-score calculation using the thesis's fixed criterion scores; it is not an EnergyPLAN simulation. The published thesis totals and ranking remain unchanged. Appendix 2 weights sum to 2.00, and the published totals cannot be reconstructed exactly from the displayed table, so this explorer reports a separate weighted-average index on the original 50–100 score scale.")

    if st.button("Reset weights to thesis values", key="reset_siting_weights"):
        for i, item in criteria.iterrows():
            st.session_state[f"siting_weight_{i}"] = float(item["weight"])
        st.rerun()

    slider_panel, ranking_panel = st.columns([1.05, 1.25], gap="large")
    interactive_weights = []
    with slider_panel:
        st.markdown("**Adjust criterion weights**")
        for i, item in criteria.iterrows():
            value = st.slider(
                item["criterion"], min_value=0.0, max_value=0.5,
                value=float(item["weight"]), step=0.01,
                key=f"siting_weight_{i}", help=f"Original thesis weight: {item['weight']:.2f}. {item['direction']}"
            )
            interactive_weights.append(value)

    weight_total = sum(interactive_weights)
    with ranking_panel:
        st.markdown("**Live site ranking**")
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
            st.caption(f"Adjustable weight total: {weight_total:.2f}. The weighted-average calculation proportionally normalises the selected weights; original thesis weights remain unchanged.")
            st.dataframe(result[["site", "region", "Thesis rank", "Interactive weighted index", "Interactive rank"]].round({"Interactive weighted index":2}), hide_index=True, use_container_width=True)
            chart = px.bar(result, x="site", y="Interactive weighted index", color="Interactive rank", text="Interactive rank", title="Current ranking", labels={"site":"Candidate site", "Interactive weighted index":"Weighted index (50–100)", "Interactive rank":"New rank"})
            chart.update_traces(textposition="outside")
            chart.update_yaxes(range=[45,105])
            st.plotly_chart(chart, use_container_width=True)
            winner = result.iloc[0]
            st.success(f"Currently ranked first: {winner['site']} ({winner['Interactive weighted index']:.2f}).")

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
    st.info("The technical system configurations and energy balances presented here are based on EnergyPLAN 16.3 scenario simulations. The renewable-energy siting MCDA and social employment calculations are separate assessments and are not EnergyPLAN outputs.")
    st.subheader("Scenario configuration")
    st.dataframe(tech_df[["name", "wind_MW", "pv_MW", "wind_TWh", "pv_TWh", "electrolyser_MW", "co2_tph", "export"]].rename(columns={
        "name":"Scenario","wind_MW":"Wind capacity (MW)","pv_MW":"PV capacity (MW)",
        "wind_TWh":"Wind generation (TWh/year)","pv_TWh":"PV generation (TWh/year)",
        "electrolyser_MW":"Electrolysers (MW)","co2_tph":"CO₂ capture (tonnes/hour)","export":"Export target"
    }), hide_index=True, use_container_width=True)
    st.subheader("Installed wind and solar capacity")
    cap = tech_df.melt(id_vars="name",value_vars=["wind_MW","pv_MW"],var_name="Technology",value_name="Capacity (MW)")
    cap["Technology"] = cap["Technology"].map({"wind_MW":"Onshore wind","pv_MW":"Solar PV"})
    st.plotly_chart(px.bar(cap,x="name",y="Capacity (MW)",color="Technology",barmode="group",title="Installed generation capacity"),use_container_width=True)
    st.subheader("Annual wind and solar generation")
    gen = tech_df.melt(id_vars="name",value_vars=["wind_TWh","pv_TWh"],var_name="Technology",value_name="Generation (TWh/year)")
    gen["Technology"] = gen["Technology"].map({"wind_TWh":"Onshore wind","pv_TWh":"Solar PV"})
    st.plotly_chart(px.bar(gen,x="name",y="Generation (TWh/year)",color="Technology",barmode="group",title="Wind and PV generation"),use_container_width=True)
    st.write(
        f"For the electricity-export pathway, the thesis models {tech['notes']['electricity_export_input_TWh']} TWh/year entering the export chain. It assumes {tech['notes']['electricity_export_losses_TWh']} TWh/year of losses, leaving {tech['notes']['electricity_export_net_TWh']} TWh/year delivered. Flexible demand is estimated at {tech['notes']['flexible_demand_TWh']} TWh/year."
    )
    with st.expander("Electricity HVDC routes — thesis Tables 15–16"):
        st.dataframe(pd.DataFrame(tech["hvdc"]),hide_index=True,use_container_width=True)
    with st.expander("Hydrogen pipeline routes — thesis Table 18"):
        st.dataframe(pd.DataFrame(tech["hydrogen_routes"]),hide_index=True,use_container_width=True)
    st.caption("Sources: thesis Tables 9–18 and Section 4.2, approximately pp. 78–95.")

elif page == "Scenario comparison":
    st.header("Scenario comparison — synthesis of the assessment")
    st.write("This section brings together the findings presented in the Technical, Social and Environmental Assessments. It is intended as a concluding synthesis: some indicators reappear here so that the five scenarios and three export pathways can be compared directly.")
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
                "Technical — hydrogen storage (GWh)": "Not reported",
                "Technical — gas storage (GWh)": "Not reported",
                "Technical — CEEP (TWh/year)": 0,
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
            "Technical — hydrogen storage (GWh)": t.get("hydrogen_GWh", "Not reported"),
            "Technical — gas storage (GWh)": t.get("gas_GWh", "Not reported"),
            "Technical — CEEP (TWh/year)": {
                "2050 Domestic Base": 485.89,
                "2050 Electricity Export": 554.49,
                "2050 Green Hydrogen Export": 442.92,
                "2050 E-methane Export": 248.73,
            }.get(label, "Not reported"),
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
    st.write("The technical comparison brings together annual generation, storage requirements and critical excess electricity production (CEEP) across all four 2050 configurations.")
    if not tech_df.empty:
        gen = tech_df[["name", "wind_TWh", "pv_TWh"]].melt(id_vars="name", var_name="Technology", value_name="Generation (TWh/year)")
        gen["Technology"] = gen["Technology"].map({"wind_TWh":"Wind", "pv_TWh":"Solar PV"})
        st.plotly_chart(px.bar(gen, x="name", y="Generation (TWh/year)", color="Technology", barmode="group", title="Annual wind and PV generation — 2050 scenarios"), use_container_width=True)
        storage_df = tech_df[["name", "battery_GWh", "hydrogen_GWh", "gas_GWh"]].rename(columns={"name":"2050 scenario", "battery_GWh":"Battery storage (GWh)", "hydrogen_GWh":"Hydrogen storage (GWh)", "gas_GWh":"Gas storage (GWh)"})
        st.markdown("**Storage requirements across all 2050 scenarios**")
        st.dataframe(storage_df, hide_index=True, use_container_width=True)
        storage_long = storage_df.melt(id_vars="2050 scenario", var_name="Storage type", value_name="Storage (GWh)")
        st.plotly_chart(px.bar(storage_long, x="2050 scenario", y="Storage (GWh)", color="Storage type", barmode="group", title="Storage requirements by technology — 2050 scenarios"), use_container_width=True)
        ceep_df = pd.DataFrame([
            {"Scenario":"2019 baseline", "CEEP (TWh/year)":0.0},
            {"Scenario":"2050 Domestic Base", "CEEP (TWh/year)":485.89},
            {"Scenario":"2050 Electricity Export", "CEEP (TWh/year)":554.49},
            {"Scenario":"2050 Green Hydrogen Export", "CEEP (TWh/year)":442.92},
            {"Scenario":"2050 E-methane Export", "CEEP (TWh/year)":248.73},
        ])
        st.markdown("**Critical excess electricity production (CEEP)**")
        st.dataframe(ceep_df, hide_index=True, use_container_width=True)
        st.plotly_chart(px.bar(ceep_df, x="Scenario", y="CEEP (TWh/year)", title="Annual critical excess electricity production across all scenarios"), use_container_width=True)
        st.caption("CEEP is electricity generated from wind or solar PV that cannot be consumed or stored at the time of production and is curtailed. The 2050 values are reported in the thesis's discussion accompanying Figure 29 (pp. 95–96); 2019 CEEP is reported as zero.")

    st.subheader("Economic dimension — export pathway comparison")
    st.write(
        "Economic indicators are available for the three export pathways. The domestic "
        "baseline and domestic-base scenarios do not generate export revenue or export profit."
    )
    economic_detail = exports[[
        "scenario", "export_volume_TWh_year", "market_price_EUR_MWh",
        "annual_revenue_EUR_bn", "annual_export_cost_for_profit_EUR_bn",
        "reported_net_profit_EUR_bn", "incremental_system_cost_for_LCOX_EUR_bn",
        "LCOX_EUR_MWh"
    ]].rename(columns={
        "scenario": "Export pathway",
        "export_volume_TWh_year": "Delivered exports (TWh/year)",
        "market_price_EUR_MWh": "Market price (€/MWh)",
        "annual_revenue_EUR_bn": "Revenue (€bn/year)",
        "annual_export_cost_for_profit_EUR_bn": "Cost used for reported profit (€bn/year)",
        "reported_net_profit_EUR_bn": "Reported net profit (€bn/year)",
        "incremental_system_cost_for_LCOX_EUR_bn": "Incremental system cost for LCOX (€bn/year)",
        "LCOX_EUR_MWh": "LCOX (€/MWh)"
    })
    st.dataframe(economic_detail, hide_index=True, use_container_width=True)
    econ_chart_left, econ_chart_right = st.columns(2)
    with econ_chart_left:
        st.plotly_chart(
            px.bar(exports, x="scenario", y="annual_revenue_EUR_bn",
                   title="Annual export revenue",
                   labels={"scenario": "Export pathway", "annual_revenue_EUR_bn": "€bn/year"}),
            use_container_width=True
        )
    with econ_chart_right:
        st.plotly_chart(
            px.bar(exports, x="scenario", y="LCOX_EUR_MWh",
                   title="Levelised cost of export (LCOX)",
                   labels={"scenario": "Export pathway", "LCOX_EUR_MWh": "€/MWh"}),
            use_container_width=True
        )
    with st.expander("How to interpret export costs, profit and LCOX"):
        st.write(
            "The thesis uses two different cost calculations. The export cost used in the "
            "reported net-profit calculation is not the same as the incremental system cost "
            "used to calculate LCOX. They should not be treated as interchangeable."
        )
        st.write(
            "Incremental export system cost = total export-scenario system cost − total "
            "domestic-base-scenario system cost."
        )
        st.write("LCOX = incremental annual system cost ÷ net annual export energy delivered.")
        st.caption(
            "The final thesis is the authoritative source for published results. Supporting "
            "workbooks help explain calculations and discrepancies; they do not silently "
            "overwrite thesis values."
        )

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
    st.write(
        "The thesis examines the potential social benefits of the 2050 energy transition, "
        "with particular attention to employment, domestic energy and water access, and "
        "regional development. Employment figures and 2050 access indicators are thesis-based "
        "estimates or scenario assumptions, not observed outcomes."
    )

    se = load_data("social_environment.json")
    emp = pd.DataFrame(se["employment"])

    st.subheader("Employment impacts across the 2050 scenarios")
    st.write(
        "The employment figures are modelled estimates based on technology-specific "
        "employment factors, investment assumptions and adjustment multipliers. They "
        "are not observed employment statistics or guaranteed job outcomes."
    )
    st.write(
        "The thesis distinguishes between permanent employment, measured in jobs, and "
        "temporary employment, measured in job-years. Permanent jobs are ongoing positions "
        "associated with operation and maintenance, fuel supply and desalination. Temporary "
        "job-years are associated mainly with construction and installation, manufacturing, "
        "and electricity and water transmission infrastructure."
    )

    employment_left, employment_right = st.columns(2, gap="large")
    with employment_left:
        st.markdown("**Permanent employment — jobs**")
        st.plotly_chart(
            px.bar(
                emp, x="scenario", y="permanent_jobs",
                labels={"scenario": "2050 scenario", "permanent_jobs": "Permanent employment (jobs)"},
                title="Estimated permanent employment"
            ),
            use_container_width=True
        )
    with employment_right:
        st.markdown("**Temporary employment — job-years**")
        st.plotly_chart(
            px.bar(
                emp, x="scenario", y="temporary_job_years",
                labels={"scenario": "2050 scenario", "temporary_job_years": "Temporary employment (job-years)"},
                title="Estimated temporary employment"
            ),
            use_container_width=True
        )
    employment_table = emp[["scenario", "permanent_jobs", "temporary_job_years"]].rename(columns={
        "scenario": "2050 scenario", "permanent_jobs": "Permanent jobs", "temporary_job_years": "Temporary employment (job-years)"
    })
    st.dataframe(employment_table, hide_index=True, use_container_width=True)
    st.warning(
        "Permanent employment is counted as jobs, not jobs per year. Temporary employment "
        "is counted in job-years. A job-year represents one full-time job for one year; "
        "it is not the number of people employed simultaneously. These are modelled estimates, "
        "not observed or guaranteed employment outcomes."
    )

    with st.expander("How the thesis estimates employment"):
        method = se["employment_method"]
        st.write("**Permanent employment:** " + method["permanent_jobs"])
        st.write("**Temporary employment:** " + method["temporary_jobs"])
        st.write(
            "Adjustment factors: " + ", ".join(
                f"{k.replace('_', ' ')} = {v}" for k, v in method["adjustment_factors"].items()
            ) + "."
        )
        st.write(
            f"Desalination employment factor: {method['desalination_factor_jobs_per_million_m3_year']} "
            f"jobs per million m³/year. The thesis states that this relationship is valid up to "
            f"{method['desalination_factor_limit_million_m3_year']} million m³/year and cautions "
            "against extrapolating beyond that capacity."
        )
        st.write(
            f"HVDC transmission: {method['hvdc_jobs_per_billion_eur_investment']:,} jobs per €bn "
            f"of investment. Water infrastructure: "
            f"{method['water_infrastructure_jobs_per_million_usd_investment']} jobs per US$ million "
            "of investment."
        )

    st.subheader("Water stress: the challenge and the 2050 scenario")
    st.write(
        "Figure 12 presents the projected water-stress challenge if substantial interventions "
        "are not implemented. The thesis discusses projections that more than 80% of Algeria's "
        "population could be exposed to extremely high water stress by 2050. This is a "
        "business-as-usual risk projection, not the outcome of the thesis's proposed 2050 "
        "transition scenarios."
    )
    figure12_url = (
        "https://files.wri.org/d8/s3fs-public/styles/1575_wide/s3/2023-08/"
        "23-08-02-aqueduct-4.0-launch-global-countries-baseline_Insights.png"
        "?VersionId=6gfns6C.Haz3iMYrsS3mTgLWULJEkixl&itok=nRnW6572"
    )
    st.image(
        figure12_url,
        caption="Figure 12. Baseline water stress by country. Source: World Resources Institute (WRI), Aqueduct 4.0 (2023).",
        use_container_width=True
    )
    st.markdown(
        "Source: [World Resources Institute – 25 Countries Face Extremely High Water Stress](https://www.wri.org/insights/highest-water-stressed-countries)"
    )

    st.write(
        "By contrast, the thesis's four 2050 transition scenarios assume the development of "
        "the domestic energy and water system, including water-supply infrastructure. Under "
        "these scenario assumptions, the water-stressed population indicator falls to 0%, "
        "water access reaches 100%, and water availability reaches 1,000 m³ per capita per year."
    )
    st.caption(
        "The more-than-80% figure describes the projected risk without the required interventions; "
        "the 0% figure is the thesis's outcome under its proposed 2050 scenario assumptions. "
        "They describe different future conditions and should not be read as contradictory estimates."
    )

    st.subheader("Projected changes in domestic energy and water access")
    access_table = pd.DataFrame([
        ["Electricity access", "100%", "100%"],
        ["Electricity per capita", "1,884 kWh/year", "5,934 kWh/year"],
        ["Renewable share of energy mix", "0.27%", "100%"],
        ["Final energy use per capita", "10,737 kWh/year", "14,916 kWh/year"],
        ["Water-stressed population", "40%", "0%"],
        ["Water availability per capita", "282 m³/year", "1,000 m³/year"],
        ["Water access", "70.6%", "100%"],
    ], columns=["Indicator", "2023 reference", "2050 transition scenarios"])
    st.dataframe(access_table, hide_index=True, use_container_width=True)
    st.caption(
        "Adapted from the thesis's Table 22. The 2050 domestic energy and water-access "
        "indicators apply across all four 2050 scenarios, which share the same domestic "
        "system foundation. The scenarios differ in the additional energy-export pathway "
        "and the infrastructure and resources required to support it. Baseline indicators "
        "are drawn from the sources and reference years cited in the thesis."
    )

    w = se["water_access"]
    a, b, c = st.columns(3)
    a.metric(
        "Water availability per capita by 2050",
        f"{w['water_per_capita_2050_m3_year']:,} m³/person/year",
        f"from {w['water_per_capita_current_m3_year']} m³/person/year"
    )
    b.metric(
        "National water-access target",
        f"{w['water_access_2050_percent']}%",
        f"from {w['water_access_current_percent']}% in {w['current_reference_year']}"
    )
    c.metric("Planned water pipelines", f">{w['planned_water_pipeline_km']:,} km")

    st.subheader("Water infrastructure and regional access")
    st.write(
        "The thesis considers a combination of water infrastructure, including desalination "
        "facilities, dams and transmission pipelines. The planned pipeline network is intended "
        "to move water from production and storage areas towards inland and southern regions. "
        "Desalination is an important component of the proposed system, but it is not the only "
        "source of water supply."
    )
    st.caption(
        "The access and availability figures are 2050 scenario targets or projections, not "
        "achieved outcomes. The thesis discusses water access in southern regions separately "
        "from its national indicators. In that regional discussion, current safe-water access "
        "is described as around 70%. This is a differently framed regional statement and "
        "should not be treated as the same measurement as the 70.6% national comparison above."
    )

    st.info(
        "The thesis also cites a projected decline of around 20% in national rainfall by 2050. "
        "Together with the projection that more than 80% of the population could face water "
        "stress without substantial intervention, this describes the future water-security "
        "challenge—not a measured outcome or the result of the proposed transition scenarios."
    )

    st.subheader("Potential benefits for southern Algeria")
    st.write(
        "The thesis argues that improved water and electricity services, together with major "
        "infrastructure investment, could support more balanced regional development. It notes "
        "that electricity access is already close to universal nationally, but that supply quality "
        "and reliability remain concerns in some southern areas."
    )
    st.markdown("""
    **Potential benefits discussed in the thesis**
    - More reliable water supplies for households in remote and underserved areas.
    - Better conditions for local agriculture and livestock activities.
    - Support for new population centres and a more balanced distribution of economic activity.
    - Improved logistics, lower transport costs and the development of local economic hubs.
    - Potential improvements in public services, including education and healthcare, and opportunities for tourism and hospitality.
    - Vocational training and local workforce development linked to the emerging renewable-energy sector.
    """)
    st.subheader("Implementation considerations")
    st.warning(
        "If desalination, dams and water-transmission infrastructure are delayed or do not reach "
        "the intended areas, some southern communities may remain dependent on groundwater. "
        "This could increase pressure on local aquifers and limit the expected improvements in "
        "water security."
    )

elif page == "Environmental assessment":
    st.header("Environmental assessment")
    se = load_data("social_environment.json")
    st.write(
        "This section examines environmental pressures associated with the energy-system "
        "pathways: water demand for energy production, land required for solar PV deployment "
        "and the emissions results reported by the thesis. Household water access and regional "
        "water security are discussed in the Social Assessment."
    )

    st.subheader("1. Water demand across the 2050 scenarios")
    water = pd.DataFrame(se["water_demand"])
    water_display = water.rename(columns={
        "scenario": "Scenario",
        "non_energy_use_Gm3_year": "Non-energy use (Gm³/year)",
        "hydrogen_production_water_Gm3_year": "Hydrogen production (Gm³/year)",
        "pv_wind_operations_water_Gm3_year": "PV/wind operations (Gm³/year)",
        "total_water_demand_Gm3_year": "Total demand (Gm³/year)"
    })
    st.dataframe(water_display, hide_index=True, use_container_width=True)
    st.plotly_chart(
        px.bar(water, x="scenario", y="total_water_demand_Gm3_year",
               title="Total water demand by scenario",
               labels={"scenario": "2050 scenario", "total_water_demand_Gm3_year": "Water demand (Gm³/year)"}),
        use_container_width=True
    )
    st.caption(
        "Values are transcribed from thesis Table 13. The source table also contains energy-use "
        "rows expressed in TWh; these are not water volumes and are excluded from this comparison. "
        "The figures distinguish water used for non-energy purposes, hydrogen production and PV/wind operations."
    )

    st.subheader("2. Estimated solar PV land requirements")
    land = pd.DataFrame(se["solar_land_use"])
    land_display = land.rename(columns={
        "scenario": "Scenario", "pv_generation_GWh_year": "PV generation (GWh/year)",
        "land_km2": "Estimated PV land (km²)",
        "share_site_02_percent": "Share of Site 02 (%)",
        "share_national_area_percent": "Share of national area (%)"
    })
    st.dataframe(land_display, hide_index=True, use_container_width=True)
    st.plotly_chart(
        px.bar(land, x="scenario", y="land_km2",
               title="Estimated land required for solar PV",
               labels={"scenario": "2050 scenario", "land_km2": "Estimated PV land (km²)"}),
        use_container_width=True
    )
    st.write(
        "The estimated land requirement increases with the scale of solar PV generation in each "
        "pathway. The thesis discusses the use of agrivoltaics as one possible way to combine "
        "solar deployment with selected land uses."
    )
    st.caption(
        "The thesis estimates PV land using 211.64 GWh/km²/year, based on 20% panel efficiency, "
        "0.84 system efficiency, 0.24 capacity factor and 0.6 ground coverage ratio. This is a "
        "PV land estimate, not the complete land or ecological footprint of all energy and export infrastructure."
    )
    st.write(
        "The thesis characterises Site 02 as sparsely populated and having low ecological "
        "activity. Nevertheless, large-scale land occupation may affect grazing, mobility, "
        "local livelihoods and cultural practices. These potential impacts require local "
        "consultation and fair benefit-sharing; the site description should not be read as "
        "evidence that the land is without social or environmental value."
    )

    st.subheader("3. CO₂ emissions reported in the thesis")
    em = se["emissions"]
    a, b, c = st.columns(3)
    a.metric("Domestic energy — 2019", f"{em['domestic_2019']:.2f} Mt")
    b.metric("Domestic energy — 2050", f"{em['domestic_2050_all_scenarios']:.0f} Mt", "All modelled 2050 scenarios")
    c.metric("E-methane export balance — 2050", f"{em['including_exports_2050']['E-methane Export']:.2f} Mt")
    st.write(
        "Including exports, the thesis reports 284.67 Mt CO₂ in 2019, zero for the electricity "
        "and green-hydrogen export scenarios in 2050, and −116.18 Mt for the e-methane export scenario."
    )
    st.warning(
        "The negative e-methane result reflects the thesis's accounting treatment of captured CO₂ "
        "allocated to importing countries. It should not be interpreted as independently verified, "
        "full life-cycle net-negative emissions. Methane leakage and other non-CO₂ greenhouse-gas "
        "emissions also remain relevant."
    )
    st.warning(em["non_co2_note"])

    st.subheader("4. Scope and environmental limitations")
    st.write(
        "The indicators above should be read within the boundaries of the thesis assessment. "
        "The PV land figures do not represent the full footprint of transmission lines, storage, "
        "conversion facilities or other infrastructure. Likewise, the reported emissions results "
        "do not by themselves establish that every pathway has zero life-cycle greenhouse-gas emissions."
    )
    with st.expander("Additional environmental data and interpretation notes"):
        for item in se["limitations"]:
            st.write("• " + item)
        st.caption(
            "These notes combine qualifications stated in the thesis with clarifications "
            "made when interpreting and presenting its data. They should not all be read "
            "as limitations explicitly identified by the thesis author."
        )

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
    st.write(
        "This section explains how the thesis developed its five energy-system scenarios, "
        "which modelling tools and data sources it used, and how the dashboard organises "
        "the resulting technical, economic, social and environmental evidence. The "
        "description below follows the thesis methodology and appendices."
    )

    st.subheader("1. Research design and scenario framework")
    st.write(
        "The thesis compares Algeria's actual 2019 energy system with four 2050 pathways: "
        "a domestic renewable-energy base case and three export-oriented pathways based "
        "on electricity, green hydrogen and e-methane. The export pathways use solar and "
        "wind as their primary renewable energy sources and differ mainly in the energy "
        "carrier and export infrastructure considered."
    )
    st.info(
        "The 2019 case is the historical reference. The 2050 cases are modelled scenarios "
        "based on projected demand and stated assumptions; they are not observations or "
        "guaranteed forecasts."
    )

    st.subheader("2. Energy-system modelling and input data")
    method_rows = [
        {"Tool or source": "EnergyPLAN 16.3", "Role described in the thesis": "Hourly energy-system simulation for the 2019 baseline and 2050 domestic and export scenarios; used to assess system operation, energy balances, costs and emissions."},
        {"Tool or source": "LUT-DEMAND model", "Role described in the thesis": "Projection of 2050 domestic energy demand, including sectoral demand and hourly demand profiles informed by population, climate and sectoral activity."},
        {"Tool or source": "PVGIS", "Role described in the thesis": "Generation of hourly solar photovoltaic potential profiles."},
        {"Tool or source": "IEA energy statistics and Algerian national statistics", "Role described in the thesis": "Main inputs for the 2019 energy balance, complemented by national statistical publications."},
        {"Tool or source": "Published studies and network-planning material", "Role described in the thesis": "Evidence used to frame potential European demand, export volumes, transmission routes and export infrastructure assumptions."},
        {"Tool or source": "EnergyPLAN default parameters and cited cost methodology", "Role described in the thesis": "Technology efficiencies and the general cost structure, including the cost methodology attributed to Gulagi et al. (2017)."},
    ]
    st.dataframe(pd.DataFrame(method_rows), hide_index=True, use_container_width=True)
    st.caption(
        "The thesis identifies IEA energy statistics (2022) and Algerian national statistics "
        "for the 2019 energy balance; LUT-DEMAND (Keiner et al., 2023) for demand projections "
        "and profiles; and PVGIS for hourly PV potential profiles. Specific export assumptions "
        "draw on the studies cited in the thesis, including Benasla et al. (2024), Neumann et "
        "al. (2024), Gatzen et al. (2024) and related infrastructure studies."
    )

    st.subheader("3. Assessment methods used in the thesis")
    assessment_rows = [
        {"Assessment": "Technical", "Approach presented": "EnergyPLAN scenario outputs are used to examine generation, demand, storage, energy balances, excess electricity and export-system requirements."},
        {"Assessment": "Economic", "Approach presented": "The thesis assesses infrastructure investment, system costs, export revenues, reported net profit and levelised cost of export (LCOX). Net-profit cost and incremental system cost used for LCOX are distinct calculations."},
        {"Assessment": "Renewable-energy siting", "Approach presented": "A two-step process: preliminary spatial filtering followed by a multi-criteria assessment of four candidate zones using 14 indicators, criterion weights and Min–Max scoring on a 50–100 scale."},
        {"Assessment": "Social", "Approach presented": "Employment impacts are estimated using technology- and investment-related employment factors and adjustment assumptions; water access and regional development are discussed as potential social implications."},
        {"Assessment": "Environmental", "Approach presented": "The thesis examines energy-related water demand, estimated PV land requirements and reported CO₂/CO₂-equivalent emissions across the scenarios."},
    ]
    st.dataframe(pd.DataFrame(assessment_rows), hide_index=True, use_container_width=True)

    st.subheader("4. Where to find the supporting methodology")
    references = [
        ("Main methodology", "Chapter 3 — scenario design, site selection and EnergyPLAN modelling."),
        ("Scenario inputs and technical/economic parameters", "Appendix 1 — scenario data, technology parameters and infrastructure details."),
        ("Renewable-energy siting", "Appendix 2 — site-selection methodology, criteria, weights and raw scoring data; see Tables 2.1 and 2.2 and Figure 2.1."),
        ("Employment estimation", "Appendix 3 — employment impact estimation methodology and assumptions."),
        ("Scenario results", "Chapter 4 and the associated results tables, including the energy-system, water-demand, infrastructure, LCOX, employment and emissions results."),
    ]
    for heading, detail in references:
        st.markdown(f"**{heading}**  \
{detail}")

    st.subheader("5. Source hierarchy used by this dashboard")
    st.markdown("""
    1. **Final 2025 master's thesis** — the primary reference for published scenario results, reported values and the author's stated methodology.
    2. **Supporting Excel workbooks and EnergyPLAN scenario files** — used to inspect detailed inputs and calculations, and to help investigate discrepancies where available.
    3. **Earlier working files and intermediate calculations** — treated as development records rather than as replacements for the final thesis.
    """)
    st.warning(
        "Where a supporting workbook differs from the final thesis, the dashboard retains "
        "the thesis-reported value as its primary reference unless a specific correction has "
        "been established and explained. Discrepancies are flagged rather than silently "
        "reconciled. Interactive calculations in this dashboard are identified separately "
        "and do not constitute a new EnergyPLAN simulation."
    )
    st.caption(
        "Primary reference: Imadeddine Menakh (2025), *Powering EU? – Energy scenarios "
        "for exporting electricity, green hydrogen and e-methane from Algeria to Europe*. "
        "Tool versions, assumptions and source descriptions above reproduce the thesis "
        "methodology; they do not represent an independent validation of the underlying models."
    )

elif page == "Thesis limitations and critical considerations":
    st.header("Thesis limitations and critical considerations")
    st.write(
        "This section brings together broader methodological limitations and critical "
        "observations that affect how the thesis results should be interpreted. Detailed "
        "indicator-specific qualifications remain in the relevant Technical, Social and "
        "Environmental Assessment sections."
    )

    st.subheader("1. Modelling scope and scenario assumptions")
    st.markdown("""
    - The results are based on modelled 2050 scenarios and their underlying assumptions; they are not forecasts or proof that the proposed systems will be implemented as modelled.
    - Financial sensitivity calculations in this dashboard do not rerun EnergyPLAN and do not establish hourly system feasibility, operational performance or the ability to deliver the adjusted export volumes.
    - The thesis's cost-minimised configurations should be understood within the model's assumptions and boundaries, rather than as proof of a universally optimal or implementation-ready system.
    """)

    st.subheader("2. Export infrastructure and delivery assumptions")
    st.markdown("""
    - Export pathways depend on substantial electricity, hydrogen, gas, water and other supporting infrastructure. Planned or proposed infrastructure should not be confused with infrastructure that is already operational.
    - The thesis assumes that 50% of submarine infrastructure costs for the electricity and hydrogen pathways are allocated to Algeria, with the remaining 50% assumed to be financed by Italy and Spain. This is a modelling assumption, not a confirmed financing agreement.
    - The e-methane export volume should be considered alongside the operational capacity of the TransMed and Medgaz pipelines. The thesis's reported 574 TWh/year e-methane export volume is higher than their combined stated capacity of 455 TWh/year; the thesis does not include the additional pipeline capacity and investment that this difference would require in its e-methane economic assessment.
    - Proposed or inactive routes, including GALSI and MEG, should not be treated as operational export capacity in the current infrastructure assessment.
    """)

    st.subheader("3. Economic interpretation")
    st.markdown("""
    - Reported net profit and LCOX use different cost calculations. The export cost used for the net-profit calculation should not be confused with the incremental system cost used for LCOX.
    - The 50% submarine-cost allocation is an assumption about the share of specified submarine infrastructure costs; it does not mean that half of all export-system costs are financed by other countries.
    """)

    st.subheader("4. Renewable-energy siting and spatial precision")
    st.markdown("""
    - The four candidate zones are manually delineated reference areas. The thesis does not provide precise GIS polygons or coordinates that would support treating the displayed boundaries as surveyed project sites.
    - Site-to-wilaya associations are indicative. The map uses the historical 58-wilaya administrative reference to remain consistent with the thesis and should not be interpreted as a precise current administrative or cadastral boundary dataset.
    - The MCDA results depend on the selected criteria, scoring ranges and weights. The original criterion weights sum to 2.00 rather than 1.00; they are retained as importance coefficients and are not silently normalised. Some criteria also rely on simplifying assumptions, including distance-to-grid categories and historical rehabilitation potential scores.
    """)

    st.subheader("5. Social and environmental evidence")
    st.markdown("""
    - Employment, water-access, land-use and emissions indicators are modelled estimates, scenario targets or projections. Their interpretation and specific qualifications are explained in the Social and Environmental Assessment sections.
    - PV land estimates cover the estimated area for solar panels under the thesis assumptions; they do not represent the full spatial footprint or ecological effects of all associated infrastructure.
    - The thesis's negative e-methane emissions balance is an accounting result and should not be interpreted as independently verified full life-cycle net-negative emissions.
    """)

    st.subheader("6. Specific corrections and inconsistencies identified in the thesis")
    st.markdown("""
    **Figure 30 — Full-load-hours chart (thesis p. 98)**
    - The legend/key orientation should be reversed for clarity: the scenario labels (2019, 2050 Base, 2050 Electricity, 2050 Hydrogen and 2050 E-methane) should identify the series, while generation technologies should be listed along the category axis.

    **Table 22 — Energy and water access indicators (thesis p. 108)**
    - The table title should be clarified to match its contents. The dashboard uses: *Comparison of current and 2050 energy and water access indicators in Algeria*.

    **Table 9 and domestic-base generation narrative (thesis pp. 78 and 88)**
    - Table 9 reports **2,134.33 TWh**; the later narrative reports **2,177.83 TWh**.
    - The supporting EnergyPLAN workbook reports **2,173.20 TWh** and lists **38.88 TWh** of condensing generation. Adding that condensing contribution to the Table 9 figure gives approximately **2,173.21 TWh**, consistent with the workbook total within rounding. The narrative's **2,177.83 TWh** is still 4.63 TWh higher and cannot be confirmed as the reconciled total from the available supporting calculations.

    **Table 10 and electricity-export generation narrative (thesis pp. 79 and 88)**
    - Table 10 reports **3,075.33 TWh**; the later narrative reports **3,179.58 TWh**.
    - The supporting EnergyPLAN workbook reports **3,085.15 TWh** for the electricity-export scenario, including approximately **9.81 TWh** from condensing generation beyond the Table 10 figure. This is a workbook-derived total and is kept distinct from the two thesis-reported figures rather than silently replacing them.

    **Growth multiple in the electricity-export narrative (thesis p. 88)**
    - The narrative states a **39-fold** increase relative to 2019 generation of 81.52 TWh. Using the supporting-workbook total of 3,085.15 TWh gives approximately **37.84-fold**. The 39-fold figure follows from the narrative's 3,179.58 TWh value, not from the workbook total.
    """)
    st.caption("The supporting workbook is used here to investigate and explain the discrepancies; workbook-derived figures are not presented as if they were published thesis values. The dashboard keeps source provenance visible.")
    st.info(
        "Attribution note: this page separates modelling assumptions and limitations "
        "documented in the thesis from additional observations made during review of the "
        "thesis and its supporting material. Not every critical observation above is "
        "necessarily stated explicitly by the thesis author."
    )

elif page == "Future development":
    st.header("Future research directions")
    st.write(
        "The thesis identifies several directions for future research to strengthen the "
        "assessment of Algeria's renewable-energy transition and its potential role as an "
        "energy and low-carbon products supplier. The areas below follow those directions "
        "and add further research opportunities arising from the study's methods and scope."
    )

    st.subheader("1. Explore hybrid export strategies and alternative energy carriers")
    st.markdown("""
    - Assess combined export strategies that supply electricity, green hydrogen and e-methane in parallel or in blended forms.
    - Examine alternative energy carriers, including methanol and ammonia.
    - Investigate the technical, logistical and economic implications of transporting hydrogen by ship over long distances.
    """)

    st.subheader("2. Assess low-carbon industrial exports")
    st.markdown("""
    - Study opportunities to use Algeria's renewable-energy resources to produce and export low-carbon steel, cement, fertilisers and processed minerals.
    - Compare the value added, infrastructure needs, energy requirements and market conditions of these products with direct energy-carrier exports.
    """)

    st.subheader("3. Improve energy-system modelling and scenario coverage")
    st.markdown("""
    - Run additional EnergyPLAN scenarios for different export targets, including illustrative cases of 100 TWh/year and 1,000 TWh/year, before interpreting the financial sensitivity results as system-level outcomes.
    - Use alternative or complementary simulation tools to test system operation, flexibility, hourly balancing and infrastructure interactions.
    - Explore mixed-export scenarios and compare how combined export volumes affect generation, storage, curtailment, costs and domestic supply.
    - Examine the effects of future cost reductions in batteries, electrolysers, concentrated solar power (CSP) and carbon-capture systems.
    """)

    st.subheader("4. Improve spatial siting and infrastructure routing")
    st.markdown("""
    - Apply GIS-based land-suitability analysis using reproducible spatial criteria and georeferenced datasets, rather than relying primarily on visual interpretation of satellite imagery.
    - Evaluate several potential PV development areas instead of assuming that one candidate site represents the entire deployment.
    - Replace straight-line distance estimates with more realistic route assessments for electricity transmission and water infrastructure, accounting for terrain, land constraints, existing corridors and engineering requirements.
    - Obtain precise GIS boundaries and coordinates for candidate sites before presenting them as project-ready development zones.
    """)

    st.subheader("5. Strengthen environmental and lifecycle assessment")
    st.markdown("""
    - Investigate methane and hydrogen leakage, and associated emissions, throughout production, processing, storage and transport chains.
    - Examine the implications of subsidies, recycling and end-of-life management for the sustainability and affordability of renewable-energy technologies.
    - Apply transparent lifecycle boundaries to compare emissions and environmental impacts across export pathways and alternative products.
    """)

    st.subheader("6. Deepen economic, social and policy analysis")
    st.markdown("""
    - Assess how financing structures, subsidies, policy frameworks and international market conditions affect export competitiveness.
    - Improve regional evidence on employment, water access, land use and the distribution of costs and benefits.
    - Integrate economic, environmental, social and policy dimensions to support long-term decision-making about Algeria's energy transition.
    """)

    st.info(
        "These are proposed directions for further research. They are not results of the "
        "2025 thesis and are not features currently implemented in this dashboard."
    )

st.divider()
st.caption("Reference: Imadeddine Menakh (2025), *Powering EU? – Energy scenarios for exporting electricity, green hydrogen and e-methane from Algeria to Europe*.")
