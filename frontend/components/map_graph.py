import folium as folium

from entity.Cube import Cube
import streamlit as st
from folium.plugins import HeatMap
import streamlit.components.v1 as components
from bean.Beans import logger


def create_map_graph(cube: Cube):
    value_col, cal_col, group_by_col = st.columns(3)
    with value_col:
        value_selection_box = st.selectbox(
            "Select Value",
            options=cube.values,
            key="cube_viewer_value_" + cube.cube_name
        )
    with cal_col:
        cal_selection_box = st.selectbox(
            "calculation Method",
            options=("SUM", "PERCENTAGE"),
            key="cube_viewer_val_cal_type_" + cube.cube_name
        )
    with group_by_col:
        group_by_selection_box = st.multiselect(
            "Group By",
            default=["lat", "lon"],
            options=cube.dimensions + ["lat", "lon"],
            key="cube_viewer_group_" + cube.cube_name
        )

    if cal_selection_box == "SUM":
        df = cube.get_group_by_values(group_by_selection_box, [value_selection_box], [cal_selection_box])
        df = df.rename({
            "lat": "latitude",
            "lon": "longitude",
            "%s_%s" % (cal_selection_box, value_selection_box): "weight"
        })
        create_map(df)

    if cal_selection_box == "PERCENTAGE":
        df = cube.get_group_by_values(group_by_selection_box, [value_selection_box], ["SUM", "COUNT"])
        df["percentage"] = df["%s_%s" % ("SUM", value_selection_box)] / df["%s_%s" % ("COUNT", value_selection_box)]
        df = df.rename(columns={"lat": "latitude", "lon": "longitude", "percentage": "weight"})
        logger.debug(df.head())
        create_map(df)


def create_map(df):
    map_df = df.loc[:, ["latitude", "longitude", "weight"]]
    lat, lon = df.loc[0, "latitude"], df.loc[0, "longitude"]
    m = folium.Map([lat, lon], tiles='cartodbpositron', zoom_start=9)
    HeatMap(map_df).add_to(m)
    components.html(m._repr_html_(), width=1400, height=1000)