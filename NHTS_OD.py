# using Pydeck to show the annual total trips between zones
import pydeck as pdk
import pandas as pd
import streamlit as st
import geopandas as gpd

# use wide mode
st.set_page_config(layout="wide")

# add a title
st.title("Florida Trips Across NHTS Zones")
# data source, full name, add url link
st.caption(
    "*Data source: [National Household Travel Survey 2022](https://nhts.ornl.gov/), [Documentation](https://nhts.ornl.gov/od/documentation)")
# add zone shapefile source, add url link


# Read NHTS OD data (OD only within FL)
trip_fl = pd.read_csv('trip_od_within_fl.csv')
# add a toggle to switch on and off, name it as only show cross zone trips
show_cross_zones = st.checkbox("Do not include same-zone trips", value=True)

if show_cross_zones:
    # filter out the origin is the same as the destination
    trip_fl = trip_fl[trip_fl['origin_zone_name']
                      != trip_fl['destination_zone_name']]
# Read the FL zone shapefile
fl_zone_shapefile = gpd.read_file('shapefiles/fl_zone_shapefile.shp')

# Create 3 columns
col1, col2, col3 = st.columns([7, 0.5, 5])


with col2:
    st.write(" ")

with col3:
    # st.write("Control parameters can be added here")

    # Add a toggle to turn on and off zone names
    show_zone_names = st.checkbox("Show zone names", value=True)

    # Create 2 sub columns for origin zone and destination zone selection
    sub_col1, sub_col2 = st.columns(2)

    with sub_col1:
        # Provide all the zone names in trip_fl for user to select, add an all zones option
        zone_names = trip_fl['origin_zone_name'].unique()
        selected_zone = st.selectbox("Select an origin zone", [
                                     "All FL NHTS zones"] + list(zone_names), index=list(zone_names).index("Miami-Fort Lauderdale-West Palm Beach, FL") + 1)
        # st.write(f"You selected: {selected_zone}")

    with sub_col2:
        # select a destination zone
        destination_zone_names = trip_fl['destination_zone_name'].unique()
        selected_destination_zone = st.selectbox("Select a destination zone", [
                                                 "All FL NHTS zones"] + list(destination_zone_names))
        # st.write(f"You selected: {selected_destination_zone}")

    if selected_zone == "All FL NHTS zones" and selected_destination_zone == "All FL NHTS zones":
        trip_fl_selected = trip_fl
    elif selected_zone == "All FL NHTS zones":
        trip_fl_selected = trip_fl[trip_fl['destination_zone_name']
                                   == selected_destination_zone]
    elif selected_destination_zone == "All FL NHTS zones":
        trip_fl_selected = trip_fl[trip_fl['origin_zone_name']
                                   == selected_zone]
    else:
        trip_fl_selected = trip_fl[(trip_fl['origin_zone_name'] == selected_zone) & (
            trip_fl['destination_zone_name'] == selected_destination_zone)]

    # add a slider bar to select top N trips to show by percentage of total trips
    if trip_fl_selected.shape[0] > 1:
        top_n_trips = st.slider("Select number of top ODs to show",
                                min_value=1, max_value=trip_fl_selected.shape[0], value=trip_fl_selected.shape[0])
    else:
        top_n_trips = 1

    # apply it on the trip_fl_selected
    trip_fl_selected = trip_fl_selected.sort_values(
        by='annual_total_trips', ascending=False).head(top_n_trips)

    # show a break down of the selected trip by travel mode, the modes are mode_air, mode_rail, mode_vehicle, mode_atf
    st.write("Table 1: Selected trips by travel mode")

    # Calculate the total trips for each mode
    mode_air_total = trip_fl_selected['mode_air'].sum()
    mode_rail_total = trip_fl_selected['mode_rail'].sum()
    mode_vehicle_total = trip_fl_selected['mode_vehicle'].sum()
    mode_atf_total = trip_fl_selected['mode_atf'].sum()
    total_trips = mode_air_total + mode_rail_total + \
        mode_vehicle_total + mode_atf_total

    # Create a dataframe to display the breakdown in a table
    mode_breakdown = pd.DataFrame({
        'Mode': ['Air', 'Rail', 'Vehicle', 'Active Transportation/Ferry'],
        'Total Trips': [mode_air_total, mode_rail_total, mode_vehicle_total, mode_atf_total],
        'Percentage': [
            round((mode_air_total / total_trips) * 100, 2),
            round((mode_rail_total / total_trips) * 100, 2),
            round((mode_vehicle_total / total_trips) * 100, 2),
            round((mode_atf_total / total_trips) * 100, 2)
        ]
    })

    # Format the 'Total Trips' column with a 1000 separator
    mode_breakdown['Total Trips'] = mode_breakdown['Total Trips'].apply(
        lambda x: "{:,}".format(x))

    # Display the table without the index
    st.write(mode_breakdown.set_index('Mode'))

    # show a break down of the selected trip by purpose, the purposes are purpose_work, purpose_nonwork
    st.write("Table 2: Selected trips by purpose")

    # Calculate the total trips for each purpose
    purpose_work_total = trip_fl_selected['purpose_work'].sum()
    purpose_nonwork_total = trip_fl_selected['purpose_nonwork'].sum()
    total_purpose_trips = purpose_work_total + purpose_nonwork_total

    # Create a dataframe to display the breakdown in a table
    purpose_breakdown = pd.DataFrame({
        'Purpose': ['Work', 'Non-Work'],
        'Total Trips': [purpose_work_total, purpose_nonwork_total],
        'Percentage': [
            round((purpose_work_total / total_purpose_trips) * 100, 2),
            round((purpose_nonwork_total / total_purpose_trips) * 100, 2)
        ]
    })

    # Format the 'Total Trips' column with a 1000 separator
    purpose_breakdown['Total Trips'] = purpose_breakdown['Total Trips'].apply(
        lambda x: "{:,}".format(x))

    # Display the table without the index
    st.write(purpose_breakdown.set_index('Purpose'))

