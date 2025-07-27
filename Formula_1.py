import pandas as pd
import requests
from urllib.request import urlopen
import json

#Streamlit
import streamlit as st
import altair as alt


def get_race_details(venue):
    session_key = get_venue(venue)

    driver_position = requests.get(f'https://api.openf1.org/v1/position?session_key={session_key}')

    driver = requests.get(f'https://api.openf1.org/v1/drivers?session_key={session_key}')
    data_race = driver_position.json()
    data_driver = driver.json()

    if isinstance(data_race, dict):
        data_race = [data_race]
  
    df_race = pd.DataFrame(data_race)
    df_driver = pd.DataFrame(data_driver)

    df_cleaned = df_race.drop_duplicates(subset=['driver_number'], keep= 'last', ignore_index = False)
    df_cleaned = df_cleaned.merge(df_driver[['driver_number', 'broadcast_name', 'team_colour', 'team_name']], on= 'driver_number', how = 'left')
    df_cleaned.rename(columns ={'broadcast_name' : 'Driver'}, inplace = True)
    #breakpoint()
    df_cleaned = df_cleaned.sort_values(by = 'position', ascending=True)
    #breakpoint()
    df_cleaned =  df_cleaned[['position', 'Driver', 'driver_number', 'team_colour', 'team_name']]
    df_styled = df_cleaned.style.apply(
        lambda row: [
            f'background-color: #{row["team_colour"]}' if col == 'team_name' else ''
            for col in df_cleaned.columns
        ], 
        axis =1
    )
    #df_styled =  df_styled[['position', 'Driver', 'driver_number', 'team_name']]                        
    return df_styled

def get_venue(place):
    venue = requests.get(f'https://api.openf1.org/v1/sessions?location={place}&session_name=Race&year=2024')
    #venue = requests.get(f'https://api.openf1.org/v1/sessions?session_name=Race&year=2024')
    data_venue = venue.json()
    df = pd.DataFrame(data_venue)
    #breakpoint()
    #return df
    return df['session_key'][0]

#Show tyres used in the 


#select driver


#show Tire color, Tire age, pit status
"""def tires_used(driver, session_key):
    stint_number in ascending:
        in each stintget the lap end - lap start
    return df[start_tire: age, tire_sequence:laps]"""

def weather(venue):
    session_key = get_venue(venue)
    weather = requests.get(f'https://api.openf1.org/v1/weather?session_key={session_key}')
    data =  weather.json()
    df = pd.DataFrame(data)
    df[['date', 'time']] = df['date'].str.split('T', expand=True)
    chart_1 = alt.Chart(df).mark_line().encode(
        x='time',
        y = alt.Y('track_temperature', scale = alt.Scale(domain=[df['track_temperature'].min(), df['track_temperature'].max()]))).properties(title = 'Track_Temperature')
    st.altair_chart(chart_1, use_container_width = True)
    chart_2 = alt.Chart(df).mark_line().encode(
        x='time',
        y = alt.Y('humidity', scale = alt.Scale(domain=[df['humidity'].min(), df['humidity'].max()]))).properties(title = 'Humidity')
    st.altair_chart(chart_2, use_container_width = True)
    #st.line_chart(df['track_temperature'], y_label = 'Track_temperature')
    #st.line_chart(df['humidity'], y_label = 'Humidity')
    return df

#Streamlit part
st.title('Formula 1 Dashboard')


# Or use "with" notation:
with st.sidebar:
    venue = st.selectbox("Select Venue", ["Sakhir","Jeddah", "Melbourne", "Suzuka","Shanghai", "Miami", "Imola", "Monaco", "Montréal", "Barcelona","Spielberg","Silverstone","Budapest",
    "Spa-Francorchamps", "Zandvoort", "Monza", "Baku", "Marina Bay", "Austin", "Mexico City", "São Paulo", "Las Vegas","Lusail","Yas Island"], key='venue')


#breakpoint()


data_loading_state = st.text('Loading data...')
selected_venue = st.session_state.venue

df_1 = get_race_details(selected_venue)


#breakpoint()
data_loading_state.text('Loading data...done!')
st.write(df_1.to_html(index = False), unsafe_allow_html=True)

weather(venue)
