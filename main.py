"""
Main entrance for streamlit
"""
import streamlit as st
from streamlit_option_menu import option_menu
from web.components.eda_options_container import eda_options_container
from web.components.model_container import model_container
from web.components.cube_container import olap_container
import streamlit_nested_layout
st.set_page_config(layout="wide")

with st.sidebar:
    selected = option_menu("Main Menu", ["EDA", "Model", "OLAP"],
        icons=['house'], menu_icon="cast", default_index=0)

if selected == "EDA":
    eda_options_container()
elif selected == 'Model':
    model_container()
elif selected == "OLAP":
    col1, col2 = st.columns(2)
    with col1:
        olap_container(0)
    with col2:
        olap_container(1)
