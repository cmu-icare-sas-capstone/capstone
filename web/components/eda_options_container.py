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
        x_col, y_col = st.columns(2)

        with data_counter_container:
            with x_col:
                group = st.selectbox(
                    "Group By",
                    options=("Age", "Race", "County", "Facility ID", "CCS Diagnosis Description", "Gender", "Covid Risk Factor")
                )

            with y_col:
                value = st.selectbox(
                    "y-axis",
                    options=("Count", "Average LOS", "Average Cost")
                )

            group_map = {
                "Age": "age_group",
                "Race": "race",
                "County": "county",
                "Facility ID": "facility_id",
                "CCS Diagnosis Description": "ccs_diagnosis_description",
                "Gender": "gender",
                "Covid Risk Factor": "covid_risk_factor"
            }
            value_map = {
                "Average LOS": "length_of_stay",
                "Average Cost": "total_costs"
            }

            if value == "Count":
                group_df = basic_eda.group_by_count(group_map[group])
            else:
                group_df = basic_eda.group_by_average(column=group_map[group], value=value_map[value])
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
                fig, ax = plt.subplots()
                ax.boxplot(group_df, showfliers=False)

            st.pyplot(fig)

    if eda_select_box == "Covid Risk Factor Comparison":

