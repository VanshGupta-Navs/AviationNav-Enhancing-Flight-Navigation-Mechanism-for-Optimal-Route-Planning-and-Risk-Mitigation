import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT,
            coordinates TEXT,
            temperature REAL,
            pressure REAL,
            humidity REAL,
            sea_level REAL,
            ground_level REAL,
            visibility INTEGER,
            wind_speed REAL,
            country TEXT,
            sunrise INTEGER,
            sunset INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_weather_data(city_name, weather_info):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO weather (
            city_name, coordinates, temperature, pressure, humidity, sea_level,
            ground_level, visibility, wind_speed, country, sunrise, sunset
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        city_name, str(weather_info['coordinates']), weather_info['temperature'],
        weather_info['pressure'], weather_info['humidity'], weather_info['sea_level'],
        weather_info['ground_level'], weather_info['visibility'], weather_info['wind_speed'],
        weather_info['country'], weather_info['sunrise'], weather_info['sunset']
    ))
    conn.commit()
    conn.close()
