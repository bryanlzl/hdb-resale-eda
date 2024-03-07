#%%
import pandas as pd
import streamlit as st
import numpy as np
import leafmap.foliumap as leafmap
import geopandas as gpd

        
hdb_mapping_price = pd.read_csv("hdb_mapping_price_per_sqm.csv")
hdb_mapping_units = pd.read_csv("hdb_mapping_units.csv")
mrt_mapping = pd.read_csv("mrt_lrt_data.csv")

# some missing lat/lng, need to filter and re-update
hdb_mapping_price = hdb_mapping_price[hdb_mapping_price['latitude'] > 0]
hdb_mapping_units = hdb_mapping_units[hdb_mapping_units['latitude'] > 0]

#%% Styling
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
def renderBadge(option):
    badge_dict = {
        "slider_enabled": "https://img.shields.io/badge/Slider-Enabled-%23009f2d?style=flat-square&labelColor=%23676767",
        "slider_none": "https://img.shields.io/badge/Slider-None-%23c42323?style=flat-square&labelColor=%23676767",
        "static": "https://img.shields.io/badge/Static%20Data-%23959595",
    }
    if option == "slider_enabled":
        st.markdown(
            f"""<img src={badge_dict[option]} alt="slider-enabled">""",
            unsafe_allow_html=True,
        )
    elif option == "slider_none":
        st.markdown(
            f"""<img src={badge_dict[option]} alt="slider-enabled">""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<img src={badge_dict[option]} alt="slider-enabled">""",
            unsafe_allow_html=True,
        )

with st.sidebar:
    st.markdown(
        """
    <div style="background-color: #0e1117; margin-bottom: 20px; padding-left: 5px; width: auto; border: 1px; border-radius: 10px; ">
        <h4 style="color: white; margin: 0; padding: 8px 0px 8px 8px">Select plots to display</h4>
    </div>
    """,
        unsafe_allow_html=True,
    )
    cb_row = {
        "plot_0": "Distribution of Resale Prices Across Years",
        "plot_1": "Comparison of Resale Prices by Flat Type",
        "plot_1.5": "Overview of flats Sold by Flat Type",
        "plot_2": "Analysis of Resale Prices by Remaining Lease Period",
        "plot_5": "Overview of Resale Prices by region",
        "plot_6": "Impact of Storey Range on Resale Prices",
        "units_heatmap_static": "Heatmap of Resale Units by Year",
        "units_heatmap_range": "Heatmap of Resale Units by Year Range",
        "price_heatmap_static": "Heatmap of Average Resale Prices by Year",
        "price_heatmap_range": "Heatmap of Average Resale Prices by Year Range",
        "plot_3": "Comparing Monthly Rental Rates by Flat Type",
        "plot_4": "Rental Price Trends Across Towns"
    }
    plot_selection = {}
    dynamic_data_plots = {"plot_1", "plot_5","price_heatmap_static","price_heatmap_range","units_heatmap_static","units_heatmap_range"}
    for checkbox in cb_row:
        match checkbox:
            case "plot_0":
                st.markdown(
                    '<p style="color:orange; font-weight:bold;">HDB Resale Analysis</p>',
                    unsafe_allow_html=True,
                )
            case "plot_3":
                st.markdown(
                    '<p style="color:orange; font-weight:bold;">HDB Rental Analysis</p>',
                    unsafe_allow_html=True,
                )

        namecol, badgecol = st.columns([2, 1])
        with namecol:
            selected = st.checkbox(cb_row[checkbox], key=checkbox)
        with badgecol:
            if checkbox in dynamic_data_plots:
                renderBadge("slider_enabled")
            else:
                renderBadge("slider_none")
        plot_selection[checkbox] = selected

    st.text("")

    ############################
    if plot_selection["price_heatmap_static"] or plot_selection["units_heatmap_static"]:
        min_year = 1990
        max_year = 2023

        st.text("")
        yr_selector = st.slider(
            "Select year",
            min_value=min_year,
            max_value=max_year,
        )

        st.text("")
        
    if plot_selection["price_heatmap_range"] or plot_selection["units_heatmap_range"]:
        min_year = 1990
        max_year = 2023

        st.text("")
        ############################
        yr_range_selector = st.slider(
            "Select year",
            min_value=min_year,
            max_value=max_year,
            value = (min_year, max_year)
        )

