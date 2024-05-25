from flask import Flask, render_template, request, jsonify
from queue import PriorityQueue
import math
import folium
from celery import Celery

app = Flask(__name__)


app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # Update with your Celery broker URL
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

# Constants for the grid
ROWS = 10000
COLS = 10000
TOP_LEFT = (39.521352181670515, -123.70724573465668)  # Example top left corner
BOTTOM_RIGHT = (37.50004159124551, -121.57799584238539)  # Example bottom right corner


def latlng_to_grid(lat, lng, top_left, bottom_right, rows, cols):
    lat_range = top_left[0] - bottom_right[0]
    lng_range = bottom_right[1] - top_left[1]
    row_size = lat_range / rows
    col_size = lng_range / cols

    row = int((top_left[0] - lat) / row_size)
    col = int((lng - top_left[1]) / col_size)
    return row, col


def grid_to_latlng(row, col, top_left, bottom_right, rows, cols):
    lat_range = top_left[0] - bottom_right[0]
    lng_range = bottom_right[1] - top_left[1]
    row_size = lat_range / rows
    col_size = lng_range / cols

    lat = top_left[0] - row * row_size
    lng = top_left[1] + col * col_size
    return lat, lng


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw_path):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
        draw_path(current)
    return path


def algorithm(draw_path, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {cube: float("inf") for row in grid for cube in row}
    f_score = {cube: float("inf") for row in grid for cube in row}
    g_score[start] = 0
    f_score[start] = h(start.getPos(), end.getPos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            return reconstruct_path(came_from, end, draw_path)

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.getPos(), end.getPos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

        draw_path(current)

    return False


class Cube:
    def __init__(self, row, col, total_rows, total_cols):
        self.row = row
        self.col = col
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.neighbors = []
        self.color = "white"

    def getPos(self):
        return self.row, self.col

    def isWall(self):
        return self.color == "black"

    def reset(self):
        self.color = "white"

    def setStart(self):
        self.color = "orange"

    def setEnd(self):
        self.color = "purple"

    def setWall(self):
        self.color = "black"

    def setPath(self):
        self.color = "blue"

    def updateNeighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isWall():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].isWall():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].isWall():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].isWall():
            self.neighbors.append(grid[self.row][self.col - 1])


def make_grid(rows, cols):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            cube = Cube(i, j, rows, cols)
            grid[i].append(cube)
    return grid

@celery.task
def find_path(start, end, obstacles):
    # Simulate heavy computation
    path = []
    for i in range(1000000):
        path.append(math.sqrt(i))
    return path

@app.route('/')
def index():
    # Calculate center of the defined area
    center_lat = (TOP_LEFT[0] + BOTTOM_RIGHT[0]) / 2
    center_lng = (TOP_LEFT[1] + BOTTOM_RIGHT[1]) / 2
    
    # Calculate the width and height of the area
    width = abs(TOP_LEFT[1] - BOTTOM_RIGHT[1])
    height = abs(TOP_LEFT[0] - BOTTOM_RIGHT[0])
    
    # Determine the zoom level based on the width or height (whichever is larger)
    zoom_level = 10 - int(math.log(max(width, height), 2))  # Adjust this factor as needed
    
    # Create folium map centered on the area with appropriate zoom level
    folium_map = folium.Map(location=[center_lat, center_lng], zoom_start=zoom_level)
    
    # Add a rectangle to represent the defined area
    folium.Rectangle(bounds=[(TOP_LEFT[0], TOP_LEFT[1]), (BOTTOM_RIGHT[0], BOTTOM_RIGHT[1])], 
                      color='blue', fill_opacity=0.1).add_to(folium_map)
    
    # Display the latitude and longitude values on the map
    folium_map.add_child(folium.LatLngPopup())
    
    # Render the HTML template with the map
    return render_template('index.html', folium_map=folium_map._repr_html_())



@app.route('/set_points', methods=['POST'])
def set_points():
    data = request.json
    start = data.get('start')
    end = data.get('end')
    obstacles = data.get('obstacles', [])

    grid = make_grid(ROWS, COLS)

    start_row, start_col = latlng_to_grid(start['lat'], start['lng'], TOP_LEFT, BOTTOM_RIGHT, ROWS, COLS)
    end_row, end_col = latlng_to_grid(end['lat'], end['lng'], TOP_LEFT, BOTTOM_RIGHT, ROWS, COLS)

    start_cube = grid[start_row][start_col]
    end_cube = grid[end_row][end_col]
    start_cube.setStart()
    end_cube.setEnd()

    for obstacle in obstacles:
        obs_row, obs_col = latlng_to_grid(obstacle['lat'], obstacle['lng'], TOP_LEFT, BOTTOM_RIGHT, ROWS, COLS)
        grid[obs_row][obs_col].setWall()

    for row in grid:
        for cube in row:
            cube.updateNeighbors(grid)

    def draw_path(cube):
        pass  # This function is used to draw the path on the map, not implemented here

    path = algorithm(draw_path, grid, start_cube, end_cube)

    if path:
        latlng_path = [(grid_to_latlng(cube.row, cube.col, TOP_LEFT, BOTTOM_RIGHT, ROWS, COLS)) for cube in path]
        return jsonify({"status": "success", "path": latlng_path})
    else:
        return jsonify({"status": "failure", "path": []})
        
        


if __name__ == "__main__":
    app.run(debug=True)
