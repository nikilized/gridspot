
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import geopandas as gpd

st.set_page_config(page_title="GridSpot", layout="wide")
st.title("GridSpot - EV Charging Opportunity Dashboard")

# Load and prepare data
df = pd.read_csv("data/gridspot_data.csv")
df["ZIP Code"] = df["ZIP Code"].astype(str)

gdf = gpd.read_file("data/dallas_zips.geojson")
gdf = gdf.merge(df, left_on="ZCTA5CE10", right_on="ZIP Code")

# Create folium map
m = folium.Map(location=[32.85, -96.85], zoom_start=10)

# Add colored polygons based on Opportunity Score
choropleth = folium.Choropleth(
    geo_data=gdf,
    name="Opportunity Score",
    data=gdf,
    columns=["ZIP Code", "Opportunity Score (0-100)"],
    key_on="feature.properties.ZCTA5CE10",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Opportunity Score"
).add_to(m)

# Add tooltips
folium.GeoJson(
    gdf,
    name="Labels",
    tooltip=folium.GeoJsonTooltip(
        fields=["ZIP Code", "City", "Estimated EVs", "Public Chargers", "Opportunity Score (0-100)"],
        aliases=["ZIP", "City", "EVs", "Chargers", "Score"],
        localize=True
    )
).add_to(m)

st.subheader("EV Charging Opportunity Map")
st_data = st_folium(m, width=1000, height=600)

# Table
st.subheader("ZIP Code Summary Table")
st.dataframe(df.sort_values("Opportunity Score (0-100)", ascending=False), use_container_width=True)
