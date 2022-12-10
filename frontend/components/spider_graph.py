import streamlit as st
import plotly.graph_objects as go
from bean.GlobalState import state
import pandas as pd
repo = state.get("repo")


def create_spider_graph(cube):
    value_col, cal_col, group_by_col = st.columns(3)
    with value_col:
        value_selection_box = st.multiselect(
            "Select Value",
            default=cube.values,
            options=cube.values,
            key="cube_viewer_value_" + cube.cube_name
        )
    with cal_col:
        cal_selection_box = st.selectbox(
            "calculation Method",
            options=("AVERAGE",),
            key="cube_viewer_val_cal_type_" + cube.cube_name
        )
    with group_by_col:
        group_by_selection_box = st.multiselect(
            "Group By",
            options=("facility_id",),
            default="facility_id",
            key="cube_viewer_group_" + cube.cube_name
        )

    facilities = repo.get_values_of_one_column(cube.cube_name, "facility_id")
    facilities = [x.replace(".0", "\0") for x in facilities]


    count_df = cube.cube_data.groupby(['facility_id'])['length_of_stay'].agg('count').to_frame('count').reset_index()

    traces_df = []
    for i in range(0, len(value_selection_box)):
        val = value_selection_box[i]
        if val == "long_stay":
            # second trace: %long stay
            long_stay_df = cube.cube_data.groupby(['facility_id'])[val].agg('sum').to_frame("sum").reset_index()
            long_stay_df = pd.merge(count_df, long_stay_df, on='facility_id', how='outer')
            long_stay_df[val] = long_stay_df["sum"] / long_stay_df["count"] * 100
            traces_df.append(long_stay_df)
        else:
            traces_df.append(cube.cube_data.groupby(['facility_id'])[val].agg('mean').to_frame(val).reset_index())

    fig = go.Figure()

    for i in range(0, len(value_selection_box)):
        if value_selection_box[i] == "total_costs":
            r = [x/1000 for x in traces_df[i][value_selection_box[i]].tolist()]
        else:
            r = traces_df[i][value_selection_box[i]].tolist()
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=facilities,
            fill='toself',
            name=value_selection_box[i]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 55]
            )),
        showlegend=True
    )
    st.plotly_chart(fig)
