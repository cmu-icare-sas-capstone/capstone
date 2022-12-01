import streamlit as st


class SessionState:
    session_state: dict

    def __init__(self):
        self.session_state = st.session_state

    def get(self, key):
        if key not in self.session_state.keys():
            return None
        else:
            return self.session_state[key]

    def remove(self, key):
        return self.session_state.pop(key, None)

    def put(self, key, value):
        self.session_state[key] = value


session_state = SessionState()
