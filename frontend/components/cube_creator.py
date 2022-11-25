from typing import List, Dict

import streamlit
from repository.MetaDataRepository import meta_data_repo
from frontend.components import multi_selector
import streamlit as st
from entity.Cube import Cube
import uuid


def create_cube_creator(dataset_name: str) -> Cube:
    src_dimensions: tuple = meta_data_repo.get_dimensions(dataset_name)
    src_values: tuple = meta_data_repo.get_values(dataset_name)
    filter_multiselect_box: List[str] = st.multiselect(
        "Select which filter to enable",
        options=src_dimensions,
        key="cube_creator_filter"
    )

    value_multiselect_box: List[str] = streamlit.multiselect(
        "Select with value to explore",
        options=src_values,
        key="cube_creator_value"
    )

    filters: Dict[str, List[str]] = {}
    for item in filter_multiselect_box:
        filter_options = meta_data_repo.get_dataset_column_values(dataset_name, item)
        filters[item] = multi_selector.create_multi_selector("cube_creator_filter_"+item+"_", item, filter_options)

    values: List[str] = value_multiselect_box
    rules = {
        "filters": filters,
        "values": values
    }
    name = st.text_input(
            "Cube Name",
            placeholder="Please enter a name for the cube"
        )

    add_button = st.button(
        "Save Cube",
        key="cube_creator_save_cube_button"
    )

    if name == "":
        name = (str(uuid.uuid1()))[0: 6]

    if len(filters) > 0 and len(values) > 0:
        cube = Cube(dataset_name, name)
        cube_values = cube.peek_cube(rules)
        st.table(cube_values.describe())

        if add_button:
            cube.init_cube(rules)
            return cube

    return None


