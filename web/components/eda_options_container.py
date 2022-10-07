import l2.eda.basic_eda as basic_eda
import matplotlib.pyplot as plt
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
                st.bar_chart(data=group_df)
            elif group == "Race":
                group_df = basic_eda.group_by("race")
                st.bar_chart(data=group_df)
            elif group == "LOS":
                group_df = basic_eda.group_by("length_of_stay")
                st.bar_chart(data=group_df)
            elif group == "County":
                group_df = basic_eda.group_by("county")
                st.bar_chart(data=group_df)

    if eda_select_box == "Box Plot":
        data_counter_container.header("Boxplot")
        with data_counter_container:
            group = st.selectbox(
                "Column",
                options=("Length Of Stay", "Total Cost")
            )
            if group == "Length Of Stay":
                group_df = basic_eda.data["length_of_stay"]
                fig, ax = plt.subplots()
                ax.boxplot(group_df, showfliers=False)
                
            if group == "Total Cost":
                group_df = basic_eda.data["total_costs"]
                fig, ax = plt.subplots()
                ax.boxplot(group_df, showfliers=False)
                
            st.pyplot(fig)


