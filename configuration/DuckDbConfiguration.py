import duckdb
import streamlit as st


class DuckDbConfiguration:
    def __init__(self):
        return

    def get_connection(self):
        conn = duckdb.connect(database=":memory:", read_only=False)
        return conn


duckdb_configuration = DuckDbConfiguration()
