import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st

# Set streamlit container = wide
# st.set_page_config(layout="wide")

# @st.cache_data
# def load_resales_data(file_name, mode):
#     if mode == "load":
#         return pd.read_csv(file_name)[
#             [
#                 "year",
#                 "date",
#                 "price/sqm",
#                 "flat_type_group",
#                 "flat_type",
#                 "remaining_lease",
#                 "town",
#                 "region",
#                 "storey_range",
#             ]
#         ]
#     else:
#         if file_name == "hdb_resales_fasqmvft.csv":
#             return pd.read_csv("hdb_resales.csv")[
#                 ["flat_type", "floor_area_sqm", "year"]
#             ]
#         elif file_name == "hdb_resales_psqmvft.csv":
#             return pd.read_csv("hdb_resales.csv")[["flat_type", "price/sqm", "year"]]
#         else:
#             return pd.read_csv(file_name)[["flat_type", "price/sqm", "year"]]

# hdb_mapping = pd.read_csv("hdb_mapping.csv", "load_opt")

hdb_mapping = pd.read_csv("hdb_mapping.csv")

st.map(hdb_mapping)

