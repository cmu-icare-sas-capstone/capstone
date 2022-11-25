import streamlit as st
from pandas import DataFrame
import plotly.graph_objects as go
import plotly.express
import plotly.subplots
from entity.Cube import Cube
from frontend.components import map_graph


def create_cube_graph(cube: Cube):
    cube_data: DataFrame = cube.cube_data
    cube_values: tuple = cube.values

    fig_col, value_col, cal_col, group_by_col = st.columns(4)
    with fig_col:
        fig_selection_box = st.selectbox(
            "Select graph type",
            options=("Bar Chart", "Pie Chart", "Map"),
            key="cube_viewer_fig_type_" + cube.cube_name
        )
    if fig_selection_box == "Map":
        map_graph.create_map_graph(cube)
    else:
        with cal_col:
            cal_selection_box = st.selectbox(
                "calculation Method",
                options=("Sum", "Average", "Count", "Std"),
                key="cube_viewer_val_cal_type_" + cube.cube_name
            )

        with group_by_col:
            group_by_selection_box = st.selectbox(
                "Group By",
                options=cube.dimensions,
                key="cube_viewer_group_" + cube.cube_name
            )


        groups = cube_data.groupby(group_by_selection_box)

        if cal_selection_box == "Sum":
            fig_df = groups.sum().loc[:, cube_values]
        elif cal_selection_box == "Average":
            fig_df = groups.mean().loc[:, cube_values]
        elif cal_selection_box == "Count":
            fig_df = groups.count().loc[:, cube_values]
        elif cal_selection_box == "Std":
            fig_df = groups.std().loc[:, cube_values]

        graph_col, description_col = st.columns([3, 2])
        with graph_col:
            if fig_selection_box == "Bar Chart":
                if len(cube.values) == 2:
                    fig = go.Figure(
                        data=[
                            go.Bar(name=cube_values[0], x=fig_df.index, y=fig_df.iloc[:, 0], yaxis='y1',
                                   offsetgroup=1),
                            go.Bar(name=cube_values[1], x=fig_df.index, y=fig_df.iloc[:, 1], yaxis='y2',
                                   offsetgroup=2)
                        ],
                        layout={
                            'yaxis1': {'title': cube_values[0]},
                            'yaxis2': {'title': cube_values[1], 'overlaying': 'y', 'side': 'right'}
                        }
                    )
                    fig.update_layout(barmode="group")
                    fig.update_yaxes(showgrid=False)
                else:
                    fig = plotly.express.bar(fig_df, text_auto=".2s")

                st.plotly_chart(fig)

            if fig_selection_box == "Pie Chart" and cal_selection_box == "Count":
                fig = go.Figure(
                    data=[
                        go.Pie(labels=fig_df.index, values=fig_df.iloc[:, 0])
                    ]
                )
                fig.update_traces(hole=.4, hoverinfo="label+percent+name")
                fig.update_layout(title_text=cube.cube_name)
                st.plotly_chart(fig)

        with description_col:
            st.table(cube_data.loc[:, cube.values].describe())
