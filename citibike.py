import pandas as pd
import numpy as np
import streamlit as st
import codecs
import matplotlib.pyplot as plt

st.title('Citybike')
sidebar = st.sidebar
sidebar.title("MENU")


DATA_URL = ('/content/citibike.csv')
DATE_COLUMN = 'started_at'
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, encoding_errors='ignore')
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

#Cargar datos si se selecciona en el checkbox
agree = sidebar.checkbox("¿Quieres mostrar todos los datos? ")
if agree:
  data_load_state = st.text('Cargando...')
  data = load_data(2000)
  
  data_load_state.text("Cargado! (using st.cache)")
  st.dataframe(data)

agree = sidebar.checkbox("¿Quieres mostrar los recorridos por hora? ")
if agree:
  data_load_state = st.text('Cargando...')
  data = load_data(2000)
  data_load_state.text("Cargado! (using st.cache)")
  #hacer la grafica
  st.subheader('Numero de recorridos por hora')
  hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
  st.bar_chart(hist_values)



# Some number in the range 0-23
hour_to_filter = sidebar.slider('HORA', 0, 23, 17)
if hour_to_filter:
  data_load_state = st.text('Cargando...')
  data = load_data(2000)
  data_load_state.text("Cargado! (using st.cache)")

  data2_rename = data.rename(columns = {'start_lat': 'lat', 'start_lng': 'lon'}, inplace = False)

  filtered_data = data2_rename[data2_rename[DATE_COLUMN].dt.hour == hour_to_filter]

  st.subheader('Mapa de los recorridos iniciados a las %s:00' % hour_to_filter)
  st.map(filtered_data)