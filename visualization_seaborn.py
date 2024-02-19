import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st

# Set streamlit container = wide
# st.set_page_config(layout="wide")

@st.cache_data
def load_resales_data(file_name, mode):
    if mode == "load":
        return pd.read_csv(file_name)
    else:
        if file_name == "hdb_resales.csv":
            return pd.read_csv(file_name)[["flat_type", "floor_area_sqm"]]
        else:
            return pd.read_csv(file_name)[["flat_type", "price/sqm"]]

hdb_resales = load_resales_data("hdb_resales.csv", "load")
new_resales = load_resales_data("new_resales.csv", "load")
old_resales = load_resales_data("old_resales.csv", "load")
hdb_resales_drop_opt = load_resales_data("hdb_resales.csv", "load_opt")
new_resales_drop_opt = load_resales_data("new_resales.csv", "load_opt")
old_resales_drop_opt = load_resales_data("old_resales.csv", "load_opt")
 
year_cutoff = 2015 

for df in [hdb_resales, new_resales, old_resales]:
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m")
    df["region"] = pd.Categorical(
        df["region"], categories=["Central", "Northeast", "East", "West", "North"]
    )

# %%
"""Plotting price/sqm over the years"""
sns.set_context("paper", font_scale=0.8)
fig = px.scatter(
    hdb_resales,
    x="date",
    y="price/sqm",
    facet_row="flat_type_group",
    color="flat_type",
    category_orders={"flat_type": hdb_resales["flat_type"].value_counts().index},
    labels={"date": "Date", "price/sqm": "Price per sqm"},
    title="HDB Resales",
    width=800,
    height=1000,
)
fig.update_traces(marker_symbol="square")
fig.update_layout(height=800)
st.plotly_chart(fig)


# %%
""" Does Flat Type affect price/sqm? """
hdb_resales_drop_opt = hdb_resales[["flat_type", "floor_area_sqm"]]
new_resales_drop_opt = new_resales[["flat_type", "price/sqm"]]
old_resales_drop_opt = old_resales[["flat_type", "price/sqm"]]

@st.cache_data
def render_boxplot_px(data, x, y, title, height=600):
    fig = px.box(
        data_frame=data,
        x=x,
        y=y,
        color=x,
        points="outliers",
        title=title
    )
    fig.update_traces(marker=dict(size=5))
    fig.update_xaxes(tickangle=15)
    fig.update_layout(height=height)  
    st.plotly_chart(fig)
    
year_cutoff = 2015

# Splitting by hdb resales
render_boxplot_px(
    hdb_resales_drop_opt,
    "flat_type",
    "floor_area_sqm",
    "Distribution of house area for each flat type"
)
# Splitting by old resales
render_boxplot_px(
    new_resales_drop_opt,
    "flat_type",
    "price/sqm",
    f"Resales before {year_cutoff}"
)
# Splitting by new resales
render_boxplot_px(
    old_resales_drop_opt,
    "flat_type",
    "price/sqm",
    f"Resales after {year_cutoff}"
)
"""Very interesting reversal of trend in recent years. Before 2010 there is increasing premium"""
"""to a bigger house, nowadays there is a slight premium to small houses."""


# %%
""" Plotting Price/sqm against Remaining Lease """
fig = px.scatter(
    data_frame=new_resales,
    x="remaining_lease",
    y="price/sqm",
    color="flat_type_group",
    category_orders={"flat_type_group": new_resales["flat_type_group"].value_counts().index.tolist()},
    title=f"Price vs Remaining Lease after {year_cutoff}",
    hover_data=["flat_type_group", "remaining_lease", "price/sqm"],
    size_max=10, 
    labels={"remaining_lease": "Remaining Lease", "price/sqm": "Price per Sqm"}
)
fig.update_layout(
    legend=dict(title="Flat Type Group", orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
    coloraxis_colorbar=dict(title="Flat Type Group"),
    margin=dict(t=60, l=0, r=0, b=0) 
)
fig.update_traces(marker=dict(size=5, opacity=0.8, line=dict(width=0)))
fig.update_layout(autosize=True)
st.plotly_chart(fig, use_container_width=True)


# %%
""" Distribution of prices across different regionsa """
sorted_data = new_resales.sort_values(by=["region", "town"])
towns_sorted_by_region = sorted_data['town'].unique()
fig = px.box(
    data_frame=sorted_data,
    x="town",
    y="price/sqm",
    color="region",
    title=f"Resales after {year_cutoff}",
    category_orders={"town": towns_sorted_by_region}
)
fig.update_traces(marker=dict(size=4), width=0.6)
fig.update_layout(
    xaxis={'categoryorder': 'array', 'categoryarray': towns_sorted_by_region},
    xaxis_tickangle=90,
    legend_title_text='Region',
    legend=dict(yanchor="top", y=1, xanchor="right", x=1),
    autosize=False, 
    height=600
)
st.plotly_chart(fig, use_container_width=True)

# %%
""" Plotting price/sqm vs storey range """
fig = px.scatter(
    data_frame=new_resales,
    x="storey_range",
    y="price/sqm",
    color="flat_type_group",
    title=f"Resales after {year_cutoff}",
    color_discrete_sequence=px.colors.qualitative.G10
)
st.plotly_chart(fig, use_container_width=True)

"""Quite interesting: price does increase with height generally but not by much if below 40"""
# %%
