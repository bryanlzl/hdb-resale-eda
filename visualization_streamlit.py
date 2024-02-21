import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st

# Set streamlit container = wide
# st.set_page_config(layout="wide")

year_cutoff = 2015

@st.cache_data
def load_resales_data(file_name, mode):
    if mode == "load":
        return pd.read_csv(file_name)[
            [
                "year",
                "date",
                "price/sqm",
                "flat_type_group",
                "flat_type",
                "remaining_lease",
                "town",
                "region",
                "storey_range",
            ]
        ]
    else:
        if file_name == "hdb_resales_fasqmvft.csv":
            return pd.read_csv("hdb_resales.csv")[["flat_type", "floor_area_sqm", "year"]]
        elif file_name == "hdb_resales_psqmvft.csv":
            return pd.read_csv("hdb_resales.csv")[["flat_type", "price/sqm", "year"]]
        else:
            return pd.read_csv(file_name)[["flat_type", "price/sqm", "year"]]

hdb_rentals = pd.read_csv('hdb_rentals.csv')
hdb_resales = load_resales_data("hdb_resales.csv", "load")
new_resales = load_resales_data("new_resales.csv", "load")
old_resales = load_resales_data("old_resales.csv", "load")
hdb_resales_drop_opt_fasqmvft = load_resales_data(
    "hdb_resales_fasqmvft.csv", "load_opt"
)
hdb_resales_drop_opt = load_resales_data("hdb_resales_psqmvft.csv", "load_opt")
new_resales_drop_opt = load_resales_data("new_resales.csv", "load_opt")
old_resales_drop_opt = load_resales_data("old_resales.csv", "load_opt")


@st.cache_data
def date_modify_add(datafr):
    datafr["date"] = pd.to_datetime(datafr["date"], format="%Y-%m")
    datafr["month"] = datafr["date"].dt.month
    datafr["region"] = pd.Categorical(
        datafr["region"], categories=["Central", "Northeast", "East", "West", "North"]
    )
    return datafr

for i in range(len([hdb_resales, new_resales, old_resales])):
    [hdb_resales, new_resales, old_resales][i] = date_modify_add(
        [hdb_resales, new_resales, old_resales][i]
    )

# %%
## SIDE NAV BAR ##
with st.sidebar:
    options = {"all resales": "all", "old resales": "old", "new resales": "new"}
    selected_resale_data = st.selectbox("Select dataset", list(options.keys()))

    st.text("")
    ############################
    min_year = 1990 if (options[selected_resale_data] == "all" or options[selected_resale_data] == "old") else 2016
    max_year = 2015 if options[selected_resale_data] == "old" else 2023
    year_cutoff = st.slider(
        "Select cutoff year", min_value=min_year, max_value=max_year, value=min_year, step=1
    )
        
    st.text("")
    ############################
    yr_range_selector = st.slider(
        "Select Year Range", min_value=year_cutoff, max_value=max_year, value=(year_cutoff, max_year)
    )
    #st.write(f"Selected year range {yr_range_selector[0]} - {yr_range_selector[1]}")

    st.text("")
    ############################
    full_yr_selector = st.slider(
        "Select Year", min_value=year_cutoff, max_value=max_year, value=year_cutoff, step=1
    )
    
    st.text("")
    ############################
    st.write("Select plots to display")
    col1, col2 = st.columns(2)
    cb_row_1 = {"plot_0": "Dist. plot of price/sqm vs years", "plot_1": "Plot price/sqm vs flat type", "plot_2": "Plot price/sqm vs Remaining Lease", "plot_3":"Plot of monthly rent vs flat type"}
    cb_row_2 = {"plot_4": "Plot monthly rent vs town", "plot_5": "Dist. plot of price/sqm vs different regions", "plot_6": "Plot price/sqm vs storey range"}
    plot_selection = {}
    with col1:
        for checkbox in cb_row_1:
            selected = st.checkbox(cb_row_1[checkbox], key=checkbox)
            plot_selection[checkbox] = selected
    with col2:
        for checkbox in cb_row_2:
            selected = st.checkbox(cb_row_2[checkbox], key=checkbox)
            plot_selection[checkbox] = selected
    
# %%
resale_data_selected = (
    hdb_resales
    if options[selected_resale_data] == "all"
    else new_resales
    if options[selected_resale_data] == "new"
    else old_resales
)

