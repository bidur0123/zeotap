import requests
import time
from collections import defaultdict
from apscheduler.schedulers.blocking import BlockingScheduler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import logging
from pymongo import MongoClient
from datetime import datetime

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

client = MongoClient("mongodb://mongodb:27017/")
db = client.weather_data
summaries_collection = db.summaries

API_KEY = "03b823f4abaacdbc0dc55a7eb02edac5"
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

weather_data = defaultdict(list)

def fetch_weather_data(city):
    try:
        logging.info(f"Fetching weather data for {city}")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Weather data received for {city}: {data}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data for {city}: {e}")
        return None

def fetch_weather_forecast(city):
    try:
        logging.info(f"Fetching weather forecast for {city}")
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Weather forecast received for {city}: {data}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather forecast for {city}: {e}")
        return None

def convert_kelvin_to_celsius(temp_k):
    return temp_k - 273.15

def aggregate_daily_data(city, day_data):
    try:
        logging.info(f"Aggregating daily data for {city}")
        temperatures = [entry["temp"] for entry in day_data]
        humidity_values = [entry["humidity"] for entry in day_data]
        wind_speeds = [entry["wind_speed"] for entry in day_data]
        main_conditions = [entry["main"] for entry in day_data]

        avg_temp = sum(temperatures) / len(temperatures)
        avg_humidity = sum(humidity_values) / len(humidity_values)
        avg_wind_speed = sum(wind_speeds) / len(wind_speeds)
        dominant_condition = max(set(main_conditions), key=main_conditions.count)

        return {
            "city": city,
            "avg_temp": avg_temp,
            "avg_humidity": avg_humidity,
            "avg_wind_speed": avg_wind_speed,
            "dominant_condition": dominant_condition,
            "date": datetime.utcnow()
        }
    except Exception as e:
        logging.error(f"Error aggregating data for {city}: {e}")
        return None

def store_daily_summary(city, summary):
    try:
        summaries_collection.insert_one(summary)
        logging.info(f"Stored daily summary for {city} in MongoDB")
    except Exception as e:
        logging.error(f"Error storing summary in MongoDB: {e}")

def trigger_alert(city, current_temp, threshold_temp):
    if current_temp > threshold_temp:
        logging.warning(f"ALERT! {city} temperature exceeded {threshold_temp}C")

def start_weather_monitoring():
    scheduler = BlockingScheduler()

    def get_weather():
        try:
            for city in CITIES:
                data = fetch_weather_data(city)
                if data:
                    temp_celsius = convert_kelvin_to_celsius(data["main"]["temp"])
                    weather_data[city].append({
                        "temp": temp_celsius, 
                        "main": data["weather"][0]["main"],
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"]
                    })
                    logging.info(f"Weather data processed for {city}: Temp {temp_celsius}C")
                    
                    if len(weather_data[city]) > 1 and temp_celsius > 35:
                        trigger_alert(city, temp_celsius, 35)
                else:
                    logging.error(f"Failed to fetch weather data for {city}")
            
            if len(weather_data[CITIES[0]]) % 5 == 0:
                daily_summaries = {
                    city: aggregate_daily_data(city, weather_data[city])
                    for city in CITIES
                }
                for city, summary in daily_summaries.items():
                    store_daily_summary(city, summary)
                visualize_data(daily_summaries)

        except Exception as e:
            logging.error(f"Error during weather data processing: {e}")

    logging.info("Starting weather monitoring system...")
    scheduler.add_job(get_weather, "interval", seconds=10, max_instances=1)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Weather monitoring system stopped.")

def visualize_data(daily_summaries):
    try:
        cities = list(daily_summaries.keys())
        avg_temps = [daily_summaries[city]["avg_temp"] for city in cities]
        avg_humidity = [daily_summaries[city]["avg_humidity"] for city in cities]
        avg_wind_speed = [daily_summaries[city]["avg_wind_speed"] for city in cities]
        
        plt.figure(figsize=(12, 10))
        
        plt.subplot(3, 1, 1)
        plt.bar(cities, avg_temps)
        plt.ylabel("Avg Temp (Celsius)")

        plt.subplot(3, 1, 2)
        plt.bar(cities, avg_humidity)
        plt.ylabel("Avg Humidity (%)")

        plt.subplot(3, 1, 3)
        plt.bar(cities, avg_wind_speed)
        plt.ylabel("Avg Wind Speed (m/s)")

        plt.suptitle("Weather Summary for Cities")
        
        plt.savefig(f"weather_summary_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.png")
        logging.info("Weather summary plot saved successfully.")
        
    except Exception as e:
        logging.error(f"Error during visualization: {e}")


if __name__ == "__main__":
    start_weather_monitoring()
