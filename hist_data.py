import pandas as pd
import os
import requests
import time

import streamlit as st
import altair as alt


# ===========
# Error handling and exception improvement
# ===========
class Hist_OpenF1:                                      #uses REST API
    def __init__(self, place):
        self.url = 'https://api.openf1.org/v1'
        self.place = place
        try:
            venue = requests.get(f'{self.url}/sessions?location={self.place}&session_name=Race&year=2024')
            venue.raise_for_status()      #check if the request was succesful
            data_venue = venue.json()

            if not data_venue:
                st.error(f'No session found for {place}')
                self.session_key=None
                return
            
            df = pd.DataFrame(data_venue)
            self.session_key = df['session_key'][0]
        
        except requests.exceptions.RequestException as e:
            st.error(f'Could not connect to F1 API:{e}')
            self.session_key = None
        except Exception as e:
            st.error(f'Error loading the session key;{e}')
            self.session_key = None


    def __repr__(self):                 #to show what the called object contains
        """String representation for debugging"""
        return (f"F1Config(base_url='{self.base_url}', "
                f"default_year={self.default_year}, "
                f"timeout={self.request_timeout})")
    

    def get_race_details(self):
        if self.session_key is None:
            return pd.DataFrame()
        
        try:
            driver_position = requests.get(f'{self.url}/position?session_key={self.session_key}')

            driver = requests.get(f'{self.url}/drivers?session_key={self.session_key}')
            data_race = driver_position.json()
            data_driver = driver.json()  

            if isinstance(data_race, dict):
                data_race = [data_race]
            
            # Fix the scalar values error
            if isinstance(data_driver, dict):
                data_driver = [data_driver]
        
            df_race = pd.DataFrame(data_race)
            self.df_driver = pd.DataFrame(data_driver)   

            if df_race.empty or self.df_driver.empty:
                st.warning("No data available for this session")
                return pd.DataFrame()

            df_cleaned = df_race.drop_duplicates(subset=['driver_number'], keep= 'last', ignore_index = False)
            df_cleaned = df_cleaned.merge(self.df_driver[['driver_number', 'broadcast_name', 'team_colour', 'team_name']], on= 'driver_number', how = 'left')
            df_cleaned.rename(columns ={'broadcast_name' : 'Driver'}, inplace = True)
            #breakpoint()
            df_cleaned = df_cleaned.sort_values(by = 'position', ascending=True)
            #breakpoint()
            df_cleaned =  df_cleaned[['position', 'Driver', 'driver_number', 'team_colour', 'team_name']]                            
            return df_cleaned
        
        except requests.exceptions.RequestException as e:
            st.error(f'Error getting race details:{e}')
            return pd.DataFrame()
        except Exception as e:
            st.error(f'Error processing race data: {e}')
            return pd.DataFrame()

    def get_car_speed(self):
        if self.session_key is None:
            return pd.DataFrame()
        try:
            # Check if we have driver data
            if not hasattr(self, 'df_driver') or self.df_driver.empty:
                st.warning("No driver data available for speed analysis")
                return pd.Series(), pd.Series()
            
            speed_df = pd.DataFrame()
            driver_number_list = self.df_driver[['driver_number']]

            # Add simple progress tracking
            progress_bar = st.progress(0)
            total_drivers = len(driver_number_list)

            for i,number in enumerate(driver_number_list.values):
                try:
                    progress_bar.progress((i + 1) / total_drivers)
                    car_speed = requests.get(f'{self.url}/laps?session_key={self.session_key}&driver_number={number[0]}')
                    car_speed.raise_for_status()
                    car_data = car_speed.json()

                    temp = pd.DataFrame(car_data)
                    speed_df = pd.concat([speed_df , temp], axis=0, ignore_index=True)

                     # Small delay to be respectful to API
                    time.sleep(0.1)

                except requests.exceptions.RequestException:
                    # Skip this driver if request fails
                    continue
                except Exception:
                    # Skip this driver if processing fails
                    continue
            
            progress_bar.empty()

            if speed_df.empty:
                st.warning("No speed data available")
                return pd.Series(), pd.Series()

            df = speed_df[['driver_number', 'i1_speed', 'i2_speed', 'is_pit_out_lap','st_speed']]
            df_clean = df[df['is_pit_out_lap'] == False]

            if 'True' in df['is_pit_out_lap'].values:
                breakpoint()
            df_clean = df[['driver_number', 'i1_speed', 'i2_speed', 'st_speed']]
            df_clean.dropna()
            self.speed_df_avg = df_clean.groupby('driver_number')['st_speed'].mean()
            self.speed_df_max = df_clean.groupby('driver_number')['st_speed'].max()
            return self.speed_df_avg, self.speed_df_max

        except Exception as e:
            st.error(f"Error getting speed data: {e}")
            return pd.Series(), pd.Series()
        

    def weather(self):
        if self.session_key is None:
                st.warning("No session available for weather data")
                return pd.DataFrame()
        
        try:
            weather = requests.get(f'{self.url}/weather?session_key={self.session_key}')
            weather.raise_for_status()
            data =  weather.json()

            if not data:
                st.info("No weather data available for this session")
                return pd.DataFrame()
            
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
            return df
        
        except requests.exceptions.RequestException as e:
            st.warning(f"Could not get weather data: {e}")
            return pd.DataFrame()
        except Exception as e:
            st.warning(f"Error processing weather data: {e}")
            return pd.DataFrame()