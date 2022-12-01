from typing import List, Dict
from frontend.components import multi_selector
from bean.GlobalState import state
from repository.Cube import Cube
import streamlit as st
import uuid


meta_data_repo = state.get("meta_data_repo")


def create_cube_creator(dataset_name: str, cube) -> dict:
    src_dimensions: tuple = meta_data_repo.get_dimensions(dataset_name)
    src_values: tuple = meta_data_repo.get_values(dataset_name)
    filter_multiselect_box: List[str] = st.multiselect(
        "Select which filter to enable",
        options=src_dimensions,
        key="cube_creator_filter"
    )

    value_multiselect_box: List[str] = st.multiselect(
        "Select with value to explore",
        options=src_values,
        default=cube.values,
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

    if len(cube.values) > 0 or len(rules["values"]) > 0:
        cube_values = cube.peek_cube(rules)
        st.table(cube_values.describe())

    return rules
