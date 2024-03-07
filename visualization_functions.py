import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st

# Set streamlit container = wide
# st.set_page_config(layout="wide")


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


@st.cache_data
def date_modify_add(datafr):
    datafr["date"] = pd.to_datetime(datafr["date"], format="%Y-%m")
    datafr["month"] = datafr["date"].dt.month
    datafr["region"] = pd.Categorical(
        datafr["region"], categories=["Central", "Northeast", "East", "West", "North"]
    )
    return datafr


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
    dynamic_data_plots = {
        "plot_1",
        "plot_5",
        "units_heatmap_static",
        "units_heatmap_range",
        "price_heatmap_static",
        "price_heatmap_range",
    }
    cb_row = {
        "plot_0": "Distribution of Resale Prices Across Years",
        "plot_1": "Comparison of Resale Prices by Flat Type",
        "plot_1.5": "Overview of Flats Sold by Flat Type",
        "plot_2": "Analysis of Resale Prices by Remaining Lease Period",
        "plot_5": "Overview of Resale Prices by region",
        "plot_6": "Impact of Storey Range on Resale Prices",
        "plot_3": "Comparing Monthly Rental Rates by Flat Type",
        "plot_4": "Rental Price Trends Across Towns",
        "units_heatmap_static": "Heatmap of Resale Units by Year",
        "units_heatmap_range": "Heatmap of Resale Units by Year Range",
        "price_heatmap_static": "Heatmap of Average Resale Prices by Year",
        "price_heatmap_range": "Heatmap of Average Resale Prices by Year Range",
    }
    with namecol:
        st.markdown(f"**{cb_row[plot_num]}**")
    with badgecol:
        if plot_num in dynamic_data_plots:
            renderBadge("slider_enabled")
        else:
            renderBadge("static")


