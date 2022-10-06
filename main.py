"""
Main entrance for streamlit
"""
import streamlit as st
from streamlit_option_menu import option_menu


with st.sidebar:
    selected = option_menu("Main Menu", ["EDA", 'Settings'],
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    selected