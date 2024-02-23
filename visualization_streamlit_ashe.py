import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st
import os
import leafmap.foliumap as leafmap
import geojson
import geopandas as gpd

hdb_mapping = pd.read_csv("hdb_mapping.csv")

with open("1-region.geojson") as f:
    gj = geojson.load(f)
regions = gj['features']

features = {}
for feature in gj['features']:
    features[feature['geometry']['type']] = feature['geometry']['coordinates']
    
#%% for foliumap
m = leafmap.Map()
m.add_basemap(basemap='TERRAIN')

def central(feature): 
    return {
    "stroke": True,
    "color": "#015085",
    "weight": 2,
    "opacity": 1,
    "fill": True,
    "fillColor": "#0595f5",
    "fillOpacity": 0.3,
}

def north(feature): 
    return {
    "stroke": True,
    "color": "#ff00f2",
    "weight": 2,
    "opacity": 1,
    "fill": True,
    "fillColor": "#85017e",
    "fillOpacity": 0.3,
}

def west(feature): 
    return {
    "stroke": True,
    "color": "#008200",
    "weight": 2,
    "opacity": 1,
    "fill": True,
    "fillColor": "#00ff00",
    "fillOpacity": 0.3,
}

def east(feature): 
    return {
    "stroke": True,
    "color": "#000082",
    "weight": 2,
    "opacity": 1,
    "fill": True,
    "fillColor": "#0000ff",
    "fillOpacity": 0.3,
}

def northeast(feature): 
    return {
    "stroke": True,
    "color": "#820000",
    "weight": 2,
    "opacity": 1,
    "fill": True,
    "fillColor": "#ff0000",
    "fillOpacity": 0.3,
}

gdf = gpd.read_file("1-region.geojson")
m.add_gdf(gdf.iloc[:1], layer_name="Central", style_function=central)
m.add_gdf(gdf.iloc[1:2], layer_name="East", style_function=east)
m.add_gdf(gdf.iloc[2:3], layer_name="North", style_function=north)
m.add_gdf(gdf.iloc[3:4], layer_name="North-East", style_function=northeast)
m.add_gdf(gdf.iloc[4:5], layer_name="West", style_function=west)

m.to_streamlit()