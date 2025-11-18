import streamlit as st
import pandas as pd
import pickle
import requests

# Load model
model = pickle.load(open("model.pkl", "rb"))

API_KEY = "fedb3649a8c9a97c44826476b4ecdd6d"

# ------------------ Weather Function ------------------
def get_current_weather(city):
    if not city:
        return None
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(URL)
    data = response.json()
    return data


# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="Rain Prediction App 🌦️", page_icon="🌧️", layout="centered")

page_bg = """
<style>
body {
    background: linear-gradient(to right, #b3e5fc, #e1f5fe);
    font-family: 'Segoe UI', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #b3e5fc, #e1f5fe);
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

[data-testid="stSidebar"] {
    background: #e3f2fd;
}

div.block-container {
    background: rgba(255, 255, 255, 0.6);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.1);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.markdown(
    """
    <h1 style='text-align: center; color: #0077b6;'>🌦️ Rain Prediction App</h1>
    <p style='text-align: center; color: gray;'>
    Get real-time weather updates and AI-based rain prediction 🌈
    </p>
    """,
    unsafe_allow_html=True,
)

city = st.text_input("🏙️ Enter City Name", placeholder="e.g., Kolkata")

data = get_current_weather(city)

if data and data.get("cod") == 200:
    current_weather = pd.DataFrame({
        "City": [data.get("name", city)],
        "Temperature": [round(data.get("main", {}).get("temp", 0))],
        "Humidity": [data.get("main", {}).get("humidity", 0)],
        "Wind_Speed": [data.get("wind", {}).get("speed", 0)],
        "Cloud_Cover": [data.get("clouds", {}).get("all", 0)],
        "Pressure": [data.get("main", {}).get("pressure", 0)]
    })

    st.markdown(
        f"<h2 style='text-align: center; color: #023e8a;'>Weather in {current_weather['City'][0]}</h2>",
        unsafe_allow_html=True,
    )

    current_weather_df = current_weather[["Temperature", "Humidity", "Wind_Speed", "Cloud_Cover", "Pressure"]]

    # ------------------ Weather Cards ------------------
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("Temperature.png", width=90)
        st.markdown(f"<div style='background-color:#e7f5ff; border-radius:15px; padding:10px; text-align:center; box-shadow:2px 2px 10px #d6e0f0;'>🌡️ <b>Temperature:</b><br>{current_weather_df['Temperature'][0]} °C</div>", unsafe_allow_html=True)
    with col2:
        st.image("Humidity.png", width=90)
        st.markdown(f"<div style='background-color:#f1f8e9; border-radius:15px; padding:10px; text-align:center; box-shadow:2px 2px 10px #e0f2f1;'>💧 <b>Humidity:</b><br>{current_weather_df['Humidity'][0]} %</div>", unsafe_allow_html=True)
    with col3:
        st.image("Wind_Speed.png", width=90)
        st.markdown(f"<div style='background-color:#fff3e0; border-radius:15px; padding:10px; text-align:center; box-shadow:2px 2px 10px #ffe0b2;'>💨 <b>Wind Speed:</b><br>{current_weather_df['Wind_Speed'][0]} m/s</div>", unsafe_allow_html=True)

    col4, col5 = st.columns(2)
    with col4:
        st.image("Cloud_Cover.jpeg", width=90)
        st.markdown(f"<div style='background-color:#ede7f6; border-radius:15px; padding:10px; text-align:center; box-shadow:2px 2px 10px #d1c4e9;'>☁️ <b>Cloud Cover:</b><br>{current_weather_df['Cloud_Cover'][0]}%</div>", unsafe_allow_html=True)
    with col5:
        st.image("Wind_Pressure.png", width=90)
        st.markdown(f"<div style='background-color:#ffebee; border-radius:15px; padding:10px; text-align:center; box-shadow:2px 2px 10px #ffcdd2;'>🌬️ <b>Pressure:</b><br>{current_weather_df['Pressure'][0]} hPa</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.dataframe(current_weather_df, use_container_width=True)

    # ------------------ Prediction Section ------------------
    if st.button(" Predict Rain"):
        result = model.predict_proba(current_weather_df)
        rain_prob = round(result[0][1] * 100, 2)
        no_rain_prob = round(result[0][0] * 100, 2)

        st.markdown(
            f"""
            <div style='background-color:#e0f7fa; border-radius:15px; padding:20px; text-align:center; box-shadow:2px 2px 12px #b2ebf2;'>
                <h3>🌧️ Rain Prediction Results</h3>
                <p><b>Probability of Rain:</b> {rain_prob}%</p>
                <p><b>Probability of No Rain:</b> {no_rain_prob}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

else:
    if city:
        st.error("❌ City not found! Please enter a valid city name.")