# %% ## SIDE NAV BAR ##
def render_sidebar(
    hdb_resales,
    new_resales,
    old_resales,
    hdb_resales_drop_opt,
    new_resales_drop_opt,
    old_resales_drop_opt,
):
    min_year = 0
    max_year = 0
    yr_selector = 0  # for map
    yr_range_selector = 0  # for plot (float) or map (array)
    last_year_of_interval = 0
    selected_resale_data = ""
    resale_data_selected = pd.DataFrame()
    resales_data_opt_selected = pd.DataFrame()
    filtered_resale_data = pd.DataFrame()
    filtered_resale_opt_selected = pd.DataFrame()

    with st.sidebar:
        st.markdown(
            """
        <div style="background-color: #0e1117; margin-bottom: -30px; padding-left: 5px; width: auto; border: 1px; border-radius: 10px; ">
            <h4 style="color: white; margin: 0; padding: 8px 0px 8px 8px">Select Visualization Mode:</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )
        visualization_mode = st.radio(
            "mode select",
            ("Data analysis (plot)", "Geospatial analysis (map)"),
            horizontal=True,
            label_visibility="hidden",
        )

        st.markdown(
            """
        <div style="background-color: #0e1117; margin-bottom: 20px; padding-left: 5px; width: auto; border: 1px; border-radius: 10px; ">
            <h4 style="color: white; margin: 0; padding: 8px 0px 8px 8px">Select Plots To Display</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if visualization_mode == "Data analysis (plot)":
            cb_row = {
                "plot_0": "Distribution of Resale Prices Across Years",
                "plot_1": "Comparison of Resale Prices by Flat Type",
                "plot_1.5": "Overview of Flats Sold by Flat Type",
                "plot_2": "Analysis of Resale Prices by Remaining Lease Period",
                "plot_5": "Overview of Resale Prices by region",
                "plot_6": "Impact of Storey Range on Resale Prices",
                "plot_3": "Comparing Monthly Rental Rates by Flat Type",
                "plot_4": "Rental Price Trends Across Towns",
            }
        else:
            cb_row = {
                "units_heatmap_static": "Overview of Resale Units Per Year",
                "units_heatmap_range": "Overview of Resale Units Across Years",
                "price_heatmap_static": "Analysis of Average Resale Price Per year",
                "price_heatmap_range": "Analysis of Average Resale Price Across Years",
            }
        plot_selection = {}
        dynamic_data_plots = {
            "plot_1",
            "plot_5",
            "price_heatmap_static",
            "price_heatmap_range",
            "units_heatmap_static",
            "units_heatmap_range",
        }
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
        if visualization_mode == "Data analysis (plot)":
            if plot_selection["plot_1"] or plot_selection["plot_5"]:
                options = {
                    "all resales (1990-2023)": "all",
                    "old resales (1990-2015)": "old",
                    "new resales 2016-2023": "new",
                }
                st.text("")
                selected_resale_data = st.selectbox(
                    "Select dataset", list(options.keys())
                )

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
                    5
                    if max_year - yr_range_selector >= 5
                    else max_year - yr_range_selector
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
                #
        else:
            if (
                plot_selection["price_heatmap_static"]
                or plot_selection["units_heatmap_static"]
            ):
                min_year = 1990
                max_year = 2023
                st.text("")
                yr_selector = st.slider(
                    "Select Specific Year",
                    min_value=min_year,
                    max_value=max_year,
                )

            if (
                plot_selection["price_heatmap_range"]
                or plot_selection["units_heatmap_range"]
            ):
                min_year = 1990
                max_year = 2023
                st.text("")
                ############################
                yr_range_selector = st.slider(
                    "Select Year Range",
                    min_value=min_year,
                    max_value=max_year,
                    value=(min_year, max_year),
                )
    return {
        "plot_selection": plot_selection,
        "visualization_mode": visualization_mode,
        "cb_row": cb_row,
        "min_year": min_year,
        "max_year": max_year,
        "yr_selector": yr_selector,
        "yr_range_selector": yr_range_selector,
        "last_year_of_interval": last_year_of_interval,
        "selected_resale_data": selected_resale_data,
        "resale_data_selected": resale_data_selected,
        "resales_data_opt_selected": resales_data_opt_selected,
        "filtered_resale_data": filtered_resale_data,
        "filtered_resale_opt_selected": filtered_resale_opt_selected,
    }


# %% ####### ALL PLOT FUNCTIONS #######
# Distribution plot of price/sqm vs years (static, all)
@st.cache_data
def scatter_psqmvd(hdb_resales):
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


# Plotting no. of flats sold vs flat type (static)
@st.cache_data
def line_fsvft(new_resales):
    flattype_trend = (
        new_resales[["date", "flat_type"]].value_counts().reset_index(name="count")
    )
    flattype_trend_pivot = (
        flattype_trend.pivot(index="date", columns="flat_type", values="count")
        .fillna(0)
        .reset_index()
    )
    flattype_trend_long = flattype_trend_pivot.melt(
        id_vars=["date"], var_name="flat_type", value_name="count"
    )
    fig = px.line(
        flattype_trend_long,
        x="date",
        y="count",
        color="flat_type",
        title="Plot of flats sold vs flat type (2016-2023)",
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Count",
        legend_title="Flat Type",
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)


# Plotting price/sqm vs Remaining Lease (static)
@st.cache_data
def scatter_psqmvrl(new_resales):
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
@st.cache_data()
def box_mrvft(hdb_rentals):
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
@st.cache_data()
def box_mrvt(hdb_rentals):
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
@st.cache_data()
def box_psqmvt(filtered_resale_data, yr_range_selector, last_year_of_interval):
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
@st.cache_data()
def scatter_psqmvsr(new_resales):
    fig = px.scatter(
        data_frame=new_resales,
        x="storey_range",
        y="price/sqm",
        color="flat_type_group",
        title="Resales from 2016 to 2023",
        color_discrete_sequence=px.colors.qualitative.G10,
    )
    st.plotly_chart(fig, use_container_width=True)