def render_plot_main_title(plot_num):
    namecol, badgecol = st.columns([1.2, 1])
    dynamic_data_plots = {"plot_1", "plot_5"}
    with namecol:
        st.markdown(f"**{cb_row[plot_num]}**")
    with badgecol:
        if plot_num in dynamic_data_plots:
            renderBadge("slider_enabled")
        else:
            renderBadge("static")

# %% ####### ALL PLOT FUNCTIONS #######
        
def price_per_sqm_heatmap_single_year(data=hdb_mapping_price):
    m = leafmap.Map()
    m.add_basemap(basemap='TERRAIN')

    m.add_heatmap(data[data[str(yr_selector)] > 0], name =f"Average price/sqm in {yr_selector}", value = str(yr_selector), radius=10)

    return m
    # m.to_streamlit()

    
def price_per_sqm_heatmap_year_range(yr_range_selector, data=hdb_mapping_price):
    m = leafmap.Map()
    m.add_basemap(basemap='TERRAIN')

    ave_range = [str(i) for i in range(yr_range_selector[0], yr_range_selector[1]+1)]

    data['mean'] = data[ave_range].mean(axis=1)

    m.add_heatmap(data[data["mean"] > 0], name =f"Average price/sqm in {yr_range_selector[0]} - {yr_range_selector[0]}", value = "mean", radius=10)

    return m
    # m.to_streamlit()
    
def units_heatmap_single_year(yr_selector, data=hdb_mapping_units):
    m = leafmap.Map()
    m.add_basemap(basemap='TERRAIN')

    m.add_heatmap(data[data[str(yr_selector)] > 0], name =f"Number of units for resale in {yr_selector}", value = str(yr_selector), radius=10)

    return m
    # m.to_streamlit()

    
def units_heatmap_year_range(yr_range_selector, data=hdb_mapping_units):
    m = leafmap.Map()
    m.add_basemap(basemap='TERRAIN')

    ave_range = [str(i) for i in range(yr_range_selector[0], yr_range_selector[1]+1)]

    data['mean'] = data[ave_range].mean(axis=1)

    m.add_heatmap(data[data["mean"] > 0], name =f"Average number of units for resale in {yr_range_selector[0]} - {yr_range_selector[0]}", value = "mean", radius=10)

    return m
    # m.to_streamlit()


def add_map_layers(m):
    gdf = gpd.read_file("1-region.geojson")
    m.add_gdf(gdf.iloc[:1], layer_name="Central", style_function=central)
    m.add_gdf(gdf.iloc[1:2], layer_name="East", style_function=east)
    m.add_gdf(gdf.iloc[2:3], layer_name="North", style_function=north)
    m.add_gdf(gdf.iloc[3:4], layer_name="North-East", style_function=northeast)
    m.add_gdf(gdf.iloc[4:5], layer_name="West", style_function=west)

    m.add_markers_from_xy(mrt_mapping[mrt_mapping["type"] == "MRT"], x='lng', y='lat', icon="subway", 
                        icon_shape=None, border_color=None, border_width=0, layer_name="MRT Stations",
                        background_color="transparent")

#%%
if plot_selection["price_heatmap_static"]:
    render_plot_main_title("price_heatmap_static")
    m = price_per_sqm_heatmap_single_year()
    add_map_layers(m)
    # m.add_colormap()
    m.to_streamlit(width=900)

if plot_selection["price_heatmap_range"]:
    render_plot_main_title("price_heatmap_range")
    m = price_per_sqm_heatmap_year_range()
    add_map_layers(m)
    m.to_streamlit(width=900)

if plot_selection["units_heatmap_static"]:
    render_plot_main_title("units_heatmap_static")
    m = units_heatmap_single_year()
    add_map_layers(m)
    m.to_streamlit(width=900)

if plot_selection["units_heatmap_range"]:
    render_plot_main_title("units_heatmap_range")
    m = units_heatmap_year_range()
    add_map_layers(m)
    m.to_streamlit(width=900)

    