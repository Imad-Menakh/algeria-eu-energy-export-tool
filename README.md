Algeria Energy Transition Explorer

An Interactive Decision-Support Dashboard for Algeria's Renewable Energy Transition and Green Energy Exports to Europe

<p align="center">
  <a href="https://algeria-eu-energy-export-tool-ty7wpqcsfgzjsyc4wsbmhm.streamlit.app/">
    <strong>🚀 Launch Live Application</strong>
  </a>
  &nbsp; | &nbsp;
  <a href="https://github.com/Imad-Menakh/algeria-eu-energy-export-tool">
    <strong>💻 View Source Code</strong>
  </a>
</p>

1. Project Overview

The Algeria Energy Transition Explorer is an interactive Python-based application developed as an extension of my master's research at LUT University.

The application builds on the thesis:

Powering EU? – Energy scenarios for exporting electricity, green hydrogen and e-methane from Algeria to Europe.

The research investigates potential pathways for Algeria's transition towards a 100% renewable energy system by 2050, while examining opportunities to export renewable electricity, green hydrogen and e-methane to Europe.

The application transforms the research findings into an interactive decision-support environment, bringing together energy-system modelling results, renewable-energy siting assessments, and technical, economic, social and environmental analyses.

It is designed for researchers, energy professionals, consultants, students and policymakers interested in renewable-energy planning, energy-system transitions and international energy cooperation.

2. Research Objectives

The underlying research addresses the following objectives:

Examine pathways towards a 100% renewable energy system in Algeria by 2050.

Compare alternative domestic renewable-energy development and energy-export strategies.

Evaluate the technical configurations and infrastructure requirements of different energy pathways.

Assess the economic implications of renewable-energy production and export.

Investigate potential social and environmental impacts.

Identify and assess suitable areas for large-scale renewable-energy development in Algeria.

3. Energy-System Scenarios

The research examines five energy-system scenarios:

Scenario

Description

Algeria 2019 Baseline

Historical reference energy system

2050 Domestic Base

Renewable-energy system designed for domestic demand

2050 Electricity Export

Domestic renewable-energy system with electricity exports to Europe

2050 Green Hydrogen Export

Renewable hydrogen production and export pathway

2050 E-methane Export

Renewable e-methane production and export pathway

The five scenarios were simulated using EnergyPLAN 16.3.

The Python application presents and explores the resulting scenario data, providing additional analytical and interactive functionalities.

4. Main Application Modules

The dashboard is organised into ten research modules.

4.1 Research Overview

Introduction to the research objectives, scenario framework and energy-transition pathways.

4.2 Renewable Energy Siting Assessment

A two-step spatial assessment combining preliminary filtering and multi-criteria decision analysis (MCDA) to examine candidate renewable-energy development zones in Algeria.

The assessment includes candidate zones and multiple criteria for evaluating renewable-energy development suitability.

4.3 Technical Assessment

Presentation of the EnergyPLAN scenario configurations and technical indicators, including:

Solar PV and wind generation capacities.

Energy-system configuration.

Electricity and energy balances.

Battery and hydrogen storage.

Electrolyser capacity.

Export infrastructure requirements.

4.4 Social Assessment

Exploration of potential social implications, including:

Estimated permanent employment.

Temporary employment and job-years.

Domestic energy access.

Water access and regional development considerations.

4.5 Environmental Assessment

Examination of selected environmental indicators, including:

Water demand across scenarios.

Water requirements associated with hydrogen production.

Solar PV land requirements.

Reported emissions.

4.6 Scenario Comparison

Comparative presentation of the five scenarios across technical, economic, social and environmental dimensions.

4.7 Interactive Scenario Explorer

An interactive financial sensitivity tool that allows users to investigate the implications of alternative:

Energy market prices.

Delivered export volumes.

Export pathways.

The sensitivity calculations use the thesis cost assumptions and do not rerun the original EnergyPLAN simulations.

4.8 Methodology and Sources

Documentation of the research design, modelling approach, input data, assessment methods and supporting references.

4.9 Thesis Limitations and Critical Considerations

Discussion of methodological boundaries, scenario assumptions, infrastructure considerations and uncertainties affecting the interpretation of results.

4.10 Future Research Development

Identification of opportunities to extend the research, including hybrid export strategies, alternative energy carriers and low-carbon industrial exports.

5. Methodology and Analytical Framework

The application brings together several research and analytical approaches.

Component

Methodology or tool

Energy-system modelling

EnergyPLAN 16.3

Renewable-energy siting

Spatial filtering and MCDA

Technical assessment

Energy-system scenario analysis

Economic assessment

Investment, revenue, profitability and LCOX analysis

Social assessment

Employment estimation and access indicators

Environmental assessment

Water, land-use and emissions indicators

Data processing

Python and Pandas

Interactive application

Streamlit

Data visualisation

Plotly

Data and Research Sources

The underlying research draws on several sources, including:

IEA energy statistics.

Algerian national energy statistics.

LUT-DEMAND energy demand projections.

PVGIS solar resource profiles.

Published research on renewable-energy technologies and export infrastructure.

EnergyPLAN scenario inputs and outputs.

Supporting research literature and technical studies.

