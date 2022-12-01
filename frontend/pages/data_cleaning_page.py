import streamlit as st
from pandas import DataFrame
import pandas as pd
from repository.SessionState import session_state
from bean.logger import get_logger
from bean.GlobalState import state


repo = state.get("repo")
meta_data_repo = state.get("meta_data_repo")


def create_data_cleaning_page():
    logger = get_logger(__name__)
    default_process_service = state.get("default_process_service")
    uploaded_df: DataFrame()
    cleaned_table_name = session_state.get("cleaned_table_name")
    is_default: bool = False

    table_name: str = upload_file()
    logger.debug("Get uploaded file: %s" % table_name)

    if len(table_name) > 0 and cleaned_table_name is None:
        is_default = default_process_service.is_default(table_name)
        logger.debug("The upload file is default: %s" % is_default)
        if is_default:
            st.write("The data is valid as default dataset")
            if st.button("Process By Default"):
                st.write("Processing and store the data by default")
                cleaned_table_name = default_process_service.process(table_name)
                logger.debug(repo.read_df(cleaned_table_name).head())
                session_state.put("cleaned_table_name", cleaned_table_name)

    if cleaned_table_name is not None:
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


# upload the file if there isn't one, otherwise return the existing one
def upload_file() -> str:
    def change_file():
        session_state.remove("uploaded_file")

    uploaded_file = st.file_uploader("Choose a File", on_change=change_file)

    if session_state.get("uploaded_file") is not None:
        return session_state.get("uploaded_file")
    elif uploaded_file is not None:
        df = pd.read_csv(uploaded_file, low_memory=False)
        repo.save_df(df, "uploaded_file")
        session_state.put("uploaded_file", "uploaded_file")
        return "uploaded_file"

    return ""
