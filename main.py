from typing import Dict
import streamlit as st
st.set_page_config(layout="wide")
from streamlit_option_menu import option_menu
from frontend.pages import data_cleaning_page
from frontend.pages import cube_creator_page
import init
import streamlit_nested_layout
from repository.SessionState import session_state
from repository.MetaDataRepository import meta_data_repo
from frontend.pages import dashboard
from repository.GlobalState import get_global_state


# for test
import pandas as pd
from repository.Repository import repo
from service.DefaultProcessService import default_process_service

if session_state.get("cleaned_table_name") is None:
    data = pd.read_csv("data/hospital_episodes_inpatient_discharges_7_0.csv")
    repo.save_df(data, "data")
    default_process_service.process("data")
    df = repo.read_df("data_clean")
    meta_data_repo.add_meta_data(
        "data_clean",
        ["facility_id", "race", "age_group", "ccs_diagnosis_description", "area_name"],
        ["length_of_stay", "total_costs", "long_stay"]
    )
    session_state.put("cleaned_table_name", "data_clean")

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Data Cleaning", "Cube Creator", "Dashboard", "Model"],
        menu_icon="cast",
        default_index=0
    )

repo.get_all_views()
if "cube_map" not in st.session_state:
    st.session_state["cube_map"] = {}
cube_map: Dict = st.session_state["cube_map"]
if selected == "Data Cleaning":
    data_cleaning_page.create_data_cleaning_page()
if selected == "Cube Creator":
    cube_map = cube_creator_page.create_cube_creator_page()
if selected == "Dashboard":
    dashboard.create_dashboard(session_state.get("cleaned_table_name"), cube_map)