with col1:

    # get the total annual trips for the zone
    trip_fl_selected['selected_trips_total'] = trip_fl_selected['annual_total_trips'].sum()

    # Calculate percentage of total trips for each row, 2 decimal places
    trip_fl_selected['percentage_of_total'] = (
        (trip_fl_selected['annual_total_trips'] / trip_fl_selected['selected_trips_total']) * 100).round(2)

    # Normalize the width to avoid extreme small and large values
    min_width = 0.5
    max_width = 10 if show_cross_zones else 1000

    min_trips = trip_fl_selected['annual_total_trips'].min()
    max_trips = trip_fl_selected['annual_total_trips'].max()
    if max_trips == min_trips:
        # Use a default width when all trips have the same count
        trip_fl_selected['normalized_width'] = min_width
    else:
        trip_fl_selected['normalized_width'] = min_width + \
            (trip_fl_selected['annual_total_trips'] - min_trips) * \
            (max_width - min_width) / (max_trips - min_trips)

    # ArcLayer to visualize flows between zones with direction
    arc_layer = pdk.Layer(
        'ArcLayer',
        trip_fl_selected,
        get_source_position='[o_x, o_y]',
        get_target_position='[d_x, d_y]',
        get_source_color='[255, 255, 0, 160]',
        get_target_color='[255, 0, 0, 160]',
        get_width="normalized_width",
        pickable=True,
        get_tilt=15,
        get_target_arrow=True,  # Arrow to show direction of travel
    )

    # GeoJsonLayer to show FL zone boundaries
    zone_layer = pdk.Layer(
        'GeoJsonLayer',
        fl_zone_shapefile.__geo_interface__,
        get_fill_color='[0, 0, 0, 0]',  # Transparent fill
        get_line_color='[33, 168, 168, 255]',  # Gray boundary lines
        get_line_width=250,
    )

    # Create TextLayer with dynamic zoom-based size and elevation
    text_layer = pdk.Layer(
        "TextLayer",
        data=fl_zone_shapefile,
        get_position="[centroid_x, centroid_y]",
        get_text="zone_name",
        get_color='[33, 168, 168, 255]',
        # get_size=16,
        size_scale=0.3,
        # add vertical offset to the text
        get_pixel_offset=[0, -10],
    )

    # ScatterplotLayer for visualizing origin points
    point_layer = pdk.Layer(
        'ScatterplotLayer',
        data=trip_fl_selected,
        get_position='[o_x, o_y]',
        get_color='[255, 255, 0, 160]',
        get_radius="500",
        pickable=True,
    )

    # Set the initial view for the map
    view = pdk.ViewState(
        longitude=-81.5158,
        latitude=28.054,
        zoom=6,
        pitch=0,
    )

    # Create a Deck object with all layers
    layers = [arc_layer, zone_layer, point_layer]
    if show_zone_names:
        layers.append(text_layer)

    r = pdk.Deck(
        layers=layers,
        initial_view_state=view,
        tooltip={
            "html": (
                "<small><b>{origin_zone_name}</b> --> <b>{destination_zone_name}</b></small><br>"
                "<small>Trips: {annual_total_trips}</small><br>"
                "<small>Percentage of total selected trips: {percentage_of_total} %</small>"
            )
        },
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        height=800
    )

    st.pydeck_chart(r)

    # Add legend under the map
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; margin-top: 10px;">
            <div style="display: flex; align-items: center; margin-right: 20px;">
                <div style="width: 20px; height: 20px; background-color: rgba(255, 255, 0, 160); margin-right: 5px;"></div>
                <small>Origin</small>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: rgba(255, 0, 0, 160); margin-right: 5px;"></div>
                <small>Destination</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

trip_fl_export = trip_fl_selected.drop(
    columns=['o_x', 'o_y', 'd_x', 'd_y', 'zone_id_x', 'zone_id_y', 'origin_state', 'destination_state', 'normalized_width'])
st.write(" ")
st.write("The selected data for visualization is shown below:")
st.write(trip_fl_export)
st.download_button(label="Download selected data", data=trip_fl_export.to_csv(
    index=False), file_name="selected_od_data_export.csv")
