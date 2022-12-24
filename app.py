import pandas as pd
import streamlit as st

from stedaui.filters import *


@st.cache(suppress_st_warning=True)
def load_data():
    st.success("Loading data")
    iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
    return iris



def reset_filters(df):
    st.warning("reseting filters")
    st.session_state["filters"] = Filters(df)


st.set_page_config("App", layout="wide", initial_sidebar_state="expanded")
st.write("Hello world!")
df = load_data()

if "filters" not in st.session_state:
    st.write("Creating Filters(df)")
    reset_filters(df)
filters = st.session_state["filters"]


with st.sidebar:

    st.title("Sidebar")

    tabnames = ["filter","histogram","scatter"]

    del_filters = st.button("Delete filters", on_click=reset_filters, args=(df,))
    
    filters.show_add()
    filters.show_filters()



def load_csv():

    st.write("Load csv")


load_csv()

# st.write("creating")
# a = Filter("aaa","bbb","ccc")
# st.write("above")
# b = a.show()
# with b:
#     st.write("test 2")
# st.write("bellow")
# with b:
#     st.write("test 3")

#st.write(filters)
#st.write(filters.filters)
st.dataframe(filters.show_df())
#st.dataframe(df)

