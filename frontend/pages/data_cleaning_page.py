import streamlit as st
from pandas import DataFrame
import pandas as pd
from repository.SessionState import session_state
from bean.logger import get_logger
from bean.GlobalState import state

repo = state.get("repo")
meta_data_repo = state.get("meta_data_repo")
logger = get_logger(__name__)
default_process_service = state.get("default_process_service")


def create_data_cleaning_page():
    col1, col2 = st.columns([1, 3])
    with col1:
        section = st.selectbox(
            label="Selection File Type",
            options=("Structured Data", "Public Comments"),
        )
    if section == "Structured Data":
        structured_data_section()
    elif section == "Public Comments":
        structured_data_section()


def structured_data_section():
    is_default: bool = False
    uploaded_df: DataFrame()
    cleaned_table_name = session_state.get("cleaned_table_name")
    table_name = upload_structured_file()
    logger.debug("Get uploaded file: %s" % table_name)

    default_dataset_info_holder = st.empty()
    process_info_holder = st.empty()
    if table_name is not None and cleaned_table_name is None:
        is_default = default_process_service.is_default(table_name)
        logger.debug("The upload file is default: %s" % is_default)
        if is_default:
            default_dataset_info_holder.success("The file is valid as a default dataset")
            if st.button("Process By Default"):
                structured_data_progress_bar = st.progress(0)
                process_info_holder.info("Processing and saving the data by default")
                cleaned_table_name = default_process_service.process(table_name, structured_data_progress_bar)
                structured_data_progress_bar.progress(100)
                structured_data_progress_bar.empty()
                logger.debug(repo.read_df(cleaned_table_name).head())
                session_state.put("uploaded_file_clean", cleaned_table_name)
        else:
            st.warning("The file is not valid as a default dataset")

    if cleaned_table_name is not None and table_name is not None:
        table_new_name = st.text_input(label="table_name", value=cleaned_table_name)
        dimensions = st.multiselect(
            label="Select data dimensions",
            options=meta_data_repo.get_table_columns(cleaned_table_name)
        )
        values = st.multiselect(
            label="Select data values",
            options=meta_data_repo.get_table_columns(cleaned_table_name)
        )
        confirm_table = st.button(label="confirm")
        if confirm_table:
            meta_data_repo.add_meta_data(table_new_name, dimensions, values)
    process_info_holder.empty()


# upload the file if there isn't one, otherwise return the existing one
def upload_structured_file():
    def change_file():
        session_state.remove("uploaded_file")
        session_state.remove("uploaded_file_clean")
        repo.remove_df("uploaded_file")
        repo.remove_df("uploaded_file_clean")

    uploaded_file = st.file_uploader("Choose a File", on_change=change_file)
    with st.spinner(text="Uploading and analyzing the file"):
        if session_state.get("uploaded_file") is not None:
            return session_state.get("uploaded_file")
        elif uploaded_file is not None:
            df = pd.read_csv(uploaded_file, low_memory=False)
            repo.save_df(df, "uploaded_file")
            session_state.put("uploaded_file", "uploaded_file")
            return "uploaded_file"

    return None


def comments_file_section():
    print()