from typing import Dict
from repository.SessionState import session_state
from frontend.pages.dashboard_page.new_cube_modal import get_new_cube_modal
from bean.logger import get_logger
import streamlit as st
from bean.GlobalState import state
from repository.Cube import Cube
from frontend.components import cube_creator
from frontend.pages import dashboard


def create_cube_creator_page():
    logger = get_logger(__name__)
    cube_map: Dict = session_state.get("cube_map")
    meta_data_repo = state.get("meta_data_repo")
    dataset_name = st.selectbox(
        label="Select the dataset",
        options=meta_data_repo.get_all_tables()
    )
    col1, col2, col3 = st.columns([2, 2, 6])

    with col2:
        new_cube_name = get_new_cube_modal()
        logger.debug(new_cube_name)
        if len(new_cube_name) > 0:
            cube = Cube(dataset_name=dataset_name, cube_name=new_cube_name)
            cube.init_cube()

    with col1:
        cube_list = meta_data_repo.get_views(table_name=dataset_name)
        cube_selection_box = st.selectbox(
            "Available Cubes",
            options=cube_list,
            key="available_cubes_selection_box",
        )

        if cube_selection_box is None:
            return

        selected_cube = Cube.get_cube(dataset_name, cube_selection_box)

    col3, col4 = st.columns([6, 4])

    with col3:
        if meta_data_repo.exists_view(selected_cube.cube_name, dataset_name):
            if len(selected_cube.values) > 0:
                dashboard.create_dashboard(dataset_name=dataset_name, selected_cube=selected_cube)

    with col4:
        cube_name = st.text_input(label="Cube Name", value=selected_cube.cube_name)
        col41, col42 = st.columns([2, 4])
        with col41:
            st.metric(label="Data Size", value=selected_cube.counts())
        with col42:
            st.text_area(label="Applied Filters", value=selected_cube.rules, height=50, disabled=True)

        create_rules = cube_creator.create_cube_creator(dataset_name, selected_cube)

        col5, col6 = st.columns(2)
        with col5:
            save = st.button(label="Save Cube")
            if save:
                selected_cube.persist_cube(create_rules, cube_name)
        with col6:
            delete = st.button(label="Delete")


    # col_cube_creator, col_cube_list = st.columns([5, 5])
    #

    #
    # with col_cube_list:
    #     col_name, col_content = st.columns([1, 2])
    #     for key in cube_map:
    #         with col_name:
    #             st.write(cube_map[key].cube_name)
    #         with col_content:
    #             st.write("data count = " + str(cube_map[key].counts()))

    return cube_map
