import pandas as pd
import requests
from urllib.request import urlopen
import json

#Streamlit
import streamlit as st
import altair as alt


from hist_data import *


#Streamlit part
st.title('Formula 1 Dashboard')


# Or use "with" notation:
with st.sidebar:
    venue = st.selectbox("Select Venue", ["Sakhir","Jeddah", "Melbourne", "Suzuka","Shanghai", "Miami", "Imola", "Monaco", "Montréal", "Barcelona","Spielberg","Silverstone","Budapest",
    "Spa-Francorchamps", "Zandvoort", "Monza", "Baku", "Marina Bay", "Austin", "Mexico City", "São Paulo", "Las Vegas","Lusail","Yas Island"], key='venue')


data_loading_state = st.text('Loading data...')
selected_venue = st.session_state.venue

venue = Hist_OpenF1(selected_venue)


df_drivers = venue.get_race_details()

df_speed_avg, df_speed_max = venue.get_car_speed()

# Convert Series to DataFrame before merging
try:
    if not df_speed_avg.empty and not df_speed_max.empty:
        # Convert Series to DataFrame
        speed_avg_df = df_speed_avg.reset_index()
        speed_avg_df.columns = ['driver_number', 'Average_speed']
        
        speed_max_df = df_speed_max.reset_index()
        speed_max_df.columns = ['driver_number', 'Max_speed']
        
        # Now merge (this will work!)
        df_1 = df_drivers.merge(speed_avg_df, on='driver_number', how='left')
        df_1 = df_1.merge(speed_max_df, on='driver_number', how='left')
        
    else:
        # If no speed data, just use race data
        df_1 = df_drivers
        st.warning("No speed data available")

except Exception as e:
    st.error(f"Error merging data: {e}")
    df_1 = df_drivers  # Fallback to just race data


df_styled = df_1.style.apply(
            lambda row: [
                f'background-color: #{row["team_colour"]}' if col == 'team_name' else ''
                for col in df_1.columns
            ], 
            axis =1
        )

data_loading_state.text('Loading data...done!')
#st.write(df_1.render(), unsafe_allow_html=True)
st.dataframe(df_styled)

venue.weather()
