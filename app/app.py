import streamlit as st
import pymongo
from datetime import date
import folium
from streamlit_folium import st_folium, folium_static
import json
from folium.plugins import HeatMap
import numpy as np


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])


client = init_connection()


def get_data_calor(mes):
    db = client.geo
    items = db.heat_centroids.find({"month": mes})
    items = [[*i["geometry"], np.log(i["count"])] for i in items]
    return items

def get_data(barco, dia):
    db = client.geo
    items = db.rutas.find({"_id": f"{barco}-{dia}"})
    items = list(items)
    return items


@st.cache_data
def get_barcos():
    db = client.geo
    items = db.barcos.find()
    items = [i["MMSI"] for i in items]
    return items

st.title('Tráfico de barcos por mes')

mes = st.selectbox('Mes', options=[ f"{i}" if i > 9 else f"0{i}" for i in range(1,13)])


heatmap_data = get_data_calor(mes)

m = folium.Map(location=(29.949932, -90.070116), zoom_start=7)
HeatMap(heatmap_data, radius=7, blur=2, ).add_to(m)
folium_static(m)


# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.


st.title('Rutas de barcos')

barcos = get_barcos()
barco = st.selectbox('Seleccione el baro', options=barcos)

dia = st.date_input('Seleccione el ía', min_value=date(2020, 1, 1), max_value=date(2020, 12, 31))

items = get_data(barco, dia)

if items:
    m = folium.Map((29.949932, -90.070116), zoom_start=7)

    folium.GeoJson(json.loads(items[0]['ruta']), name="Rute").add_to(m)
    folium.LayerControl().add_to(m)

    st_folium(m)

else:
    st.write(f"El día {dia} el barco {barco} no hizo recorridos")
