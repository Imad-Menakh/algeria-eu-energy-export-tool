"""Independent interactive satellite map for the Algeria site-selection module.

The polygons are the historical 58 wilaya administrative boundaries named in
Appendix 2. They are NOT the manually delineated candidate-zone boundaries.
This component deliberately does not invent the missing candidate polygons or
reconstruct Scribble Maps infrastructure lines from a screenshot.
"""
import requests
import folium
import streamlit as st
from streamlit_folium import st_folium

WILAYA_GEOJSON_URL = (
    "https://raw.githubusercontent.com/syscli/algeria/main/geo/wilayas-58.geojson"
)

WILAYA_NAMES = {
    "01": "Adrar", "02": "Chlef", "03": "Laghouat", "04": "Oum El Bouaghi",
    "05": "Batna", "06": "Bejaia", "07": "Biskra", "08": "Bechar",
    "09": "Blida", "10": "Bouira", "11": "Tamanrasset", "12": "Tebessa",
    "13": "Tlemcen", "14": "Tiaret", "15": "Tizi Ouzou", "16": "Algiers",
    "17": "Djelfa", "18": "Jijel", "19": "Setif", "20": "Saida",
    "21": "Skikda", "22": "Sidi Bel Abbes", "23": "Annaba", "24": "Guelma",
    "25": "Constantine", "26": "Medea", "27": "Mostaganem", "28": "M'Sila",
    "29": "Mascara", "30": "Ouargla", "31": "Oran", "32": "El Bayadh",
    "33": "Illizi", "34": "Bordj Bou Arreridj", "35": "Boumerdes",
    "36": "El Tarf", "37": "Tindouf", "38": "Tissemsilt", "39": "El Oued",
    "40": "Khenchela", "41": "Souk Ahras", "42": "Tipaza", "43": "Mila",
    "44": "Ain Defla", "45": "Naama", "46": "Ain Temouchent",
    "47": "Ghardaia", "48": "Relizane", "49": "Timimoun",
    "50": "Bordj Badji Mokhtar", "51": "Ouled Djellal",
    "52": "Beni Abbes", "53": "In Salah", "54": "In Guezzam",
    "55": "Touggourt", "56": "Djanet", "57": "El M'Ghair", "58": "El Menia",
}

SITE_MEMBERSHIP = {
    "01": ["Site 01"], "50": ["Site 01"], "52": ["Site 01", "Site 02"],
    "08": ["Site 02"], "32": ["Site 02"], "47": ["Site 02"],
    "58": ["Site 02"], "03": ["Site 02"], "51": ["Site 02"],
    "17": ["Site 02"], "57": ["Site 02"], "30": ["Site 02", "Site 03"],
    "33": ["Site 03"], "39": ["Site 03"], "55": ["Site 03"],
    "54": ["Site 04"], "11": ["Site 04"],
}
SITE_COLORS = {
    "Site 01": "#4934C8", "Site 02": "#42BFC0",
    "Site 03": "#C4B52B", "Site 04": "#B94D2F",
}

@st.cache_data(ttl=86400, show_spinner=False)
def load_wilaya_geojson():
    response = requests.get(WILAYA_GEOJSON_URL, timeout=30)
    response.raise_for_status()
    data = response.json()
    for feature in data.get("features", []):
        props = feature.setdefault("properties", {})
        code = str(props.get("code", props.get("Code", ""))).zfill(2)
        memberships = SITE_MEMBERSHIP.get(code, [])
        props["wilaya_code"] = code
        props["wilaya_name"] = WILAYA_NAMES.get(code, f"Wilaya {code}")
        props["site_membership"] = ", ".join(memberships) if memberships else "Not listed in a candidate zone"
    return data

def _style(feature):
    memberships = feature["properties"].get("site_membership", "")
    if memberships == "Site 01":
        color = SITE_COLORS["Site 01"]
    elif memberships == "Site 02":
        color = SITE_COLORS["Site 02"]
    elif memberships == "Site 03":
        color = SITE_COLORS["Site 03"]
    elif memberships == "Site 04":
        color = SITE_COLORS["Site 04"]
    elif memberships:
        color = "#777777"  # shared administrative associations
    else:
        color = "#ffffff"
    return {
        "fillColor": color,
        "color": "#f2f2f2" if memberships else "#b8b8b8",
        "weight": 1.2 if memberships else 0.45,
        "fillOpacity": 0.42 if memberships else 0.025,
    }

def render_site_admin_map():
    st.subheader("Satellite imagery and 58-wilaya administrative reference")
    st.caption(
        "Coloured outlines identify wilayas associated with candidate zones in "
        "Appendix 2. They are not the exact manually drawn site boundaries."
    )
    try:
        geojson = load_wilaya_geojson()
    except Exception as exc:
        st.warning(
            "The administrative boundary layer could not be loaded. The original "
            "thesis figure remains available below as the reference map."
        )
        st.caption(f"Technical detail: {exc}")
        return

    m = folium.Map(
        location=[28.0, 2.5], zoom_start=4, tiles=None,
        control_scale=True, prefer_canvas=True,
    )
    folium.TileLayer(
        tiles=("https://server.arcgisonline.com/ArcGIS/rest/services/"
               "World_Imagery/MapServer/tile/{z}/{y}/{x}"),
        attr=("Tiles © Esri — Sources: Esri, Maxar, Earthstar Geographics, "
              "and the GIS User Community"),
        name="Satellite imagery", overlay=False, control=True,
    ).add_to(m)
    folium.TileLayer(
        "OpenStreetMap", name="Road map", overlay=False, control=True,
    ).add_to(m)
    folium.GeoJson(
        geojson, name="Historical 58-wilaya administrative reference",
        style_function=_style,
        tooltip=folium.GeoJsonTooltip(
            fields=["wilaya_name", "wilaya_code", "site_membership"],
            aliases=["Wilaya:", "2019–2026 code:", "Appendix 2 association:"],
            sticky=True,
        ),
    ).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    st_folium(m, use_container_width=True, height=650, returned_objects=[])

    st.markdown(
        "**How to read the map**\n"
        "- Site 01, Site 02, Site 03 and Site 04 colours identify the wilayas listed under each site in Appendix 2.\n"
        "- Grey identifies wilayas associated with more than one candidate zone: Beni Abbes (Sites 01 and 02) and Ouargla (Sites 02 and 03).\n"
        "- The layer is an administrative reference only; it does not digitise the four site polygons, roads, gas pipelines or HVDC routes."
    )
    st.caption(
        "Boundary source: syscli/algeria, historical 58-wilaya layer (2019–2026), "
        "derived from OpenStreetMap/geoBoundaries; CC BY-SA 2.0. "
        "Attribution: © OpenStreetMap contributors. Satellite tiles: Esri."
    )