The master's thesis is the primary reference for the research methodology and reported scenario results.

6. Technology Stack

The project combines energy-system modelling with Python-based application development.

Technology

Application

EnergyPLAN 16.3

Original energy-system scenario simulations

Python

Dashboard development and analytical calculations

Pandas

Data organisation and processing

Streamlit

Interactive web application

Plotly

Interactive data visualisation

JSON

Structured storage of application datasets

GitHub

Version control and source-code management

Streamlit Community Cloud

Application deployment

7. My Contribution

I developed this application as an interactive extension of my master's research at LUT University.

Energy-System Modelling and Research

Developed and simulated five energy-system scenarios using EnergyPLAN 16.3 as part of my master's thesis.

Conducted technical, economic, social and environmental assessments.

Developed the renewable-energy siting assessment using spatial filtering and MCDA.

Analysed alternative renewable-energy export pathways from Algeria to Europe.

Python Application Development

Developed the interactive dashboard using Python and Streamlit.

Organised and processed research datasets using Pandas.

Implemented scenario selection and comparative analytical components.

Developed interactive visualisations using Plotly.

Implemented financial sensitivity calculations based on selected market assumptions and export volumes.

Structured the research findings into an accessible multi-module application.

8. Project Structure

The repository is organised into the following directories and files:

```text
algeria-eu-energy-export-tool/
│
├── assets/
│   ├── .gitkeep
│   ├── thesis_infrastructure_map.png
│   └── thesis_site_selection_map.png
│
├── data/
│   ├── export_scenarios.json
│   ├── siting_criteria.json
│   ├── siting_results.json
│   ├── siting_sites.json
│   ├── social_environment.json
│   └── technical_results.json
│
├── .gitignore
├── LICENSE
├── README.md
├── app.py
├── requirements.txt
└── site_selection_map_component.py

Directory and File Descriptions

assets/

Contains supporting visual assets used by the application.

thesis_infrastructure_map.png: Infrastructure map from the original research.

thesis_site_selection_map.png: Renewable-energy site-selection map from the original research.

.gitkeep: Keeps the directory tracked by Git when necessary.

data/

Contains structured JSON datasets used to populate the dashboard and support its analytical functionalities.

export_scenarios.json: Energy-export scenario data.

siting_criteria.json: Criteria used in the renewable-energy site-selection assessment.

siting_results.json: Results of the site-selection assessment.

siting_sites.json: Data describing the candidate sites.

social_environment.json: Social and environmental assessment data.

technical_results.json: Technical energy-system results.

Main application files

app.py: Main Streamlit application, including dashboard modules, data processing, analytical calculations and visualisations.

site_selection_map_component.py: Dedicated component for the interactive renewable-energy site-selection map.

requirements.txt: Python dependencies required to run the application.

.gitignore: Specifies files and directories excluded from Git version control.

LICENSE: Defines the licensing terms for the project.

README.md: Project documentation, methodology and installation instructions.

9. Run the Application Locally

Prerequisites

Python 3.10 or a compatible Python version.

Git.

pip.

Installation

Step 1. Clone the repository

git clone https://github.com/Imad-Menakh/algeria-eu-energy-export-tool.git

Step 2. Navigate to the project directory

cd algeria-eu-energy-export-tool

Step 3. Install the dependencies

pip install -r requirements.txt

Step 4. Run the Streamlit application

streamlit run app.py

The application should open in your default browser.

10. Interpretation and Limitations

The dashboard presents research findings, modelled scenario results and additional analytical calculations.

The following distinctions are important:

The five 2050 energy-system scenarios are simulations based on the assumptions and boundaries of the original research. They are not forecasts or guaranteed implementation outcomes.

The technical energy-system configurations are based on EnergyPLAN 16.3 scenario simulations.

The interactive financial sensitivity tool does not rerun EnergyPLAN or establish hourly operational feasibility.

Renewable-energy siting and social employment assessments are separate analytical components, not direct EnergyPLAN outputs.

Additional calculations and interpretations are distinguished from values directly reported in the thesis.

Results should be interpreted in the context of their underlying assumptions, data sources and methodological limitations.

11. Future Development

Potential future extensions include:

Integration of additional energy carriers.

Assessment of hybrid renewable-energy export strategies.

More advanced financial modelling and sensitivity analysis.

Integration of additional renewable-energy resource datasets.

Improved spatial analysis and GIS functionalities.

Development of reusable energy-system decision-support tools.

12. References

Menakh, I. (2025). Powering EU? – Energy scenarios for exporting electricity, green hydrogen and e-methane from Algeria to Europe. Master's thesis, LUT University.

13. Application and Contact

Live Application:
https://algeria-eu-energy-export-tool-ty7wpqcsfgzjsyc4wsbmhm.streamlit.app/

GitHub Repository:
https://github.com/Imad-Menakh/algeria-eu-energy-export-tool

Developer: Imadeddine Menakh

Institution: LUT University

LinkedIn:
https://www.linkedin.com/in/imadeddine-menakh-34502b37a/

This project demonstrates the integration of energy-system modelling, renewable-energy assessment and Python-based digital tools to support the exploration and communication of complex energy-transition scenarios.
