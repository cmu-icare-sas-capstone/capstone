import streamlit as st
import plotly
import plotly.graph_objects as go


def create_pie_chart(cube):
    value_col, cal_col, group_by_col = st.columns(3)
    with cal_col:
        cal_selection_box = st.selectbox(
            "calculation Method",
            options=("Count"),
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

    if cal_selection_box == "Count":
        fig_df = groups.count().loc[:, cube_values]

    graph_col, description_col = st.columns([3, 2])
    with graph_col:
        specs = [[{'type': 'domain'}, {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}]]
        fig = plotly.subplots.make_subplots(rows=2, cols=2, specs=specs)
        for i in range(0, len(cube_values)):
            fig.add_trace(
                go.Pie(title=cube_values[i], labels=fig_df.index, values=fig_df.iloc[:, i]),
                row=int(i / 2 + 1),
                col=int(i % 2 + 1)
            )

        fig.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig.update_layout(title_text=cube.cube_name)

        st.plotly_chart(fig)
