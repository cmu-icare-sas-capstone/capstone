import plotly.express
import streamlit as st
import web.cube.Cube as cube
import l1.etl.DatabaseIO as dbio
from web.constants.WebConstants import readable_column_map
import pandas as pd
import plotly.graph_objects as go

dimensions = ("facility_id", "age_group", "race", "ccs_diagnosis_description", "gender", "area_name")


def olap_container(id: int):
    filter_types_map = {
        "Race": "select_box",
        "Age Group": "multiselect_box",
        "CCS Diagnosis Description": "multiselect_box"
    }
    # TODO: if more dataset need to be added
    # datasets_map = {
    #     "Cancer Alley": "hospital_inpatient_discharges"
    # }
    #
    # dataset_option_box = st.selectbox(
    #     "Dataset options",
    #     options="Cancer Alley"
    # )
    data = dbio.read_from_db("hospital_inpatient_discharges")
    olap_container = st.container()
    olap_container.header("Group %d" % (id))

    with olap_container:
        filter_col, value_col, describe_col = st.columns([2, 2, 2])

        with filter_col:
            filter_multiselect_box = st.multiselect(
                "Select which filter to enable",
                ["Race", "Age Group", "CCS Diagnosis Description", "Area Name"],
                key="filter" + str(id)
            )

            filter_selection_box_map = {}
            slicers = []
            for opt in filter_multiselect_box:
                slicers.append(readable_column_map[opt])
                if filter_types_map[opt] == 'select_box':
                    selection_box = st.selectbox(
                        opt,
                        options=tuple(cube.query_available_options(data=data, column=readable_column_map[opt])),
                        key=str(id) + opt
                    )
                    filter_selection_box_map[str(id) + opt] = selection_box

                elif filter_types_map[opt] == "multiselect_box":
                    multi_selection_box = st.multiselect(
                        opt,
                        options=tuple(cube.query_available_options(data=data, column=readable_column_map[opt])),
                        key=str(id) + opt,
                    )

                    filter_selection_box_map[str(id) + opt] = multi_selection_box

        with value_col:
            value_multiselect_box = st.multiselect(
                "Select which value to drill",
                ["LOS", "Cost"],
                key="value" + str(id)
            )

            values = []
            for opt in value_multiselect_box:
                values.append(readable_column_map[opt])

        filters = {}
        for opt in filter_multiselect_box:
            filters[readable_column_map[opt]] = filter_selection_box_map[str(id) + opt]

        data_cube = pd.DataFrame()
        if len(values) > 0 and len(slicers) > 0 and len(filters) > 0:
            data_cube = cube.get_cube(data, list(dimensions), filters, values)

        if not data_cube.empty:
            with describe_col:
                st.table(data_cube[values].describe())

        olap_fig_container = st.container()

        with olap_fig_container:
            fig_col, cal_col, groupby_col = st.columns(3)
            with fig_col:
                fig_selection_box = st.selectbox(
                    "Select graph type",
                    options=("Bar Chart", "Pie Chart"),
                    key="figure_options_" + str(id)
                )
            with cal_col:
                cal_selection_box = st.selectbox(
                    "calculation Method",
                    options=("Sum", "Average", "Count"),
                    key="calculation_method_" + str(id)
                )

            with groupby_col:
                groupby_selection_box = st.selectbox(
                    "groupby selection box",
                    options=(dimensions - filters.keys()),
                    key="groupby_selection_" + str(id)
                )
                custom_group_checkbox = st.checkbox("Create custom subgroups")
                if "custom_df" not in st.session_state:
                    custom_data_cube = pd.DataFrame()
                    st.session_state["custom_df"] = custom_data_cube
                    print(str(type(st.session_state["custom_df"])))
                else:
                    custom_data_cube = st.session_state["custom_df"]

                if custom_group_checkbox:
                    custom_cols_multiselect_box = st.multiselect(
                        "Custom Groups",
                        options=cube.query_available_options(data, groupby_selection_box),
                        key="custom_cols_multiselect_box_" + str(id)
                    )

                    # match custom groups
                    for i in range(len(custom_cols_multiselect_box)):
                        if custom_cols_multiselect_box[i] in cube.custom_groups.keys():
                            custom_group = custom_cols_multiselect_box[i]
                            # custom_cols_multiselect_box.remove(custom_cols_multiselect_box[i])
                            custom_cols_multiselect_box.append(custom_group)
                            real_values = cube.custom_groups[custom_group]
                            for item in real_values:
                                cp_data_cube = data_cube.copy(deep=True)
                                cp_data_cube = cp_data_cube[cp_data_cube[groupby_selection_box] == item]
                                cp_data_cube.loc[:, groupby_selection_box] = custom_group
                                print(cp_data_cube)
                                custom_data_cube = custom_data_cube.append(cp_data_cube)
                                print(custom_data_cube)
                        else:
                            custom_data_cube = custom_data_cube.append(data_cube[data_cube[groupby_selection_box]
                                                                                 == custom_cols_multiselect_box[i]])
                    print(custom_cols_multiselect_box)
                    ref_data_cube = custom_data_cube

                else:
                    ref_data_cube = data_cube
            if not ref_data_cube.empty:
                print(ref_data_cube)
                groups = cube.group_cube(ref_data_cube, groupby_selection_box)

                fig_df = pd.DataFrame()
                if cal_selection_box == "Sum":
                    fig_df = groups.sum().loc[:, values]
                elif cal_selection_box == "Average":
                    fig_df = groups.mean().loc[:, values]
                elif cal_selection_box == "Count":
                    fig_df = groups.count().loc[:, values]

                if fig_selection_box == "Bar Chart":
                    if len(values) == 2:
                        fig = go.Figure(
                            data=[
                                go.Bar(name=values[0], x=fig_df.index, y=fig_df.iloc[:, 0], yaxis='y1',
                                       offsetgroup=1),
                                go.Bar(name=values[1], x=fig_df.index, y=fig_df.iloc[:, 1], yaxis='y2',
                                       offsetgroup=2)
                            ],
                            layout={
                                'yaxis1': {'title': values[0]},
                                'yaxis2': {'title': values[1], 'overlaying': 'y', 'side': 'right'}
                            }
                        )
                        fig.update_layout(barmode="group")
                        fig.update_yaxes(showgrid=False)
                    else:
                        fig = plotly.express.bar(fig_df)

                    st.plotly_chart(fig)
