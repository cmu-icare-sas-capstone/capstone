from typing import Dict
from pandas import DataFrame
from typing import List

import plotly.express
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

import old.l1.etl.DatabaseIO as dbio
from old.web.constants.WebConstants import readable_column_map
import pandas as pd
import plotly.graph_objects as go

dimensions = ("facility_id", "age_group", "race", "ccs_diagnosis_description", "gender", "area_name")
values = ("length_of_stay", "total_costs")


def create_olap_container(container_id: int) -> DataFrame:
    filter_types_map: Dict[str, str] = {
        "Race": "select_box",
        "Age Group": "select_box",
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
    data: DataFrame = dbio.read_from_db("hospital_inpatient_discharges")
    olap_container: DeltaGenerator = st.container()
    olap_container.header("Group %d" % container_id)

    with olap_container:
        filter_col: DeltaGenerator
        value_col: DeltaGenerator
        describe_col: DeltaGenerator
        filter_col, value_col, describe_col = st.columns([2, 2, 2])

        with filter_col:
            filter_multiselect_box: List[str] = st.multiselect(
                "Select which filter to enable",
                ["Race", "Age Group", "CCS Diagnosis Description", "Area Name"],
                key="filter" + str(container_id)
            )

            filter_selection_box_map: Dict[str, str] = {}
            slicers: List[str] = []
            for opt in filter_multiselect_box:
                slicers.append(readable_column_map[opt])
                if filter_types_map[opt] == 'select_box':
                    selection_box = st.selectbox(
                        opt,
                        options=tuple(Cube.query_available_options(data=data, column=readable_column_map[opt])),
                        key=str(container_id) + opt
                    )
                    filter_selection_box_map[str(container_id) + opt] = selection_box

                elif filter_types_map[opt] == "multiselect_box":
                    key: str = str(container_id) + opt + "mult_select"
                    if key not in st.session_state:
                        multiselect_box = []
                        st.session_state[key] = multiselect_box
                    else:
                        multiselect_box = st.session_state[key]

                    with st.expander(opt):
                        next_val: str = st.selectbox(
                            opt,
                            options=tuple(Cube.query_available_options(data=data, column=readable_column_map[opt])),
                            key=str(container_id) + opt,
                        )
                        user_val: str = st.text_input(
                            opt,
                            key=str(container_id)+opt+"text_input"
                        )
                        clear_button: DeltaGenerator = st.button(
                            "clear",
                            key=str(container_id)+opt+"button"
                        )
                        if clear_button:
                            next_val = ""
                            user_val = ""
                            multiselect_box.clear()

                        if next_val not in multiselect_box and len(next_val) > 0:
                            multiselect_box.append(next_val)

                        if len(user_val) > 0:
                            matched_columns: List[str] = Cube.match_columns(data=data, column=readable_column_map[opt],
                                                                            wildcard=user_val)
                            for item in matched_columns:
                                if item not in multiselect_box:
                                    multiselect_box.append(item)

                        st.text_area(opt, value=multiselect_box, disabled=True, key=str(container_id)+opt+"text_area")
                        filter_selection_box_map[str(container_id) + opt] = multiselect_box

        with value_col:
            value_multiselect_box = st.multiselect(
                "Select which value to drill",
                ["LOS", "Cost"],
                key="value" + str(container_id)
            )

            values = []
            for opt in value_multiselect_box:
                values.append(readable_column_map[opt])

        filters = {}
        for opt in filter_multiselect_box:
            filters[readable_column_map[opt]] = filter_selection_box_map[str(container_id) + opt]

        data_cube = pd.DataFrame()
        if len(values) > 0 and len(slicers) > 0 and len(filters) > 0:
            data_cube = Cube.peek_cube(data)

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
                    key="figure_options_" + str(container_id)
                )
            with cal_col:
                cal_selection_box = st.selectbox(
                    "calculation Method",
                    options=("Sum", "Average", "Count"),
                    key="calculation_method_" + str(container_id)
                )

            with groupby_col:
                groupby_selection_box = st.selectbox(
                    "groupby selection box",
                    options=(dimensions - filters.keys()),
                    key="groupby_selection_" + str(container_id)
                )

            if not data_cube.empty:
                groups = Cube.group_cube(data_cube, groupby_selection_box)

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

    return data_cube
