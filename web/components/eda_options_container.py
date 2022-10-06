import l2.eda.basic_eda as basic_eda
import web.graph as graphs
import streamlit as st

def eda_options_container():
    eda_select_box = st.selectbox(
            "EDA Options",
            options=("Data Point Count", "Box Plot")
        )

    data_counter_container = st.container()
    if eda_select_box == "Data Point Count":
        data_counter_container.header("Data Point Count")

        with data_counter_container:
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
        data_counter_container.header("Boxplot")
        with data_counter_container:
            group = st.selectbox(
                "Column",
                options=("LOS", "hello")
            )
            if group == "LOS":
                group_df = basic_eda.data["length_of_stay"]
                fig = graphs.plot_boxplot(data=group_df, x="length_of_stay")

            st.plotly_chart(fig)