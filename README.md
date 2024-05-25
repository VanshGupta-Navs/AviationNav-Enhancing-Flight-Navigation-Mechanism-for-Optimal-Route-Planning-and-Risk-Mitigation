# Weather and Route Planning Application

This Flask application integrates weather data retrieval, scenario identification based on weather conditions, and route planning using the A* algorithm. It provides both API endpoints and a user interface for interacting with the functionalities.

## Features

### 1. Weather Data Retrieval

- Fetches real-time weather data for a specified city using the OpenWeatherMap API.
- Stores the weather information in an SQLite database for future reference.

### 2. Scenario Identification

- Identifies weather scenarios for stored cities based on specific weather conditions:
    - High temperature (> 35°C)
    - Low visibility (< 1000 meters)
    - High wind speed (> 15 m/s)
    - Extreme conditions (temperature > 60°C or wind speed > 30 m/s)
    - High humidity (> 90%)

### 3. Route Planning

- Plans the optimal route between two cities considering weather conditions.
- Utilizes the A* algorithm for pathfinding.
- Considers weather-related factors such as wind speed and temperature when calculating the optimal route.

## Setup

### Prerequisites

- Python 3.x installed on your system.
- Internet connection to fetch real-time weather data.
- Dependencies listed in `requirements.txt` installed.

### Installation

1. Clone this repository to your local machine:

    ```bash
    git clone <repository_url>
    ```

2. Navigate to the project directory:

    ```bash
    cd <project_directory>
    ```

3. Install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

- Ensure that the `weather_data.db` SQLite database file has read/write permissions.
- Modify the `api_key` variable in `fetch_weather` function with your OpenWeatherMap API key.
- Update the database name, API endpoints, and any other configuration in the Flask application as required.

## Usage

1. **Running the Application**:

    Execute the following command to start the Flask development server:

    ```bash
    python app.py
    ```

    This will start the server, and the application will be accessible at `http://localhost:5000/`.

2. **API Endpoints**:

    - `/get_weather` (POST): Accepts a city name and returns weather information.
    - `/scenarios` (GET): Returns identified weather scenarios for stored cities.
    - `/plan_route` (POST): Accepts start and end cities, plans the optimal route considering weather conditions, and returns the route.

3. **Frontend**:

    The frontend of the application can be accessed by visiting the root URL (`http://localhost:5000/`). It provides a user interface to interact with the API endpoints.

## Contributing

Contributions are welcome! If you'd like to enhance this application, please fork the repository and create a new branch for your feature. After implementing your changes, submit a pull request, and we'll review it.

**This code is still under development, feel free to add your contributions**
