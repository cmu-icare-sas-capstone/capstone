"""
Main entrance for streamlit
"""
import streamlit as st
import l2.description.Maps as maps
import folium
from folium.plugins import HeatMap
import streamlit.components.v1 as components
from spicy import stats

heatmap = maps.heatmap_los()
lat, lon = heatmap.loc[0, "latitude"], heatmap.loc[0, "longitude"]

data = heatmap[['latitude', 'longitude']]
max_los = heatmap["avg_los"].max()
min_los = heatmap["avg_los"].min()
data["weight"] = (heatmap["avg_los"] - min_los) / (max_los - min_los)
print(data["weight"])
m = folium.Map([lat, lon], tiles='cartodbpositron', zoom_start=9)
HeatMap(data).add_to(m)
components.html(m._repr_html_(), width=700, height=500)
