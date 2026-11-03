import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Algeria Energy Transition Explorer",
    page_icon="⚡",
    layout="wide"
)

DATA_DIR = Path(__file__).parent / "data"

with (DATA_DIR / "export_scenarios.json").open(encoding="utf-8") as f:
    export_df = pd.DataFrame(json.load(f))

with (DATA_DIR / "siting_results.json").open(encoding="utf-8") as f:
    siting_df = pd.DataFrame(json.load(f))

st.title("Algeria Energy Transition Explorer")
st.caption("An interactive presentation of the findings of *Powering EU?* (2025)")

st.info(
    "The thesis is the primary reference for published results. Interactive "
    "sensitivities are shown separately and do not replace EnergyPLAN modelling."
)

pages = [
    "Research overview",
    "Four assessment dimensions",
    "Renewable energy siting",
    "Algeria's energy system",
    "Export scenarios",
    "Economic assessment",
    "Social assessment",
    "Environmental assessment",
    "Interactive scenario explorer",
    "Methodology and sources",
]
page = st.sidebar.radio("Research modules", pages)

if page == "Research overview":
    st.header("Research overview")
    st.write(
        "The thesis examines Algeria's transition from a fossil-based energy "
        "system towards renewable-based domestic supply and energy exports to "
        "Europe by 2050. Three export pathways are modelled: electricity via "
        "HVDC, green hydrogen and synthetic e-methane."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("2050 final energy demand", "908.72 TWh/year")
    c2.metric("Export pathways", "3")
    c3.metric("Energy-system model", "EnergyPLAN 16.3")

    st.subheader("The five scenarios studied")
    scenario_cols = st.columns(5)
    scenario_names = [
        ("2019 baseline", "Algeria's reference energy system"),
        ("2050 domestic", "100% renewable domestic system"),
        ("Electricity export", "HVDC electricity exports"),
        ("Hydrogen export", "Green hydrogen exports"),
        ("E-methane export", "Synthetic e-methane exports"),
    ]
    for col, (name, detail) in zip(scenario_cols, scenario_names):
        with col:
            st.markdown(f"**{name}**")
            st.caption(detail)

    st.subheader("An integrated assessment")
    st.write(
        "The thesis evaluates the export pathways across four complementary "
        "dimensions: technical feasibility, economic viability, environmental "
        "impact and social benefits."
    )
    st.markdown(
        "Use the navigation menu to explore the assessment framework, renewable "
        "energy siting, energy-system scenarios and export economics."
    )

elif page == "Four assessment dimensions":
    st.header("Four dimensions of the energy transition")
    st.write(
        "The thesis adopts an integrated perspective. The three export pathways "
        "are assessed across four dimensions rather than through technical or "
        "economic performance alone."
    )

    dimensions = [
        ("Technical feasibility", "Energy-system modelling and configuration, "
         "renewable generation, storage, energy balances and the infrastructure "
         "needed to deliver energy exports."),
        ("Economic viability", "Investment and system costs, export revenues, "
         "profitability and the levelised cost of export (LCOX)."),
        ("Social benefits", "Employment creation and the social and socioeconomic "
         "implications of the different export pathways."),
        ("Environmental impact", "Land and water requirements and the environmental "
         "implications associated with large-scale renewable energy and export "
         "pathways."),
    ]
    cols = st.columns(2)
    icons = ["⚙️", "€", "👥", "🌱"]
    for i, (heading, description) in enumerate(dimensions):
        with cols[i % 2]:
            st.markdown(f"### {icons[i]} {heading}")
            st.write(description)

    st.warning(
        "These descriptions introduce the assessment dimensions. Detailed "
        "indicators and numerical findings will be added from the corresponding "
        "thesis chapters and appendices; no missing values are inferred here."
    )

elif page == "Renewable energy siting":
    st.header("Renewable energy siting assessment")
    st.write(
        "The thesis applies a multi-criteria decision analysis (MCDA) to compare "
        "four candidate sites for large-scale renewable energy deployment."
    )
    st.metric("Candidate sites assessed", "4")
    st.subheader("Reference results from the thesis")
    site_view = siting_df.sort_values("rank").copy()
    site_view.columns = ["Candidate site", "Original MCDA score", "Original rank"]
    st.dataframe(site_view, hide_index=True, use_container_width=True)

    best = siting_df.loc[siting_df["rank"].idxmin()]
    st.success(
        f'{best["site"]} is the highest-ranked candidate, with an original '
        f'MCDA score of {best["score"]} and rank {best["rank"]}.'
    )

    fig = px.bar(
        siting_df.sort_values("rank"),
        x="site", y="score", text="score",
        title="Original MCDA scores by candidate site",
        labels={"site": "Candidate site", "score": "MCDA score"}
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Assessment method")
    st.write(
        "The thesis evaluates the candidate sites using 14 criteria and a "
        "weighted multi-criteria assessment. The original scores and ranking "
        "are reproduced here as reference results."
    )
    st.info(
        "The original thesis scores are preserved. Interactive changes to "
        "criterion weights and alternative rankings are not enabled yet; they "
        "will be added only after the original criteria, weights and scoring "
        "rules have been transcribed and checked."
    )

elif page == "Algeria's energy system":
    st.header("Algeria's energy system")
    st.write(
        "This module will bring together the thesis reference results for the "
        "2019 baseline and the 2050 domestic renewable-energy scenario, followed "
        "by the system configurations used in the export scenarios."
    )
    st.metric("2050 final energy demand", "908.72 TWh/year")
    st.info(
        "The detailed generation mix, installed capacities, storage and energy "
        "balance are reserved for integration from the corresponding thesis "
        "tables. Final energy demand must not be confused with total electricity "
        "generation."
    )

elif page == "Export scenarios":
    st.header("Three renewable energy export pathways")
    st.write(
        "The thesis models electricity exports through HVDC, green hydrogen "
        "exports and synthetic e-methane exports."
    )
    st.dataframe(
        export_df[["scenario", "export_volume_TWh_year"]].rename(columns={
            "scenario": "Export pathway",
            "export_volume_TWh_year": "Delivered exports (TWh/year)"
        }),
        hide_index=True,
        use_container_width=True
    )
    st.caption(
        "Export volumes shown here are the thesis reference values for delivered "
        "annual exports."
    )

elif page == "Economic assessment":
    st.header("Economic assessment")
    st.write(
        "This section compares annual export revenue, thesis-reported net profit "
        "and the levelised cost of export (LCOX)."
    )
    display = export_df[[
        "scenario", "export_volume_TWh_year", "market_price_EUR_MWh",
        "annual_revenue_EUR_bn", "reported_net_profit_EUR_bn", "LCOX_EUR_MWh"
    ]].copy()
    display.columns = [
        "Export pathway", "Delivered exports (TWh/year)", "Market price (€/MWh)",
        "Revenue (€bn/year)", "Reported net profit (€bn/year)", "LCOX (€/MWh)"
    ]
    st.dataframe(display, hide_index=True, use_container_width=True)

    left, right = st.columns(2)
    with left:
        fig = px.bar(
            export_df, x="scenario", y="annual_revenue_EUR_bn",
            title="Annual export revenue",
            labels={"scenario": "Export pathway", "annual_revenue_EUR_bn": "€bn/year"}
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.bar(
            export_df, x="scenario", y="LCOX_EUR_MWh",
            title="Levelised cost of export (LCOX)",
            labels={"scenario": "Export pathway", "LCOX_EUR_MWh": "€/MWh"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Important: two different cost calculations"):
        st.write(
            "The thesis distinguishes the export cost used in the net-profit "
            "calculation from the incremental system cost used for LCOX. They "
            "must not be treated as interchangeable."
        )
        st.write(
            "Incremental export system cost = total export-scenario system cost "
            "− total domestic base-scenario system cost."
        )
        st.write(
            "LCOX = incremental annual system cost ÷ net annual export energy delivered."
        )
        st.caption(
            "The thesis remains authoritative for published reference values. "
            "Supporting workbooks are used to understand calculations and "
            "discrepancies, not to silently overwrite thesis results."
        )

elif page == "Social assessment":
    st.header("Social assessment")
    st.write(
        "The thesis considers social benefits and implications of the export "
        "pathways, including employment creation."
    )
    st.info(
        "The detailed employment and social-impact indicators will be populated "
        "from the thesis's social-impact assessment. This page deliberately "
        "does not introduce estimates that are not yet integrated."
    )

elif page == "Environmental assessment":
    st.header("Environmental assessment")
    st.write(
        "The thesis considers environmental impacts associated with the "
        "renewable-energy and export pathways, including land and water "
        "requirements."
    )
    st.info(
        "The detailed land, water and environmental results will be populated "
        "from the thesis's environmental assessment. This page deliberately "
        "does not introduce estimates that are not yet integrated."
    )

elif page == "Interactive scenario explorer":
    st.header("Interactive scenario explorer")
    st.write(
        "Explore how changing the market price and delivered export volume "
        "affects the financial results while keeping the thesis cost assumption "
        "constant."
    )
    selected = st.selectbox("Select export pathway", export_df["scenario"].tolist())
    row = export_df.loc[export_df["scenario"] == selected].iloc[0]

    price = st.slider(
        "Market price (€/MWh)", 10.0, 200.0,
        float(row["market_price_EUR_MWh"]), 0.5
    )
    volume = st.slider(
        "Delivered export volume (TWh/year)", 100, 1000,
        int(row["export_volume_TWh_year"]), 5
    )

    adjusted_revenue = volume * price / 1000
    fixed_cost = float(row["annual_export_cost_for_profit_EUR_bn"])
    indicative_profit = adjusted_revenue - fixed_cost

    a, b, c = st.columns(3)
    a.metric("Adjusted revenue", f"€{adjusted_revenue:,.3f}bn/year")
    b.metric("Fixed thesis cost assumption", f"€{fixed_cost:,.3f}bn/year")
    c.metric("Indicative net profit", f"€{indicative_profit:,.3f}bn/year")

    st.warning(
        "This is a financial sensitivity calculation, not an EnergyPLAN "
        "simulation. It does not recalculate hourly generation, demand, storage, "
        "curtailment, transmission losses or physical system feasibility. "
        "Changing export volume here does not demonstrate that the energy system "
        "can technically deliver that volume."
    )

else:
    st.header("Methodology and sources")
    st.subheader("Modelling approach")
    st.write(
        "The thesis uses EnergyPLAN 16.3 for energy-system modelling, "
        "LUT-DEMAND for 2050 demand and PVGIS solar profiles. The assessment "
        "covers technical, economic, social and environmental dimensions."
    )
    st.subheader("Source hierarchy")
    st.markdown(
        """
        1. **Final 2025 master's thesis:** primary reference for published results.
        2. **Updated supporting Excel workbooks:** calculation evidence and detailed inputs where consistent with the thesis.
        3. **Earlier workbooks and EnergyPLAN files:** historical development records, not replacements for final thesis results.
        """
    )
    st.subheader("Interpretation")
    st.write(
        "Published thesis results are kept separate from user-generated "
        "sensitivity calculations. The scenario explorer is not an EnergyPLAN "
        "replacement."
    )

st.divider()
st.caption(
    "Research reference: Imadeddine Menakh (2025), "
    "*Powering EU? – Energy scenarios for exporting electricity, green hydrogen "
    "and e-methane from Algeria to Europe*. Prototype dashboard."
)
