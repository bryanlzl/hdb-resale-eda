#%%
import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st
import os
import folium
from folium.features import CustomIcon
import numpy as np
import leafmap.foliumap as leafmap
import geojson
import geopandas as gpd

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
        
hdb_mapping = pd.read_csv("hdb_mapping.csv")
mrt_mapping = pd.read_csv("mrt_lrt_data.csv")

# some missing lat/lng, need to filter and re-update
hdb_mapping = hdb_mapping[hdb_mapping['latitude'] > 0]
hdb_mapping = hdb_mapping[hdb_mapping['latitude'] > 0]

#%%

# sub = min(hdb_mapping['price/sqm'])
# hdb_mapping
# # print(sub)
# hdb_mapping['price/sqm'] = hdb_mapping['price/sqm'] - sub

#%%
def central(feature): 
    return {
    "stroke": True,
    "color": "rgb(56, 155, 232)",
    "weight": 3,
    "opacity": 1,
    "fill": False,
    "fillColor": "rgb(131, 201, 255)",
    "fillOpacity": 0.3,
}

def north(feature): 
    return {
    "stroke": True,
    "color": "rgb(196, 102, 102)",
    "weight": 3,
    "opacity": 1,
    "fill": False,
    "fillColor": "rgb(255, 171, 171)",
    "fillOpacity": 0.3,
}

def west(feature): 
    return {
    "stroke": True,
    "color": "rgb(49, 153, 82)",
    "weight": 3,
    "opacity": 1,
    "fill": False,
    "fillColor": "rgb(125, 239, 161)",
    "fillOpacity": 0.3,
}

def east(feature): 
    return {
    "stroke": True,
    "color": "rgb(0, 104, 201)",
    "weight": 3,
    "opacity": 1,
    "fill": False,
    "fillColor": "rgb(0, 104, 201)",
    "fillOpacity": 0.1,
}

def northeast(feature): 
    return {
    "stroke": True,
    "color": "rgb(255, 43, 43)",
    "weight": 3,
    "opacity": 1,
    "fill": False,
    "fillColor": "rgb(255, 43, 43)",
    "fillOpacity": 0.1,
}

#%%
m = leafmap.Map()
m.add_basemap(basemap='TERRAIN')

gdf = gpd.read_file("1-region.geojson")
m.add_gdf(gdf.iloc[:1], layer_name="Central", style_function=central)
m.add_gdf(gdf.iloc[1:2], layer_name="East", style_function=east)
m.add_gdf(gdf.iloc[2:3], layer_name="North", style_function=north)
m.add_gdf(gdf.iloc[3:4], layer_name="North-East", style_function=northeast)
m.add_gdf(gdf.iloc[4:5], layer_name="West", style_function=west)

m.add_markers_from_xy(mrt_mapping[mrt_mapping["type"] == "MRT"], x='lng', y='lat', icon="subway", 
                      icon_shape=None, border_color=None, border_width=0, layer_name="MRT Stations",
                      background_color="transparent")
m.add_heatmap(hdb_mapping, name ="Price/sqm", value = 'price/sqm', radius=10)

m.to_streamlit(width = 900)
# %%
