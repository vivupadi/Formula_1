import pandas as pd
import os
import requests

import streamlit as st
import altair as alt

class Hist_OpenF1:                                      #uses REST API
    def __init__(self, place):
        self.url = 'https://api.openf1.org/v1'
        self.place = place
        venue = requests.get(f'{self.url}/sessions?location={self.place}&session_name=Race&year=2024')
        data_venue = venue.json()
        df = pd.DataFrame(data_venue)
        self.session_key = df['session_key'][0]
    
    def get_race_details(self):
        driver_position = requests.get(f'{self.url}/position?session_key={self.session_key}')

        driver = requests.get(f'{self.url}/drivers?session_key={self.session_key}')
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


    def weather(self):
        weather = requests.get(f'{self.url}/weather?session_key={self.session_key}')
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
    