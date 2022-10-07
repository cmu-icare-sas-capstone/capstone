"""
Main entrance for streamlit
"""
import streamlit as st
from streamlit_option_menu import option_menu
from web.components.eda_options_container import eda_options_container
from web.components.model_container import model_container

with st.sidebar:
    selected = option_menu("Main Menu", ["EDA", "Model"],
        icons=['house'], menu_icon="cast", default_index=0)

if selected == "EDA":
    eda_options_container()
elif selected == 'Model':
    model_container()
    

