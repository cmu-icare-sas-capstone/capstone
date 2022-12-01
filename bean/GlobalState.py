import streamlit as st
from bean.logger import get_logger
import pickle


logger = get_logger(__name__)


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

    def get_or_default(self, key, default):
        if self.get(key) is None:
            self.put(key, default)
            return default
        else:
            return self.get(key)


@st.cache(persist=True)
def get_global_state():
    state = GlobalState()
    logger.debug("create global state")
    return state


state = get_global_state()
