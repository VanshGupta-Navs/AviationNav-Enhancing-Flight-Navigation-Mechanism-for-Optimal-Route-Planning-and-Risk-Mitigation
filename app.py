from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import sqlite3
import math
import json
import heapq
import logging

app = Flask(__name__)

def create_database(city_name=None, weather_info=None, flight_info=None):
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departure_city TEXT,
            arrival_city TEXT,
            outbound_date TEXT,
            return_date TEXT,
            price REAL,
            currency TEXT
        )
    ''')
    conn.commit()
    
    if city_name and weather_info:
        insert_weather_data(conn, city_name, weather_info)
    
    if flight_info:
        insert_flight_data(conn, flight_info)
    
    conn.close()

def insert_weather_data(conn, city_name, weather_info):
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

def insert_flight_data(conn, flight_info):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flights (
            departure_city, arrival_city, outbound_date, return_date, price, currency
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        flight_info['departure_city'], flight_info['arrival_city'], flight_info['outbound_date'],
        flight_info['return_date'], flight_info['price'], flight_info['currency']
    ))
    conn.commit()

def fetch_weather(city_name):
    api_key = "37857d75384b1e66067f16b3829b109e"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_info = {
            'coordinates': data['coord'],
            'temperature': data['main']['temp'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'sea_level': data['main'].get('sea_level'),
            'ground_level': data['main'].get('grnd_level'),
            'visibility': data['visibility'],
            'wind_speed': data['wind']['speed'],
            'country': data['sys']['country'],
            'sunrise': data['sys']['sunrise'],
            'sunset': data['sys']['sunset']
        }
        create_database(city_name, weather_info)
    else:
        weather_info = {'error': data.get('message', 'Failed to retrieve data')}
    
    return weather_info

def fetch_flights(departure_id, arrival_id, outbound_date, return_date):
    api_key = "65380562e4c04a87f32c8843b5e0544350e0e3b34b33af05dc8fe2970d459027"
    url = f"https://serpapi.com/search.json?engine=google_flights&departure_id={departure_id}&arrival_id={arrival_id}&outbound_date={outbound_date}&return_date={return_date}&currency=USD&hl=en&api_key={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        flight_info = {
            'departure_city': departure_id,
            'arrival_city': arrival_id,
            'outbound_date': outbound_date,
            'return_date': return_date,
            'price': data['price'],
            'currency': data['currency']
        }
        create_database(flight_info=flight_info)
    else:
        flight_info = {'error': data.get('message', 'Failed to retrieve data')}
    
    return flight_info

def identify_scenarios():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weather')
    rows = cursor.fetchall()

    scenarios = {}
    for row in rows:
        city_name, coordinates, temperature, pressure, humidity, sea_level, ground_level, visibility, wind_speed, country, sunrise, sunset = row[1:]

        conditions = {
            'coordinates': json.loads(coordinates.replace("'", '"')),
            'temperature': temperature,
            'pressure': pressure,
            'humidity': humidity,
            'sea_level': sea_level,
            'ground_level': ground_level,
            'visibility': visibility,
            'wind_speed': wind_speed,
            'country': country,
            'sunrise': sunrise,
            'sunset': sunset
        }

        if temperature > 308.15:  # High temperature
            scenarios[city_name] = conditions
            scenarios[city_name]['scenario'] = "High temperature detected."
        
        if visibility < 1000:  # Low visibility
            scenarios[city_name] = conditions
            scenarios[city_name]['scenario'] = "Low visibility detected."
        
        if wind_speed > 15:  # High wind speed
            scenarios[city_name] = conditions
            scenarios[city_name]['scenario'] = "High wind speed detected."
        
        if temperature > 333.15 or wind_speed > 30:
            scenarios[city_name] = conditions
            scenarios[city_name]['scenario'] = "Extreme conditions detected."

        if humidity > 50:  # High humidity
            scenarios[city_name] = conditions
            scenarios[city_name]['scenario'] = "High humidity detected."
        scenarios[city_name] = conditions
    conn.close()
    return scenarios

# ROUTE PLANNING -------------------------------------------------------------------------------------------------------------------
# Step 1: Graph Representation

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)
        self.edges[value] = []

    def add_edge(self, from_node, to_node, distance):
        if from_node not in self.nodes:
            self.add_node(from_node)
        if to_node not in self.nodes:
            self.add_node(to_node)
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance

# Step 2: Weather Data Integration

def update_graph_with_weather(graph, weather_data):
    for city, conditions in weather_data.items():
        if conditions.get('error'):
            continue
        # Example: Increase distance if high wind speed
        if conditions['wind_speed'] > 15:
            for neighbor in graph.edges[city]:
                graph.distances[(city, neighbor)] *= 1.5  # Adjust factor as needed

def get_distance(lat1, lon1, lat2, lon2):
    if None in (lat1, lon1, lat2, lon2):
        return float("nan")
    degRad = 2 * math.pi / 360
    distance = 6.370e6 * math.acos(
        math.sin(lat1 * degRad) * math.sin(lat2 * degRad)
        + math.cos(lat1 * degRad)
        * math.cos(lat2 * degRad)
        * math.cos((lon2 - lon1) * degRad)
    )
    return distance

# Haversine formula to calculate distance between two points on the Earth
def haversine(coord1, coord2):
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    print(f"Haversine distance between {coord1} and {coord2}: {distance} km")
    return distance

# Step 3: A* Algorithm Implementation

def heuristic(node, end_node, city_coordinates):
    coord1 = city_coordinates[node]
    coord2 = city_coordinates[end_node]
    distance = haversine(coord1, coord2)
    print(f"Heuristic distance from {node} to {end_node}: {distance} km")
    return distance

def astar(graph, start, end, city_coordinates):
    queue = []
    heapq.heappush(queue, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while queue:
        current = heapq.heappop(queue)[1]

        if current == end:
            break

        for neighbor in graph.edges[current]:
            new_cost = cost_so_far[current] + graph.distances[(current, neighbor)]
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end, city_coordinates)
                heapq.heappush(queue, (priority, neighbor))
                came_from[neighbor] = current

    # Reconstruct path
    path = []
    while current:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# --------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city_name = request.form.get('city_name')
    weather_data = fetch_weather(city_name)
    return jsonify(weather_data)

# @app.route('/get_flights', methods=['POST'])
# def get_flights():
#     departure_id = request.form.get('departure_id')
#     arrival_id = request.form.get('arrival_id')
#     outbound_date = request.form.get('outbound_date')
#     return_date = request.form.get('return_date')
#     flight_data = fetch_flights(departure_id, arrival_id, outbound_date, return_date)
#     return jsonify(flight_data)

@app.route('/scenarios')
def scenarios():
    scenarios = identify_scenarios()
    return jsonify(scenarios)

# Update the plan_route function to handle missing city names
@app.route('/plan_route', methods=['POST'])
def plan_route():
    start = request.form.get('start').lower()
    end = request.form.get('end').lower()
    weather_data = identify_scenarios()
    graph = Graph()
    
    # Add nodes to the graph
    for city in weather_data.keys():
        graph1 = graph.add_node(city.lower())
        # graph1 = graph.add_node
        logging.info(graph1)

    # Fetch city coordinates dynamically
    city_coordinates = {city.lower(): (conditions['coordinates']['lat'], conditions['coordinates']['lon']) for city, conditions in weather_data.items() if 'coordinates' in conditions}

    # Add edges dynamically based on distances
    cities = list(city_coordinates.keys())
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            city1 = cities[i]
            city2 = cities[j]
            if city1 in graph.edges and city2 in graph.edges:
                distance = haversine(city_coordinates[city1], city_coordinates[city2])
                print(f"Distance between {city1} and {city2}: {distance} km")
                graph.add_edge(city1, city2, distance)

    update_graph_with_weather(graph, weather_data)
    
    if start not in graph.edges or end not in graph.edges:
        return jsonify({'error': 'Start or end city not found in the graph.'})
    
    optimal_route = astar(graph, start, end, city_coordinates)
    
    print(f"Optimal route from {start} to {end}: {optimal_route}")
    
    return jsonify({
        'start': start,
        'end': end,
        'route': optimal_route
    })


if __name__ == '__main__':
    create_database()  # Ensure the database is created at the start
    app.run(debug=True)