import pandas as pd

from old import l2 as basic_eda
import matplotlib.pyplot as plt
import streamlit as st


def eda_options_container():
    eda_select_box = st.selectbox(
            "EDA Options",
            options=("Basic Info", "Box Plot", "Correlation")
        )

    basic_info_container = st.container()
    if eda_select_box == "Basic Info":
        basic_info_container.header("Basic Info")
        x_col, y_col = st.columns(2)

        with basic_info_container:
            with x_col:
                group = st.selectbox(
                    "Group By",
                    options=("Age", "Race", "County", "Facility ID", "CCS Diagnosis Description", "Gender", "Covid Risk Factor", "LOS")
                )

            with y_col:
                value = st.selectbox(
                    "y-axis",
                    options=("Count", "Average LOS", "Average Cost")
                )

            group_map = {
                "Age": "age_group",
                "Race": "race",
                "County": "area_name",
                "Facility ID": "facility_id",
                "CCS Diagnosis Description": "ccs_diagnosis_description",
                "Gender": "gender",
                "Covid Risk Factor": "covid_risk_factor",
                "LOS": "length_of_stay"
            }
            value_map = {
                "Average LOS": "length_of_stay",
                "Average Cost": "total_costs"
            }

            if value == "Count":
                group_df = basic_eda.group_by_count(group_map[group])
            else:
                if group == "LOS" and value == "Average LOS":
                    group_df = pd.DataFrame()
                else:
                    group_df = basic_eda.group_by_average(column=group_map[group], value=value_map[value])

            st.bar_chart(data=group_df)

    if eda_select_box == "Box Plot":
        basic_info_container.header("Boxplot")
        with basic_info_container:
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

    # if eda_select_box == "Correlation":
