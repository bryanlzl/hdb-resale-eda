import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st

# Set streamlit container = wide
# st.set_page_config(layout="wide")

year_cutoff = 2016


# %% ## Data pre-loading ##
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
            return pd.read_csv("hdb_resales.csv")[
                ["flat_type", "floor_area_sqm", "year"]
            ]
        elif file_name == "hdb_resales_psqmvft.csv":
            return pd.read_csv("hdb_resales.csv")[["flat_type", "price/sqm", "year"]]
        else:
            return pd.read_csv(file_name)[["flat_type", "price/sqm", "year"]]


hdb_rentals = pd.read_csv("hdb_rentals.csv")
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


# %% ## Badge renders ##
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


# %% ## SIDE NAV BAR ##
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
        "plot_2": "Analysis of Resale Prices by Remaining Lease Period",
        "plot_5": "Overview of Resale Prices by region",
        "plot_6": "Impact of Storey Range on Resale Prices",
        "plot_3": "Comparing Monthly Rental Rates by Flat Type",
        "plot_4": "Rental Price Trends Across Towns",
    }
    plot_selection = {}
    dynamic_data_plots = {"plot_1", "plot_5"}
    for checkbox in cb_row:
        match checkbox:
            case "plot_0":
                st.markdown(
                    '<p style="color:orange; font-weight:bold;">HDB Rental Analysis</p>',
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
    if plot_selection["plot_1"] or plot_selection["plot_5"]:
        options = {
            "all resales (1990-2023)": "all",
            "old resales (1990-2015)": "old",
            "new resales 2016-2023": "new",
        }
        selected_resale_data = st.selectbox("Select dataset", list(options.keys()))

        st.text("")
        ############################
        min_year = (
            1990
            if (
                options[selected_resale_data] == "all"
                or options[selected_resale_data] == "old"
            )
            else 2016
        )
        max_year = 2015 if options[selected_resale_data] == "old" else 2023

        st.text("")
        ############################
        yr_range_selector = st.slider(
            "Select 5-year range",
            min_value=min_year,
            max_value=max_year,
            step=5,
        )

        st.text("")
        ############################

        # %%
        yr_range_selector = (
            yr_range_selector if yr_range_selector <= max_year else max_year
        )
        last_year_of_interval = yr_range_selector + (
            5 if max_year - yr_range_selector >= 5 else max_year - yr_range_selector
        )

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
            (resale_data_selected["year"] >= yr_range_selector)
            & (resale_data_selected["year"] <= last_year_of_interval)
        ]
        filtered_resale_opt_selected = resales_data_opt_selected[
            (resales_data_opt_selected["year"] >= yr_range_selector)
            & (resales_data_opt_selected["year"] <= last_year_of_interval)
        ]

        # selected_year_resale_data = filtered_resale_data[
        #     filtered_resale_data["year"] == full_yr_selector
        # ]


# %% ####### ALL PLOT FUNCTIONS #######
# Distribution plot of price/sqm vs years (static, all)
@st.cache_data
def scatter_psqmvd():
    sns.set_context("paper", font_scale=0.8)
    fig = px.scatter(
        hdb_resales,
        x="date",
        y="price/sqm",
        facet_row="flat_type_group",
        color="flat_type",
        category_orders={"flat_type": hdb_resales["flat_type"].value_counts().index},
        labels={"date": "Date", "price/sqm": "Price per sqm"},
        title="Plotting price/sqm over the years (1990-2023)",
        width=800,
        height=1000,
    )
    fig.update_traces(marker_symbol="square")
    fig.update_layout(height=800)
    st.plotly_chart(fig)


# Plotting floor_area_sqm vs flat type (static, all)
# Plotting price/sqm vs flat type (dynamic, select 5-year range)
@st.cache_data
def box_psqmvft(data, x, y, title, height=600):
    fig = px.box(data_frame=data, x=x, y=y, color=x, points="outliers", title=title)
    fig.update_traces(marker=dict(size=5))
    fig.update_xaxes(tickangle=15)
    fig.update_layout(height=height)
    st.plotly_chart(fig)


# Plotting price/sqm vs Remaining Lease (static)
st.cache_data()


def scatter_psqmvrl():
    fig = px.scatter(
        data_frame=new_resales,
        x="remaining_lease",
        y="price/sqm",
        color="flat_type_group",
        category_orders={
            "flat_type_group": new_resales["flat_type_group"]
            .value_counts()
            .index.tolist()
        },
        title="Plot of price/sqm vs remaining lease (2016-2023)",
        hover_data=["flat_type_group", "remaining_lease", "price/sqm"],
        size_max=10,
        labels={"remaining_lease": "Remaining Lease", "price/sqm": "Price per Sqm"},
    )
    fig.update_layout(
        legend=dict(
            title="Flat Type Group",
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
        ),
        coloraxis_colorbar=dict(title="Flat Type Group"),
        margin=dict(t=60, l=0, r=0, b=0),
        autosize=True,
    )
    fig.update_traces(marker=dict(size=5, opacity=0.8, line=dict(width=0)))
    fig.update_layout(autosize=True)
    st.plotly_chart(fig, use_container_width=True)


# Rental plot of monthly rent vs flat type
st.cache_data()


def box_mrvft():
    hdb_rentals.sort_values(by=["flat_type"], inplace=True)
    fig = px.box(
        hdb_rentals,
        x="flat_type",
        y="monthly_rent",
        color="flat_type",
        category_orders={
            "flat_type": ["1-room", "2-room", "3-room", "4-room", "5-room", "Executive"]
        },
        title="Plot of monthly rent vs flat type (2021-2023)",
    )
    st.plotly_chart(fig)


# Rental plot of monthly rent vs town
st.cache_data()


