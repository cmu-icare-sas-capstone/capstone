import streamlit as st
from bean.Beans import logger


class GlobalState:
    global_state: dict

    def __init__(self):
        self.global_state = {}

    def get(self, key):
        if key not in self.global_state.keys():
            return None
        else:
            return self.global_state[key]

    def remove(self, key):
        return self.global_state.pop(key, None)

    def put(self, key, value):
        self.global_state[key] = value


@st.cache
def get_global_state():
    state = GlobalState()
    logger.debug("create global state")
    return state