resales_data_opt_selected = (
    hdb_resales_drop_opt
    if options[selected_resale_data] == "all"
    else new_resales_drop_opt
    if options[selected_resale_data] == "new"
    else old_resales_drop_opt
)

filtered_resale_data = resale_data_selected[
    (resale_data_selected["year"] >= yr_range_selector[0])
    & (resale_data_selected["year"] <= yr_range_selector[1])
]

filtered_resale_opt_selected = resales_data_opt_selected[
    (resales_data_opt_selected["year"] >= yr_range_selector[0])
    & (resales_data_opt_selected["year"] <= yr_range_selector[1])
]

selected_year_resale_data = filtered_resale_data[filtered_resale_data["year"] == full_yr_selector]

#%% ####### ALL PLOT FUNCTIONS #######
#Distribution plot of price/sqm vs years
@st.cache_data
def scatter_psqmvd():
    sns.set_context("paper", font_scale=0.8)
    fig = px.scatter(
        resale_data_selected,
        x="date",
        y="price/sqm",
        facet_row="flat_type_group",
        color="flat_type",
        category_orders={
            "flat_type": resale_data_selected["flat_type"].value_counts().index
        },
        labels={"date": "Date", "price/sqm": "Price per sqm"},
        title="HDB Resales",
        width=800,
        height=1000,
    )
    fig.update_traces(marker_symbol="square")
    fig.update_layout(height=800)
    st.plotly_chart(fig)

#Plotting floor_area_sqm vs flat type
#Plotting price/sqm vs flat type
@st.cache_data
def box_psqmvft(data, x, y, title, height=600):
    fig = px.box(data_frame=data, x=x, y=y, color=x, points="outliers", title=title)
    fig.update_traces(marker=dict(size=5))
    fig.update_xaxes(tickangle=15)
    fig.update_layout(height=height)
    st.plotly_chart(fig)

