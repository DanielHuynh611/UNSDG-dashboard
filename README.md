# Greenhouse Gas (GHG) Emissions and Energy Equality Dashboard
## Overview
This project is a data visualization dashboard built using Dash and Plotly to explore and analyze global greenhouse gas emissions (GHG) and renewable energy investment trends. The goal is to provide insights into the progress towards the United Nations' Sustainable Development Goals (SDG) 7 and 13, which focus on affordable clean energy and climate action.

The dashboard displays information such as GHG emissions by sector, correlation of emissions over time, renewable energy capacity by region, and international financial flows supporting clean energy development.

## Features
1. Interactive Line Charts - Explore GHG emissions trends over time for various sectors and specific countries.
2. Bar Charts - View renewable energy-generating capacity by region.
3. Dropdown Selectors - Choose specific countries or regions to filter data and view targeted insights.
4. Responsive and Accessible Layout - The layout is designed to be intuitive and provides clear, easy-to-read visualizations.
## Dataset Information
- world_ghg_total_nona.csv: Contains total GHG emissions data by country from 1990 to 2020.
- industry_co2.csv: Sectoral GHG emissions data.
- installed_renewable.xlsx: Renewable energy-generating capacity by region.
- investment.xlsx: Data on international financial flows supporting renewable energy projects.
## Installation
1. **Clone the repository**
   ```
   git clone https://github.com/DanielHuynh611/UNSDG-dashboard.git
   ```
2. **Installed required packages**
   ```
   pip install -r requirements.txt
   ```
## How to run the program
1. Run the following command:
   ```
   python app.py
   ```
2. Open your browser and go to http://127.0.0.1:8051/ to access the dashboard.

## Dashboard Sections
1. Introduction
- Provides an overview of key messages related to global GHG emissions, energy sector contributions, and financial requirements for achieving net-zero emissions.
2. GHG Emissions Over Time by Sector
- Interactive line chart showing GHG emissions trends across sectors like Energy, Agriculture, Waste, and more. Allows users to focus on specific emissions levels and zoom in on trends.
3. GHG Emissions by Country
- Dropdown selector to choose a country and view its GHG emissions over time. Highlights the correlation of each country's emissions with global trends.
4. Renewable Energy-Generating Capacity by Region
- Horizontal bar chart displaying renewable energy capacity by region for the year 2022.
5. Financial Flows Supporting Clean Energy
- Time series chart showing international financial investments in renewable energy projects by region. Users can select different regions to view their specific financial flow trends.

## License
This project is licensed under the MIT License.
