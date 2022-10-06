import l2.eda.basic_eda as basic_eda
import matplotlib.pyplot as plt
import streamlit as st


def eda_options_container():
    eda_select_box = st.selectbox(
            "EDA Options",
            options=("Data Point Count", "Box Plot")
        )

    data_counter_container = st.container()
    # if eda_select_box == "Data Point Count":
    #     data_counter_container.header("Data Point Count")
    #
    #     with data_counter_container:
    #         group = st.selectbox(
    #             "Group By",
    #             options=("Age", "Race", "LOS", "County")
    #         )
    #         col1, col2 = st.columns(2)
    #         if group == "Age":
    #             show_count_and_describe("age_group", col1, col2)
    #         elif group == "Race":
    #             show_count_and_describe("race", col1, col2)
    #         elif group == "LOS":
    #             show_count_and_describe("length_of_stay", col1, col2)
    #         elif group == "County":
    #             show_count_and_describe("area_name", col1, col2)

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


# def show_count_and_describe(column, col1, col2):
#     with col1:
#         group_df = basic_eda.group_by("age_group")
#         st.bar_chart(data=group_df)
#     with col2:
#         group_df_description = basic_eda.data.loc[:, column]
#         st.table(group_df_description)
