"""
Main entrance for streamlit
"""
import streamlit as st
from pandas import DataFrame
from streamlit_option_menu import option_menu

from old.web.components import eda_options_container
from old.web.components import model_container
from old.web.components.cube_container import create_olap_container
import plotly.graph_objects as go
import plotly
st.set_page_config(layout="wide")

with st.sidebar:
    selected = option_menu("Main Menu", ["EDA", "Model", "Dashboard"],
        icons=['house'], menu_icon="cast", default_index=0)

if selected == "EDA":
    eda_options_container()
elif selected == 'Model':
    model_container()
elif selected == "Dashboard":
    hide_col2 = st.checkbox('Hide Group 2')
    if not hide_col2:
        col1, col2 = st.columns(2)
        with col1:
            cube1: DataFrame = create_olap_container(1)
        with col2:
            cube2: DataFrame = create_olap_container(2)

        with st.expander("Group 1 vs Group2"):
            fig_col, cal_col, groupby_col = st.columns(3)
            with fig_col:
                fig_selection_box = st.selectbox(
                    "Select graph type",
                    options=("Bar Chart", "dummy"),
                    key="figure_options_groups"
                )
            with cal_col:
                cal_selection_box = st.selectbox(
                    "calculation Method",
                    options=("Sum", "Average", "Count"),
                    key="calculation_method_groups"
                )

            fig_df: DataFrame = DataFrame()
            cube1["group_no"] = 'Group1'
            cube2["group_no"] = 'Group2'
            fig_df = fig_df.append(cube1).append(cube2)
            groups = fig_df.groupby("group_no")

            selected_values = []
            for item in fig_df.columns:
                if item in old.web.components.cube_container.values:
                    selected_values.append(item)

            if cal_selection_box == "Sum":
                fig_df = groups.sum().loc[:, selected_values]
            elif cal_selection_box == "Average":
                fig_df = groups.mean().loc[:, selected_values]
            elif cal_selection_box == "Count":
                fig_df = groups.count().loc[:, selected_values]

            if fig_selection_box == "Bar Chart":
                if len(selected_values) == 2:
                    fig = go.Figure(
                        data=[
                            go.Bar(name=selected_values[0], x=fig_df.index, y=fig_df.iloc[:, 0], yaxis='y1',
                                   offsetgroup=1),
                            go.Bar(name=selected_values[1], x=fig_df.index, y=fig_df.iloc[:, 1], yaxis='y2',
                                   offsetgroup=2)
                        ],
                        layout={
                            'yaxis1': {'title': selected_values[0]},
                            'yaxis2': {'title': selected_values[1], 'overlaying': 'y', 'side': 'right'}
                        }
                    )
                    fig.update_layout(barmode="group")
                    fig.update_yaxes(showgrid=False)
                else:
                    fig = plotly.express.bar(fig_df)

                st.plotly_chart(fig)

    else:
        create_olap_container(1)
