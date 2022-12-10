from typing import Dict
import streamlit as st
st.set_page_config(layout="wide")
from streamlit_option_menu import option_menu
import streamlit_nested_layout
import init
from frontend.pages import dataset_page
from frontend.pages.dashboard_page import cube_creator_page
from frontend.pages import model_page
from frontend.pages import nlp_page
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Dataset", "Dashboard", "Model", "NLP"],
        menu_icon="cast",
        default_index=0
    )

if "cube_map" not in st.session_state:
    st.session_state["cube_map"] = {}
cube_map: Dict = st.session_state["cube_map"]

if selected == "Dataset":
    dataset_page.dataset_page()
if selected == "Dashboard":
    cube_map = cube_creator_page.create_cube_creator_page()
if selected == "Model":
    model_page.create_model_page()
if selected == "NLP":
    nlp_page.create_nlp_page()
