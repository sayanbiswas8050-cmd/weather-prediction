import streamlit as st
import pandas as pd
import pickle
import requests

model = pickle.load(open("model.pkl","rb"))
API_KEY = "fedb3649a8c9a97c44826476b4ecdd6d"

def get_current_weather(city):
    if not city:
        return None
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response =requests.get(URL)
    data = response.json()
    return data

st.title("Rain Prediction App")

city = st.text_input("Enter City Name")


data = get_current_weather(city)

if data:
    current_weather = pd.DataFrame({
        "City": [data.get("name", city)],
        "Temperature": [round(data.get("main", {}).get("temp", 0)//10)],
        "Humidity": [data.get("main", {}).get("humidity", 0)],
        "Wind_Speed": [data.get("wind", {}).get("speed", 0)*10],
        "Cloud_Cover": [data.get("clouds", {}).get("all", 0)],
        "Pressure": [data.get("main", {}).get("pressure", 0)]
        })

    st.header(f"Weather in {current_weather['City'][0]}")

    current_weather_df = current_weather[["Temperature","Humidity","Wind_Speed","Cloud_Cover","Pressure"]]
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.image("Temperature.png",width= 100)
        st.header(f"Temperature: {current_weather_df['Temperature'][0]} °C")
    with col2:
        st.image("Humidity.png",width= 100)
        st.header(f"Humidity:     {current_weather_df["Humidity"][0]} %")
    with col3:
        st.image("Wind_Speed.png",width=100)
        st.header(f"Wind_Speed: {current_weather_df["Wind_Speed"][0]} (m/s)")
    col4,col5 =st.columns(2)
    with col4:
        st.image("Cloud_Cover.jpeg",width=100)
        st.header(f"Cloud_Cover: {current_weather_df["Cloud_Cover"][0]} ")
    with col5:
        st.image("Wind_Pressure.png",width=100)
        st.header(f"Wind Pressure: {current_weather_df["Pressure"][0]}")

    st.dataframe(current_weather_df)
    if st.button("Rain Prediction"):
        result = model.predict_proba(current_weather_df)
        st.text("Probability of rain in " + current_weather['City'][0] +" : "+str(round((result[0][1]*100),2))+" %")
        st.text("Probability of no rain in " +current_weather['City'][0] +" :" +str(round((result[0][0]*100),2))+" %")
