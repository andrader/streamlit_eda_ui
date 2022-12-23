import streamlit as st
import pandas as pd


@st.cache(suppress_st_warning=True)
def load_data():
    st.success("Loading data")
    iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
    return iris


st.set_page_config("App", layout="wide", initial_sidebar_state="expanded")
st.write("Hello world!")

from filters import *






                        
            
                

df = load_data()

if "filters" not in st.session_state:
    st.write("Creating Filters(df)")
    st.session_state["filters"] = Filters(df)
filters = st.session_state["filters"]


with st.sidebar:

    st.title("Filters")

    del_filters = st.button("Delete filters")
    if del_filters:
        st.session_state["filters"] = Filters(df)
        filters = st.session_state["filters"]
    
    filters.show_add()
    filters.show_filters()


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

