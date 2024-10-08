import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Function to get weather data
def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            st.error(f"Error {response.status_code}: {data['message']}")
            return None
    except requests.RequestException as e:
        st.error(f"Request error: {e}")
        return None

# Function to display current weather
def display_current_weather(data):
    if data:
        st.subheader("Current Weather")
        st.write(f"Weather in {data['name']}, {data['sys']['country']}:")
        st.write(f"Description: {data['weather'][0]['description']}")
        st.write(f"Temperature: {data['main']['temp']}°C")
        st.write(f"Humidity: {data['main']['humidity']}%")
        st.write(f"Wind Speed: {data['wind']['speed']} m/s")
    else:
        st.warning("Failed to fetch current weather data.")

# Function to display weather forecast with different charts
def display_forecast(api_key, city):
    st.subheader("5-Day Weather Forecast")

    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            times = [entry['dt_txt'] for entry in data['list']]
            temperatures = [entry['main']['temp'] for entry in data['list']]
            humidity = [entry['main']['humidity'] for entry in data['list']]
            wind_speed = [entry['wind']['speed'] for entry in data['list']]

            # Display forecast table
            forecast_df = pd.DataFrame({'Time': times, 'Temperature (°C)': temperatures,
                                        'Humidity (%)': humidity, 'Wind Speed (m/s)': wind_speed})
            st.write(forecast_df)

            # Plot temperature forecast line chart using Plotly
            fig_temp = px.line(forecast_df, x='Time', y='Temperature (°C)', title='Temperature Forecast',
                               labels={'Temperature (°C)': 'Temperature'})
            st.plotly_chart(fig_temp)

            # Plot humidity forecast bar chart using Plotly
            fig_humidity = px.bar(forecast_df, x='Time', y='Humidity (%)', title='Humidity Forecast',
                                  labels={'Humidity (%)': 'Humidity'})
            st.plotly_chart(fig_humidity)

            # Plot wind speed forecast area chart using Plotly
            fig_wind_speed = px.area(forecast_df, x='Time', y='Wind Speed (m/s)', title='Wind Speed Forecast',
                                      labels={'Wind Speed (m/s)': 'Wind Speed'})
            st.plotly_chart(fig_wind_speed)

        else:
            st.error(f"Error {response.status_code}: {data['message']}")
    except requests.RequestException as e:
        st.error(f"Request error: {e}")

# Streamlit App
def main():
    st.title("Weather Forecast App")

    # Input for City Name
    city = st.text_input("Enter City Name:", "London")
    api_key = 'fc6944c921634f2df96210c37b5dac93'

    # Fetch Current Weather
    current_weather_data = get_weather(api_key, city)
    display_current_weather(current_weather_data)

    # Fetch and Display 5-Day Forecast with Different Charts
    display_forecast(api_key, city)

if __name__ == "__main__":
    main()
