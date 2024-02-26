import pandas as pd
import streamlit as st
from visualization_functions import (
    load_resales_data,
    date_modify_add,
    render_plot_main_title,
    render_sidebar,
    renderBadge,
    scatter_psqmvd,
    box_psqmvft,
    line_fsvft,
    scatter_psqmvrl,
    box_mrvft,
    box_mrvt,
    box_psqmvt,
    scatter_psqmvsr,
)
from visualization_map_functions import (
    price_per_sqm_heatmap_single_year,
    price_per_sqm_heatmap_year_range,
    units_heatmap_single_year,
    units_heatmap_year_range,
    add_map_layers,
)

year_cutoff = 2016

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

hdb_mapping_price = pd.read_csv("hdb_mapping_price_per_sqm.csv")
hdb_mapping_units = pd.read_csv("hdb_mapping_units.csv")
mrt_mapping = pd.read_csv("mrt_lrt_data.csv")

# some missing lat/lng, need to filter and re-update
hdb_mapping_price = hdb_mapping_price[hdb_mapping_price["latitude"] > 0]
hdb_mapping_units = hdb_mapping_units[hdb_mapping_units["latitude"] > 0]

for i in range(len([hdb_resales, new_resales, old_resales])):
    [hdb_resales, new_resales, old_resales][i] = date_modify_add(
        [hdb_resales, new_resales, old_resales][i]
    )

(
    plot_selection,
    visualization_mode,
    cb_row,
    min_year,
    max_year,
    yr_selector,
    yr_range_selector,
    last_year_of_interval,
    selected_resale_data,
    resale_data_selected,
    resales_data_opt_selected,
    filtered_resale_data,
    filtered_resale_opt_selected,
) = render_sidebar(
    hdb_resales,
    new_resales,
    old_resales,
    hdb_resales_drop_opt,
    new_resales_drop_opt,
    old_resales_drop_opt,
).values()

options = {
    "all resales (1990-2023)": "all",
    "old resales (1990-2015)": "old",
    "new resales 2016-2023": "new",
}

if visualization_mode == "Data analysis (plot)":
    if plot_selection["plot_0"]:
        render_plot_main_title("plot_0")
        scatter_psqmvd(hdb_resales)
        """ We observe a strongly increasing price trend over the last 35 years, ranging from 5x to 15x increases (corresponding to about 20% annualized return!). """
        """ The smaller the apartments, the higher the rate of inflation. """
        """ We further observe some local highs at 1997 (Asian Financial Crisis) and 2013 (Cooling measures), as well as a marked pickup in prices post 2020 during the COVID period. """
        st.markdown("""---""")

    if plot_selection["plot_1"]:
        render_plot_main_title("plot_1")
        """ Does Flat Type affect price/sqm? """
        box_psqmvft(
            filtered_resale_data,
            "flat_type",
            "price/sqm",
            f"Plot of price/sqm vs flat type ({yr_range_selector}-{last_year_of_interval})"
        )
        """ Normalized prices are generally invariant across flat sizes today. """
        """ Interstingly, before 2010, there was an increasing premium to larger houses; however, this trend reversed and today there is a slight premium for smaller houses (1 and 2-room flats). """
        """ We can visualize this distribution for specific years using the year slider. """
        st.markdown("""---""")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Comparison of floor area (sqm) by Flat Type**")
        with col2:
            renderBadge("static")
        box_psqmvft(
            hdb_resales_drop_opt_fasqmvft,
            "flat_type",
            "floor_area_sqm",
            "Plot of floor area (sqm) vs flat type (1990-2023)",
        )
        """ 3 room flats have large positive outliers due to luxury 3 room apartments. """
        """ Those are mostly ground floor or penthouse apartments with large rooms, balconies, and/or patios. """

        st.markdown("""---""")

    if plot_selection["plot_1.5"]:
        render_plot_main_title("plot_1.5")

        line_fsvft(new_resales)
        """The 2nd quarter of 2020 beared the brunt of at least two months of circuit breakers (COVID-19),"""
        """hence the observed lowest dip for all flat type resales sold during the period"""
        st.markdown("""---""")

    if plot_selection["plot_2"]:
        render_plot_main_title("plot_2")

        scatter_psqmvrl(new_resales)
        """For 2016 onwards, generally increasing trend as expected, although seems to taper off when remaining lease reaches ~80 years"""
        # Can use scatterplot for streamlit, for static graph displot seems better
        st.markdown("""---""")

    if plot_selection["plot_5"]:
        render_plot_main_title("plot_5")

        box_psqmvt(filtered_resale_data, yr_range_selector, last_year_of_interval)
        """ From 1992 - 2002, Marine Parade resale prices were the highest overall due to its small and mature residential area (scarcity, low supply), coupled with desirable attributes such as comprehensive ameneties and well-developed infrastructure."""
        """ From 2002, BTO system was fully implemented, which reduced demand pressure on mature estates like Marine Parade and Bishan"""
        """ From 2000 - 2005, Punggol resale prices were the highest in the northeast due its underdeveloped nature and low flat count (increase demand) as well as the 1996 gov-backed Punggol 21 masterplan which raised speculative property value and prices in the area."""
        """ From 2016 - 2023, Central areas are generally more expensive than the rest due to overall accessibility around Singapore, whereas areas at the extremes of Singapore are noticeably lower priced for the same reason."""
        """ The remaining residential areas have less variance, slight differences might be due to popularity, access to amenities, or distance from the airport."""
        st.markdown("""---""")

    if plot_selection["plot_6"]:
        render_plot_main_title("plot_6")

        scatter_psqmvsr(new_resales)
        """ For newer resales, price does increase with floor height generally but not by much if below 40 storeys. """
        st.markdown("""---""")

    if plot_selection["plot_3"]:
        render_plot_main_title("plot_3")

        box_mrvft(hdb_rentals)
        """Generally increasing rental with size as expected"""
        st.markdown("""---""")

    if plot_selection["plot_4"]:
        render_plot_main_title("plot_4")

        box_mrvt(hdb_rentals)
        """ Surprisingly, rentals are quite invariant across regions. """
        st.markdown("""---""")