#Plotting price/sqm vs Remaining Lease
st.cache_data()
def scatter_psqmvrl():
    fig = px.scatter(
        data_frame=resale_data_selected,
        x="remaining_lease",
        y="price/sqm",
        color="flat_type_group",
        category_orders={"flat_type_group": resale_data_selected["flat_type_group"].value_counts().index.tolist()},
        title=f"Price vs Remaining Lease after {year_cutoff}",
        hover_data=["flat_type_group", "remaining_lease", "price/sqm"],
        size_max=10,
        labels={"remaining_lease": "Remaining Lease", "price/sqm": "Price per Sqm"}
    )
    fig.update_layout(
        legend=dict(title="Flat Type Group", orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        coloraxis_colorbar=dict(title="Flat Type Group"),
        margin=dict(t=60, l=0, r=0, b=0),
        autosize=True
    )
    fig.update_traces(marker=dict(size=5, opacity=0.8, line=dict(width=0)))
    fig.update_layout(autosize=True)
    st.plotly_chart(fig, use_container_width=True)

# Rental plot of monthly rent vs flat type
st.cache_data()
def box_mrvft():
    fig = px.box(hdb_rentals, x='flat_type', y='monthly_rent',
                 color="flat_type",
                category_orders={'flat_type': ['1-room', '2-room', '3-room', '4-room', '5-room', 'Executive']},
                title='HDB Rental Prices (2021-2023)')
    st.plotly_chart(fig)

# Plotting monthly rent vs town
st.cache_data()
def box_mrvt():
    hdb_rentals.dropna(subset=['town', 'region'], inplace=True)
    hdb_rentals['town'] = hdb_rentals['town'].astype(str)
    hdb_rentals['region'] = hdb_rentals['region'].astype(str)
    category_orders = {
        'town': sorted(hdb_rentals['town'].unique()),
        'region': sorted(hdb_rentals['region'].unique())
    }
    fig = px.box(hdb_rentals, x='town', y='monthly_rent', color='region',
                title='HDB Rental Prices (2021-2023)',
                category_orders=category_orders)

    fig.update_layout(xaxis={'categoryorder':'array', 
                            'categoryarray': category_orders['town']},
                    xaxis_title="Town",
                    yaxis_title="Monthly Rent",
                    legend_title="Region",
                    xaxis_tickangle=-45)
    st.plotly_chart(fig)
    
# Distribution plot of price/sqm vs different regions
st.cache_data()
def box_psqmvt():
    sorted_data = filtered_resale_data.sort_values(by=["region", "town"])
    towns_sorted_by_region = sorted_data['town'].unique()
    fig = px.box(
        data_frame=sorted_data,
        x="town",
        y="price/sqm",
        color="region",
        title=f"Resales from {year_cutoff} to {max_year}",
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

# Plotting price/sqm vs storey range
st.cache_data()
def scatter_psqmvsr():
    fig = px.scatter(
        data_frame=filtered_resale_data,
        x="storey_range",
        y="price/sqm",
        color="flat_type_group",
        title=f"Resales from {year_cutoff} to {max_year}",
        color_discrete_sequence=px.colors.qualitative.G10
    )
    st.plotly_chart(fig, use_container_width=True)


#%%
if plot_selection["plot_0"]:
    """Plotting price/sqm over the years"""
    scatter_psqmvd()
    """ We observe a strongly increasing price trend over the last 35 years, ranging from 5x to 15x increases (corresponding to about 20% annualized return!). """
    """ The smaller the apartments, the higher the rate of inflation. """
    """ We further observe some local highs at 1997 (Asian Financial Crisis) and 2013 (Cooling measures), as well as a marked pickup in prices post 2020 during the COVID period. """
    st.markdown("""---""")


# %%
if plot_selection["plot_1"]:
    """ Plotting price/sqm over flat type """
    """ Does Flat Type affect price/sqm? """
    box_psqmvft(
        filtered_resale_opt_selected,
        "flat_type",
        "price/sqm",
        f"Resale price for each flat type ({yr_range_selector[0]}-{yr_range_selector[1]})" 
        if options[selected_resale_data] == "all"
        else f"Resales before {year_cutoff}"
        if options[selected_resale_data] == "new"
        else f"Resales after {year_cutoff}"
    )
    
    """ Plotting floor_area_sqm over flat type """
    if options[selected_resale_data] == "all":
        box_psqmvft(
            hdb_resales_drop_opt_fasqmvft,
            "flat_type",
            "floor_area_sqm",
            f"Distribution of house area for each flat type ({yr_range_selector[0]}-{yr_range_selector[1]})"
        )
        """ 3 room flats have large positive outliers due to luxury 3 room apartments. """
        """ Those are mostly ground floor or penthouse apartments with large rooms, balconies, and/or patios. """
        
    """ Normalized prices are generally invariant across flat sizes today. """
    """ Interstingly, before 2010, there was an increasing premium to larger houses; however, this trend reversed and today there is a slight premium for smaller houses (1 and 2-room flats). """
    """ We can visualize this distribution for specific years using the year slider. """
    st.markdown("""---""")

# %%
if plot_selection["plot_2"]:
    """ Plotting Price/sqm against Remaining Lease """
    # Draw the plot with filtered data

    scatter_psqmvrl()
    """For 2016 onwards, generally increasing trend as expected, although seems to taper off when remaining lease reaches ~80 years"""
    #Can use scatterplot for streamlit, for static graph displot seems better
    st.markdown("""---""")

#%%
if plot_selection["plot_3"]:
    """ Plot of monthly rent vs flat type (Rental)"""

    box_mrvft()
    """Generally increasing rental with size as expected"""
    st.markdown("""---""")

#%%
if plot_selection["plot_4"]:
    """ Plotting monthly rent over town"""

    box_mrvt()
    """ Surprisingly, rentals are quite invariant across regions. """
    st.markdown("""---""")

#%%
if plot_selection["plot_5"]:
    """ Distribution of prices across different regions """

    box_psqmvt()
    """ From 1990 - 2015, Punggol resale prices were the highest among all towns due its underdeveloped nature and low flat count (increase demand) as well as the 1996 gov-backed Punggol 21 masterplan which raised speculative property value and prices in the area. """
    """ From 2016 - 2023, Central areas are more expensive than the rest due to accessibility to work. """
    """ The remaining residential areas have less variance, slight differences might be due to popularity, access to amenities, or distance from the airport."""
    st.markdown("""---""")

# %%
if plot_selection["plot_6"]:
    """ Plotting price/sqm vs storey range """

    scatter_psqmvsr()
    """ For newer resales, price does increase with floor height generally but not by much if below 40 storeys. """
    st.markdown("""---""")
