from typing import Dict
from repository.MetaDataRepository import meta_data_repo
from frontend.components import cube_graph
import streamlit as st
from pandas import DataFrame
from entity.Cube import Cube
import plotly.graph_objects as go


def create_dashboard(dataset_name: str, cube_map: Dict[str, Cube]):
    cube: Cube
    cube_selection_box = st.multiselect(
        "Available Cubes",
        options=tuple(cube_map.keys()),
        key="available_cubes_selection_box"
    )
    with st.expander("Cube Details"):
        for cube_name in cube_selection_box:
            cube = cube_map[cube_name]
            cube_graph.create_cube_graph(cube)

    # comparison between cubes
    fig_col, cal_col = st.columns(2)
    cubes_df: DataFrame = DataFrame()
    try:
        if len(cube_selection_box) > 1:
            all_values: list = meta_data_repo.get_values(dataset_name)

            for cube_name_key in cube_map:
                cube_map[cube_name_key].cube_data.loc[:, "group_no"] = cube_name_key
                cubes_df = cubes_df.append(cube_map[cube_name_key].cube_data)

            cube_groups = cubes_df.groupby("group_no")
            with fig_col:
                cubes_fig_selection_box = st.selectbox(
                    "Select graph type",
                    options=("Bar Chart", "dummy"),
                    key="cube_viewer_fig_type_cubes"
                )

            with cal_col:
                cubes_cal_selection_box = st.selectbox(
                    "Calculation Method",
                    options=("Sum", "Average", "Count"),
                    key="cube_viewer_val_cal_type_cubes"
                )

                if cubes_cal_selection_box == "Sum":
                    cube_fig_df = cube_groups.sum().loc[:, all_values]
                elif cubes_cal_selection_box == "Average":
                    cube_fig_df = cube_groups.mean().loc[:, all_values]
                elif cubes_cal_selection_box == "Count":
                    cube_fig_df = cube_groups.count().loc[:, all_values]

            if cubes_fig_selection_box == "Bar Chart":
                cube_fig = go.Figure(
                    data=[
                        go.Bar(name=all_values[0], x=cube_fig_df.index, y=cube_fig_df.iloc[:, 0], yaxis='y1',
                               offsetgroup=1),
                        go.Bar(name=all_values[1], x=cube_fig_df.index, y=cube_fig_df.iloc[:, 1], yaxis='y2',
                               offsetgroup=2)
                    ],
                    layout={
                        'yaxis1': {'title': all_values[0]},
                        'yaxis2': {'title': all_values[1], 'overlaying': 'y', 'side': 'right'}
                    }
                )
                cube_fig.update_layout(barmode="group")
                cube_fig.update_yaxes(showgrid=False)
                st.plotly_chart(cube_fig)
    except:
        st.write("Must have two values to show this graph")