else:
    if plot_selection["units_heatmap_static"]:
        render_plot_main_title("units_heatmap_static")
        m = units_heatmap_single_year(yr_selector, hdb_mapping_units)
        add_map_layers(m, mrt_mapping, yr_selector)
        m.to_streamlit(width=900)

        """ Between 2002 and 2003, we observe the increase of resale units and prices in the North-East region as the NE line was opened. """
        """ A surge in resale units in Punggol can be observed in 2007 as the Punggol 21 Plus plan by Lee Hsien Loong was introduced. """
        st.markdown("""---""")

    if plot_selection["units_heatmap_range"]:
        render_plot_main_title("units_heatmap_range")
        m = units_heatmap_year_range(yr_range_selector, hdb_mapping_units)
        add_map_layers(m, mrt_mapping, yr_range_selector[1])
        m.to_streamlit(width=900)
        
        """ In 1990-1999, we observe that Tampines and Pasir Ris have the densest resale units by region. """
        """ In 2000-2009, we observe that Woodlands has the densest resale units by region, and the development of the North-East region caused an increase in resale units. """
        """ In 2001-2019, we observe that Sengkang and Punggol has the densest resale units by region. """
        """ We note that the Central region did not see any surges in resale units across the years. """
        st.markdown("""---""")

    if plot_selection["price_heatmap_static"]:
        render_plot_main_title("price_heatmap_static")
        m = price_per_sqm_heatmap_single_year(yr_selector, hdb_mapping_price)
        add_map_layers(m, mrt_mapping, yr_selector)
        # m.add_colormap()
        m.to_streamlit(width=900)

        """ We observe some local highs at 1997 (Asian Financial Crisis) and 2013 (Cooling measures), as well as a marked pickup in prices post 2020 during the COVID period. """
        """ Between 2002 and 2003, we observe the increase of resale units and prices in the North-East region as the NE line was opened. """
        """ Between 1995-1996, Punggol experienced an increase in average price due to the introduction of Punggol 21, but development plans experienced continuous setbacks. """
        st.markdown("""---""")

    if plot_selection["price_heatmap_range"]:
        render_plot_main_title("price_heatmap_range")
        m = price_per_sqm_heatmap_year_range(yr_range_selector, hdb_mapping_price)
        add_map_layers(m, mrt_mapping, yr_range_selector[1])
        m.to_streamlit(width=900)

        """ In 1990-1999, we observe that the Western region has lower resale prices, and that the Northern and Eastern region have higher than averageresale prices. """
        """ In 2000-2009, we observe that the North-Eastern and Eastern region have higher than average resale prices. """
        """ In 2010-2019, we observe that the Western region have higher than average resale prices, particularly in Pioneer and Clementi as this decade marked the entry of NTU and NUS' ranking into the global top 50 universities by QS World University Rankings. """
        st.markdown("""---""")