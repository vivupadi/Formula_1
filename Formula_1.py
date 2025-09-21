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


#breakpoint()


data_loading_state = st.text('Loading data...')
selected_venue = st.session_state.venue

venue = Hist_OpenF1(selected_venue)

df_1 = venue.get_race_details()

#df_1 = get_race_details(selected_venue)


#breakpoint()
data_loading_state.text('Loading data...done!')
#st.write(df_1.render(), unsafe_allow_html=True)
#st.markdown(df_1.render(), unsafe_allow_html = True)
st.dataframe(df_1)

venue.get_car_speed()
venue.weather()
