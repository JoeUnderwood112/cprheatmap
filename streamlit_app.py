
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="CPR Engineer Heatmap", layout="wide")

# Load the new Excel sheet
df = pd.read_excel("CPR HEATMAP.xlsx")

# Drop missing coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Sidebar filters
call_types = df["Refrigeration / Catering"].dropna().unique().tolist()
selected_call_type = st.sidebar.selectbox("Select Call Type", ["All"] + call_types)

subbie_types = df["Subbie"].dropna().unique().tolist()
selected_subbie = st.sidebar.selectbox("Select Subcontractor (Yes = Subbie, No = Internal)", ["All"] + subbie_types)

# Apply filters
filtered_df = df.copy()
if selected_call_type != "All":
    filtered_df = filtered_df[filtered_df["Refrigeration / Catering"] == selected_call_type]
if selected_subbie != "All":
    filtered_df = filtered_df[filtered_df["Subbie"] == selected_subbie]

engineers = filtered_df["Engineer(s)"].dropna().unique().tolist()
selected_engineer = st.sidebar.selectbox("Select Engineer", ["All"] + engineers)

if selected_engineer != "All":
    filtered_df = filtered_df[filtered_df["Engineer(s)"] == selected_engineer]

# Summary
st.markdown(f"### Showing {len(filtered_df)} calls")

# Map rendering
m = folium.Map(location=[54.5, -2.5], zoom_start=6)

for _, row in filtered_df.iterrows():
    label = f"{row['Engineer(s)']} | {row['Refrigeration / Catering']} | Subbie: {row['Subbie']}"
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=5,
        popup=label,
        color="blue",
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

st_folium(m, width=1000, height=700)
