# %%
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd


# %% Styling
def central(feature):
    return {
        "stroke": True,
        "color": "rgb(56, 155, 232)",
        "weight": 3,
        "opacity": 1,
        "fill": True,
        "fillColor": "rgb(131, 201, 255)",
        "fillOpacity": 0.3,
    }


def north(feature):
    return {
        "stroke": True,
        "color": "rgb(196, 102, 102)",
        "weight": 3,
        "opacity": 1,
        "fill": True,
        "fillColor": "rgb(255, 171, 171)",
        "fillOpacity": 0.3,
    }


def west(feature):
    return {
        "stroke": True,
        "color": "rgb(49, 153, 82)",
        "weight": 3,
        "opacity": 1,
        "fill": True,
        "fillColor": "rgb(125, 239, 161)",
        "fillOpacity": 0.2,
    }


def east(feature):
    return {
        "stroke": True,
        "color": "rgb(0, 104, 201)",
        "weight": 3,
        "opacity": 1,
        "fill": True,
        "fillColor": "rgb(0, 104, 201)",
        "fillOpacity": 0.1,
    }


def northeast(feature):
    return {
        "stroke": True,
        "color": "rgb(255, 43, 43)",
        "weight": 3,
        "opacity": 1,
        "fill": True,
        "fillColor": "rgb(255, 43, 43)",
        "fillOpacity": 0.1,
    }


# %%
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


# %% ####### ALL PLOT FUNCTIONS #######


@st.cache_data
def price_per_sqm_heatmap_single_year(yr_selector, hdb_mapping_price):
    st.markdown(f"**Average Price/sqm ({yr_selector})**")
    m = leafmap.Map()
    m.add_basemap(basemap="TERRAIN")
    m.add_heatmap(
        hdb_mapping_price[hdb_mapping_price[str(yr_selector)] > 0],
        name=f"Average Price/sqm ({yr_selector})",
        value=str(yr_selector),
        radius=10,
    )

    return m
    # m.to_streamlit()


@st.cache_data
def price_per_sqm_heatmap_year_range(yr_range_selector, hdb_mapping_price):
    st.markdown(f"**Average price/sqm ({yr_range_selector[0]}-{yr_range_selector[1]})**")
    m = leafmap.Map()
    m.add_basemap(basemap="TERRAIN")
    ave_range = [str(i) for i in range(yr_range_selector[0], yr_range_selector[1] + 1)]
    hdb_mapping_price["mean"] = hdb_mapping_price[ave_range].mean(axis=1)
    m.add_heatmap(
        hdb_mapping_price[hdb_mapping_price["mean"] > 0],
        name=f"Average price/sqm ({yr_range_selector[0]}-{yr_range_selector[1]})",
        value="mean",
        radius=10,
    )
    return m
    # m.to_streamlit()


@st.cache_data
def units_heatmap_single_year(yr_selector, hdb_mapping_units):
    st.markdown(f"**Quantity of Resale Units ({yr_selector})**")
    m = leafmap.Map()
    m.add_basemap(basemap="TERRAIN")
    m.add_heatmap(
        hdb_mapping_units[hdb_mapping_units[str(yr_selector)] > 0],
        name=f"Quantity of Resale Units ({yr_selector})",
        value=str(yr_selector),
        radius=10,
    )

    return m
    # m.to_streamlit()


@st.cache_data
def units_heatmap_year_range(yr_range_selector, hdb_mapping_units):
    st.markdown(
        f"**Average number of units for resale ({yr_range_selector[0]}-{yr_range_selector[1]})**"
    )
    m = leafmap.Map()
    m.add_basemap(basemap="TERRAIN")
    ave_range = [str(i) for i in range(yr_range_selector[0], yr_range_selector[1] + 1)]
    hdb_mapping_units["mean"] = hdb_mapping_units[ave_range].mean(axis=1)
    m.add_heatmap(
        hdb_mapping_units[hdb_mapping_units["mean"] > 0],
        name=f"Average number of units for resale ({yr_range_selector[0]}-{yr_range_selector[1]})",
        value="mean",
        radius=10,
    )

    return m
    # m.to_streamlit()


def add_map_layers(m, mrt_mapping):
    gdf = gpd.read_file("1-region.geojson")
    m.add_gdf(gdf.iloc[:1], layer_name="Central", style_function=central)
    m.add_gdf(gdf.iloc[1:2], layer_name="East", style_function=east)
    m.add_gdf(gdf.iloc[2:3], layer_name="North", style_function=north)
    m.add_gdf(gdf.iloc[3:4], layer_name="North-East", style_function=northeast)
    m.add_gdf(gdf.iloc[4:5], layer_name="West", style_function=west)

    m.add_markers_from_xy(
        mrt_mapping[mrt_mapping["type"] == "MRT"],
        x="lng",
        y="lat",
        icon="subway",
        icon_shape=None,
        border_color=None,
        border_width=0,
        layer_name="MRT Stations",
        background_color="transparent",
    )