def box_mrvt():
    hdb_rentals.sort_values(by=["region", "town"], inplace=True)
    hdb_rentals.dropna(subset=["town", "region"], inplace=True)
    hdb_rentals["town"] = hdb_rentals["town"].astype(str)
    hdb_rentals["region"] = hdb_rentals["region"].astype(str)
    # category_orders = {
    #     "region": sorted(hdb_rentals["region"].unique()),
    #     "town": sorted(hdb_rentals["town"].unique()),
    # }
    fig = px.box(
        hdb_rentals,
        x="town",
        y="monthly_rent",
        color="region",
        title="Plot of monthly rent vs town (2021-2023)",
        # category_orders=category_orders,
    )

    fig.update_layout(
        # xaxis={"categoryorder": "array", "categoryarray": category_orders["town"]},
        xaxis_title="Town",
        yaxis_title="Monthly Rent",
        legend_title="Region",
        xaxis_tickangle=-45,
    )
    st.plotly_chart(fig)


# Distribution plot of price/sqm vs different regions (dynamic, select 5-year range)
st.cache_data()


def box_psqmvt():
    sorted_data = filtered_resale_data.sort_values(by=["region", "town"])
    towns_sorted_by_region = sorted_data["town"].unique()
    fig = px.box(
        data_frame=sorted_data,
        x="town",
        y="price/sqm",
        color="region",
        title=f"Plot of price/sqm vs region ({yr_range_selector}-{last_year_of_interval})",
        category_orders={"town": towns_sorted_by_region},
    )
    fig.update_traces(marker=dict(size=4), width=0.6)
    fig.update_layout(
        xaxis={"categoryorder": "array", "categoryarray": towns_sorted_by_region},
        xaxis_tickangle=90,
        legend_title_text="Region",
        legend=dict(yanchor="top", y=1, xanchor="right", x=1),
        autosize=False,
        height=600,
    )
    st.plotly_chart(fig, use_container_width=True)


# Plotting price/sqm vs storey range (static)
st.cache_data()


def scatter_psqmvsr():
    fig = px.scatter(
        data_frame=new_resales,
        x="storey_range",
        y="price/sqm",
        color="flat_type_group",
        title="Resales from 2016 to 2023",
        color_discrete_sequence=px.colors.qualitative.G10,
    )
    st.plotly_chart(fig, use_container_width=True)


# %%
if plot_selection["plot_0"]:
    render_plot_main_title("plot_0")
    scatter_psqmvd()
    """ We observe a strongly increasing price trend over the last 35 years, ranging from 5x to 15x increases (corresponding to about 20% annualized return!). """
    """ The smaller the apartments, the higher the rate of inflation. """
    """ We further observe some local highs at 1997 (Asian Financial Crisis) and 2013 (Cooling measures), as well as a marked pickup in prices post 2020 during the COVID period. """
    st.markdown("""---""")

# %%
if plot_selection["plot_1"]:
    render_plot_main_title("plot_1")
    """ Does Flat Type affect price/sqm? """
    box_psqmvft(
        filtered_resale_data,
        "flat_type",
        "price/sqm",
        f"Plot of price/sqm vs flat type ({yr_range_selector}-{last_year_of_interval})"
        if options[selected_resale_data] == "all"
        else f"Resales before {min_year}"
        if options[selected_resale_data] == "new"
        else f"Resales after {min_year}",
    )
    """ Normalized prices are generally invariant across flat sizes today. """
    """ Interstingly, before 2010, there was an increasing premium to larger houses; however, this trend reversed and today there is a slight premium for smaller houses (1 and 2-room flats). """
    """ We can visualize this distribution for specific years using the year slider. """
    st.markdown("""---""")

    st.markdown("**Comparison of floor area (sqm) by Flat Type**")
    if options[selected_resale_data] == "all":
        box_psqmvft(
            hdb_resales_drop_opt_fasqmvft,
            "flat_type",
            "floor_area_sqm",
            "Plot of floor area (sqm) vs flat type (2016-2023)",
        )
        """ 3 room flats have large positive outliers due to luxury 3 room apartments. """
        """ Those are mostly ground floor or penthouse apartments with large rooms, balconies, and/or patios. """

    st.markdown("""---""")

# %%
if plot_selection["plot_2"]:
    render_plot_main_title("plot_2")
    # Draw the plot with filtered data

    scatter_psqmvrl()
    """For 2016 onwards, generally increasing trend as expected, although seems to taper off when remaining lease reaches ~80 years"""
    # Can use scatterplot for streamlit, for static graph displot seems better
    st.markdown("""---""")

# %%
if plot_selection["plot_5"]:
    render_plot_main_title("plot_5")

    box_psqmvt()
    """ From 1990 - 2015, Punggol resale prices were the highest among all towns due its underdeveloped nature and low flat count (increase demand) as well as the 1996 gov-backed Punggol 21 masterplan which raised speculative property value and prices in the area. """
    """ From 2016 - 2023, Central areas are more expensive than the rest due to accessibility to work. """
    """ The remaining residential areas have less variance, slight differences might be due to popularity, access to amenities, or distance from the airport."""
    st.markdown("""---""")

# %%
if plot_selection["plot_6"]:
    render_plot_main_title("plot_6")

    scatter_psqmvsr()
    """ For newer resales, price does increase with floor height generally but not by much if below 40 storeys. """
    st.markdown("""---""")

# %%
if plot_selection["plot_3"]:
    render_plot_main_title("plot_3")

    box_mrvft()
    """Generally increasing rental with size as expected"""
    st.markdown("""---""")

# %%
if plot_selection["plot_4"]:
    render_plot_main_title("plot_4")

    box_mrvt()
    """ Surprisingly, rentals are quite invariant across regions. """
    st.markdown("""---""")
