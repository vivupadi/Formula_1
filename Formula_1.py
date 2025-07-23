import pandas as pd
import requests
from urllib.request import urlopen
import json

#Streamlit
import streamlit as st


#Get a specific race detail

def get_race_details(session_key):
    race = requests.get(f'https://api.openf1.org/v1/intervals?session_key={session_key}')
    driver = requests.get(f'https://api.openf1.org/v1/drivers?session_key={session_key}')
    data_race = race.json()
    data_driver = driver.json()
    df_race = pd.DataFrame(data_race)
    df_cleaned = df_race.drop_duplicates(subset=['driver_number'], ignore_index = True)
    df_driver = pd.DataFrame(data_driver)
    df_cleaned = df_cleaned.merge(df_driver[['driver_number', 'broadcast_name']], on= 'driver_number', how = 'left')
    df_cleaned.rename(columns ={'broadcast_name' : 'Driver'})
    return df_cleaned

df_1 = get_race_details(9141)


breakpoint()


#Show drivers in sequence


#select driver


#show Tire color, Tire age, pit status

#Streamlit part

st.table(df_1)