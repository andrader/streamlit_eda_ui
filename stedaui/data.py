
from time import sleep
import streamlit as st
from streamlit import session_state as state

import pandas as pd

def create_tabs(tabnames: list[str]):
    return dict(zip(tabnames, st.tabs(tabnames)))


def run_in_container_factory(container):
    print("running decorator factory")

    def decorator_run_in_container(func):
        print("running decorator")

        def wrapper(*args, **kwargs):
            print("running wrapper")
            with container:
                res = func(*args, **kwargs)
            return res
        
        return wrapper
    
    return decorator_run_in_container

def run_query(key):
    query = state[key]
    if query:
        with st.spinner(f"running {query}"):
            sleep(2)

def container_load_query():

    container = st.container()

    with container:

        _run_query2 = run_in_container_factory(container)(run_query)

        if "query" not in state:
            state['query'] = 'Select ...'

        key="container_load_query"
        st.text_area("Query", key=key, on_change=_run_query2, args=(key,))
        st.button("run", on_click=_run_query2, args=(key,))



st.experimental_memo
def read_file_to_df(file):
    with st.spinner(f"reading file {file.name}"):
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)

def container_file_uploader(uploaded_files_key="uploaded_files", datasets_key="datasets"):
    st.file_uploader("Select file", type=['csv','xlsx'], accept_multiple_files=True, key=uploaded_files_key)

    state[datasets_key] = {}
    for file in state[uploaded_files_key]:
        state[datasets_key][file.name.rsplit(".", 1)[0]] = read_file_to_df(file)