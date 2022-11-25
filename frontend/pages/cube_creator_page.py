from typing import Dict
from repository.SessionState import session_state
from repository.MetaDataRepository import meta_data_repo
from frontend.components import cube_creator
from entity import Cube
import streamlit as st
import uuid
from bean.Beans import logger


def create_cube_creator_page():
    cube_map: Dict = session_state.get("cube_map")
    col_cube_creator, col_cube_list = st.columns([6, 4])
    dataset_name = st.selectbox(
        label="Select the dataset",
        options=meta_data_repo.get_all_table_names()
    )

    with col_cube_creator:
        logger.debug(dataset_name)
        cube: Cube = cube_creator.create_cube_creator(dataset_name)
        if cube is not None:
            logger.debug(cube.counts())
            cube_map[cube.cube_name] = cube

    with col_cube_list:
        col_name, col_content = st.columns([1, 2])
        for key in cube_map:
            with col_name:
                st.write(cube_map[key].cube_name)
            with col_content:
                st.write("data count = " + str(cube_map[key].counts()))

    return cube_map
