## Description
A Dash web application visualizes global CO2 production trends from 1920 to 2022. 
The application includes a **Play** and **Stop** button, enabling the automatic playback of global CO2 production over the time range. 
The application features a dynamic scatter_geo plot, allowing users to interact by clicking on specific countries. 
Upon clicking, a pie chart is displayed, showcasing the breakdown of CO2 production by industry for the selected country and year. 
Additionally, users have the option to hide or show the pie chart using a convenient button. 
The project sources its CO2 production data from https://github.com/owid/co2-data.git. 
The primary goal is to provide an insightful and interactive visualization of global CO2 production patterns.

## The data set
The origin data set is cleaned up to keep only data after the year of 1920, and the following columns: 
country,region,year,iso_code,land_use_change_co2,cement_co2,coal_co2,flaring_co2,oil_co2,gas_co2,other_industry_co2. <br>Please use the provided data set *clean-co2-data.csv* for this visualization.

## Formatting
The formatting is set up for a standard full-screen dimension of 680x1280. In case screen resolution differs, consider adjusting the formatting of charts, annotations, and other elements to ensure optimal presentation.

