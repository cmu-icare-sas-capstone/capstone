import streamlit as st
from pandas import DataFrame
from repository.Cube import Cube
from frontend.components import map_graph
from frontend.components import spider_graph
from frontend.components import bar_chart


def create_cube_graph(cube: Cube):
    cube_data: DataFrame = cube.cube_data
    cube_values: tuple = cube.values

    fig_selection_box = st.selectbox(
        "Select graph type",
        options=("Bar Chart", "Pie Chart", "Map", "Spider Map"),
        key="cube_viewer_fig_type_" + cube.cube_name
    )
    if fig_selection_box == "Map":
        map_graph.create_map_graph(cube)
    elif fig_selection_box == "Spider Map":
        spider_graph.create_spider_graph(cube)
    elif fig_selection_box == "Bar Chart":
        bar_chart.create_bar_chart(cube)
