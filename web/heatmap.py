import l2.description.Maps as maps
import folium
from folium.plugins import HeatMap
import streamlit.components.v1 as components


def los_heatmap():
    heatmap = maps.heatmap_los()
    lat, lon = heatmap.loc[0, "latitude"], heatmap.loc[0, "longitude"]
    m = folium.Map([lat, lon], tiles='cartodbpositron', zoom_start=9)
    HeatMap(heatmap).add_to(m)
    components.html(m._repr_html_(), width=700, height=500)
