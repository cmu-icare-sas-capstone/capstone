"""
Main entrance for streamlit
"""
import streamlit as st
from streamlit_option_menu import option_menu
from web.components.eda_options_container import *
from web.components.coefficient_pie import plot_pie

with st.sidebar:
    selected = option_menu("Main Menu", ["EDA", "Model"],
        icons=['house'], menu_icon="cast", default_index=0)

if selected == "EDA":
    eda_options_container()
elif selected == 'Model':
    plot_pie()
    

