import streamlit as st
import plotly.graph_objects as go
import plotly.express
import plotly.subplots


def create_bar_chart(cube):
    value_col, cal_col, group_by_col = st.columns(3)
    with cal_col:
        cal_selection_box = st.selectbox(
            "calculation Method",
            options=("Sum", "Average", "Count", "Std"),
            key="cube_viewer_val_cal_type_" + cube.cube_name
        )

    with group_by_col:
        group_by_selection_box = st.selectbox(
            "Group By",
            options=cube.dimensions,
            key="cube_viewer_group_" + cube.cube_name
        )
    cube_data = cube.cube_data
    cube_values = cube.values
    groups = cube_data.groupby(group_by_selection_box)

    if cal_selection_box == "Sum":
        fig_df = groups.sum().loc[:, cube_values]
    elif cal_selection_box == "Average":
        fig_df = groups.mean().loc[:, cube_values]
    elif cal_selection_box == "Count":
        fig_df = groups.count().loc[:, cube_values]
    elif cal_selection_box == "Std":
        fig_df = groups.std().loc[:, cube_values]

    graph_col, description_col = st.columns([3, 2])
    with graph_col:
        fig = plotly.subplots.make_subplots(rows=2, cols=2)
        for i in range(0, len(cube_values)):
            fig.add_trace(
                go.Bar(name=cube_values[i], x=fig_df.index, y=fig_df.iloc[:, i], yaxis="y"+str(i+1), offsetgroup=i+1),
                row=int(i / 2 + 1),
                col=int(i % 2 + 1)
            )

        fig.update_layout(barmode="group")
        fig.update_yaxes(showgrid=False)

        st.plotly_chart(fig)

        # if fig_selection_box == "Pie Chart" and cal_selection_box == "Count":
        #     fig = go.Figure(
        #         data=[
        #             go.Pie(labels=fig_df.index, values=fig_df.iloc[:, 0])
        #         ]
        #     )
        #     fig.update_traces(hole=.4, hoverinfo="label+percent+name")
        #     fig.update_layout(title_text=cube.cube_name)
        #     st.plotly_chart(fig)