"""
Main entrance for streamlit
"""
import streamlit as st
from streamlit_option_menu import option_menu
import l2.eda.basic_eda as basic_eda
import web.graph as graphs

with st.sidebar:
    selected = option_menu("Main Menu", ["EDA"],
        icons=['house'], menu_icon="cast", default_index=0)

if selected == "EDA":
    eda_select_box = st.selectbox(
        "EDA Options",
        options=("Data Point Count", "Box Plot")
    )

    data_point_count_container = st.container()
    if eda_select_box == "Data Point Count":
        data_point_count_container.header("Data Point Count")

        with data_point_count_container:
            group = st.selectbox(
                "Group By",
                options=("Age", "Race", "LOS", "County")
            )

            if group == "Age":
                group_df = basic_eda.group_by("age_group")
            elif group == "Race":
                group_df = basic_eda.group_by("race")
            elif group == "LOS":
                group_df = basic_eda.group_by("length_of_stay")
            elif group == "County":
                group_df = basic_eda.group_by("area_name")

            st.bar_chart(data=group_df)

    if eda_select_box == "Box Plot":
        data_point_count_container.header("Boxplot")
        with data_point_count_container:
            group = st.selectbox(
                "Column",
                options=("LOS", "hello")
            )
            if group == "LOS":
                group_df = basic_eda.data["length_of_stay"]
                fig = graphs.plot_boxplot(data=group_df, x="length_of_stay")

            st.plotly_chart(fig)





