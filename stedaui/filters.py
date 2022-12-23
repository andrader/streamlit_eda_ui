from dataclasses import dataclass
from functools import reduce
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st
from typing import Any, Union


def convert_types(df):
    df = df.copy()
    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)
    
    return df

def cat_filter(df, column):
    val = st.multiselect(
        f"Values for {column}",
        df[column].unique(),
        default=list(df[column].unique()),
    )
    if val:
        mask = df[column].isin(val)
        return column, val, mask
    

def num_filter(df, column):
    _min = float(df[column].min())
    _max = float(df[column].max())
    step = (_max - _min) / 100
    val = st.slider(
        f"Values for {column}",
        min_value=_min,
        max_value=_max,
        value=(_min, _max),
        step=step,
    )
    mask = df[column].between(*val)
    return column, val, mask

def date_filter(df, column):
    val = st.date_input(
        f"Values for {column}",
        value=(
            df[column].min(),
            df[column].max(),
        ),
    )
    if len(val) == 2:
        val = tuple(map(pd.to_datetime, val))
        start_date, end_date = val
        mask = df[column].between(start_date, end_date)
        return column, val, mask

def text_filter(df, column):
    val = st.text_input(
        f"Substring or regex in {column}",
    )
    
    if val:
        mask = df[column].astype(str).str.contains(val)
        return column, val, mask


def filter_col(df, column):
    if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
        # Treat columns with < 10 unique values as categorical
        res = cat_filter(df, column)
    elif is_numeric_dtype(df[column]):
        res = num_filter(df, column)
    elif is_datetime64_any_dtype(df[column]):
        res = date_filter(df, column)
    else:
        res = text_filter(df, column)
    
    return res




@dataclass
class Filter():
    column: str
    val: Any
    mask: pd.Series

    def show(self):
        ex = st.expander(f'**{self.column}**: {self.val}', expanded=False)
        return ex


class Filters():

    def __init__(self, df) -> None:
        self.df = df
        self.filters: dict[str, Filter] = {}
        self.connetors = []
        self.mask = None
        self.count = 0

        
    
    def show_add(self):

        container = st.expander("Filter", expanded=True)

        with container:
            selected_col = st.selectbox("Column", self.df.columns)
            res = filter_col(self.df, selected_col)

            confirm = st.button("Add", type="primary")
            if confirm and res is not None:
                col, val, mask = res
                new_filter = Filter(col, val, mask)
                # melhor nao, quando tiver operações diferentes
                # if new_filter in self.filters.values(): 
                #     st.error("Filter already exists!")
                # else:
                self.count += 1
                self.filters[selected_col + str(self.count)] = new_filter

        return container

    def show_df(self):
        masks = [f.mask for f in self.filters.values() if f.mask is not None]
        if not len(masks):
            return self.df
        mask = reduce(pd.Series.__and__, masks)
        self.current_df = self.df[mask]
        return self.current_df
    
    def show_filters(self):
        if self.filters:
            st.write("Filters:")
            for key in list(self.filters):
                f = self.filters[key]
                with f.show():
                    btn_delete = st.button(f"Delete", key=f"Delete {key}")
                    if btn_delete:
                        self.filters.pop(key)
