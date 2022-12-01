from typing import List

import streamlit as st

import utility
from bean.logger import get_logger
from repository.SessionState import session_state


logger = get_logger(__name__)


def create_multi_selector(key: str, label: str, options: List[str]) -> List[str]:
    logger.debug("Create multi selector " + key)
    with st.expander(label):

        if session_state.get(key) is None:
            logger.debug("no key found")
            multi_selector_values: List[str] = []
            session_state.put(key, multi_selector_values)
        else:
            multi_selector_values = session_state.get(key)

        with st.container():
            clear_button = st.button(
                "clear",
                key=key + "_button"
            )

            if clear_button:
                multi_selector_values.clear()

            multi_selector: str = st.selectbox(
                label,
                options=tuple(options),
                key=key+"_multi_selector",
            )
            logger.debug(multi_selector)
            if multi_selector != "dummy" and multi_selector not in multi_selector_values:
                multi_selector_values.append(multi_selector)

            user_input_box: str = st.text_input(
                "custom " + label,
                key=key+"_user_input_box"
            )
            user_customized_values: List[str] = utility.match_all_values_by_wildcard(options, user_input_box)
            multi_selector_values += user_customized_values
            logger.debug(multi_selector_values)
            session_state.put(key, multi_selector_values)
            selected_value_area: str = st.text_area(
                "selected values " + label,
                key=key+"_text_area",
                disabled=True,
                value=multi_selector_values
            )

    return multi_selector_values
