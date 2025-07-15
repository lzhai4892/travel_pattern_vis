# Florida Trips Cross NHTS Zones

This application visualizes the annual total trips between zones in Florida using data from the National Household Travel Survey (NHTS) 2022. It leverages Pydeck for map visualization and Streamlit for the web interface.
[Link to the web app]((https://fl-travel-pattern.streamlit.app/)

## Features

- **Interactive Map**: Visualize trips between zones with directional arcs.
- **Zone Selection**: Filter trips by selecting specific origin and destination zones.
- **Trip Breakdown**: View selected trips broken down by travel mode and purpose.
- **Data Export**: Download the selected trip data as a CSV file.

## Data Sources

- **Trip Data**: [National Household Travel Survey 2022](https://nhts.ornl.gov/)
- **Zone Shapefile**: Provided in the `shapefiles` directory.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/travel_pattern_vis.git
   ```
2. Navigate to the project directory:
   ```bash
   cd travel_pattern_vis
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run NHTS_OD.py
   ```
2. Open your web browser and go to `http://localhost:8501` to view the application.

## Configuration

- **Wide Mode**: The application uses Streamlit's wide mode for better visualization.
- **Toggle Options**: 
  - Show only cross-zone trips.
  - Display zone names on the map.

## Visualization

- **ArcLayer**: Shows flows between zones with direction.
- **GeoJsonLayer**: Displays Florida zone boundaries.
- **TextLayer**: Optionally shows zone names.
- **ScatterplotLayer**: Visualizes origin points.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data provided by the National Household Travel Survey.
