from frontend.components.Modal import Modal
import streamlit as st


def get_new_cube_modal():
    new_cube_name = ""
    modal = Modal(title="Add Data Cube", key="new_cube_modal", max_width=600)
    st.write("")
    st.write("")
    open_modal = st.button("Add a New Data Cube")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            new_cube_name = st.text_input(label="Enter the cube name")
            if len(new_cube_name) == 0:
                st.write("Name cannot be empty!!")

            confirm = st.button("Confirm")
            if confirm:
                return new_cube_name

    return ""
