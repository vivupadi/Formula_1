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

#df_1 = pd.concat([df_drivers, df_speed_avg, df_speed_max], axis=0, join='inner', ignore_index=True)
df_1= df_drivers.merge(df_speed_avg,on='driver_number').merge(df_speed_max,on='driver_number')
#df_1 = get_race_details(selected_venue)
df_1.rename(columns={'st_speed_x' : 'Average_speed', 'st_speed_y' : 'Max_speed'})
df_styled = df_1.style.apply(
            lambda row: [
                f'background-color: #{row["team_colour"]}' if col == 'team_name' else ''
                for col in df_1.columns
            ], 
            axis =1
        )

#breakpoint()
data_loading_state.text('Loading data...done!')
#st.write(df_1.render(), unsafe_allow_html=True)
st.dataframe(df_styled)

venue.weather()
