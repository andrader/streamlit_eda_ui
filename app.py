from time import sleep

import pandas as pd
import streamlit as st
from streamlit import session_state as state

from stedaui.filters import *
from stedaui.data import container_file_uploader, create_tabs, container_load_query

@st.cache(suppress_st_warning=True)
def load_data():
    st.success("Loading data")
    iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
    return iris


def init_state(key, value):
    if key not in state:
        print(f"Initializing {key}={str(value)}")
        if callable(value):
            state[key] = value()
        else:
            state[key] = value


def reset_filters(df):
    # with st.spinner("reseting filters"):
        #pass#sleep(0.2)
    state["filters"] = Filters(df)


st.set_page_config("App", layout="wide", initial_sidebar_state="expanded")
st.write("Hello world!")
df = load_data()


init_state("filters", lambda: Filters(df))
filters = state["filters"]

init_state("datasets", dict())


with st.sidebar:
    tabs = create_tabs(["Load", "Select", "Filter", "Plot"])

with tabs["Load"]:
    loadtabs = create_tabs(["Upload File", "SQL", "URL"])

    with loadtabs["SQL"]:
        container_load_query()
    
    with loadtabs["Upload File"]:
        container_file_uploader()
             
            



with tabs["Filter"]:
    del_filters = st.button("Delete filters", on_click=reset_filters, args=(df,))
    
    filters.show_add()
    filters.show_filters()

#st.dataframe(filters.show_df())


if state.datasets:

    dftabs = create_tabs(state.datasets)

    for name in dftabs:
        with dftabs[name]:
            st.dataframe(state.datasets[name], use_container_width=True, height=200)