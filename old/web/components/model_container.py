import streamlit as st
from old.web.components.coefficient_pie import plot_pie


def model_container():
    model_select_box = st.selectbox(
            "Model Options",
            options=("LR1", "dummy")
    )

    model_fig_container = st.container()
    if model_select_box == "LR1":
        model_fig_container.header("LR1")
        with model_fig_container:
            plot_pie()


