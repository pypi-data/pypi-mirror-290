from shapely.geometry import Point, Polygon, LineString
from shapely.affinity import translate, rotate, scale
import matplotlib.pyplot as plt
from shapely.plotting import plot_polygon, plot_points
from shapely.geometry import CAP_STYLE
import numpy as np


class Node:
    def __init__(self, x, y):
        self.point = Point(x, y)

    def get_point(self):
        return self.point

class Scenario:
    def __init__(self, grid_size=(60, 60), min_distance=10):
        #min_distance é a menor distância entre os obstáculos
        self.grid_size = grid_size
        self.min_distance = min_distance
        self.start = None
        self.end = None
        self.obstacles = []

    def set_start(self, x, y):
        self.start = Node(x, y)

    def set_end(self, x, y):
        self.end = Node(x, y)

    def is_valid_position(self, new_obstacle):
        for obstacle in self.obstacles:
            if new_obstacle.distance(obstacle) < self.min_distance:
                return False
        return True

    def add_obstacle(self, obstacle, position=(0, 0)):
        dx, dy = position
        obstacle = translate(obstacle, dx, dy)

        if self.is_valid_position(obstacle):
            self.obstacles.append(obstacle)
            print("Obstacle added.")
        else:
            print("Obstacle not added. Minimum distance requirement not met.")

    def check_path_collision(self, path_points):

        for obstacle in self.obstacles:
            for i in range(1, len(path_points)):
                line_segment = LineString([path_points[i-1], path_points[i]])
                if line_segment.intersects(obstacle):
                    return True  # Colisão detectada
        return False  # Nenhuma colisão
    
    def check_path_collision2(self, path_points, robot_radius):

        for obstacle in self.obstacles:
            expanded_obstacle = obstacle.buffer(robot_radius, cap_style=CAP_STYLE.round)
            for i in range(1, len(path_points)):
                line_segment = LineString([path_points[i-1], path_points[i]])
                if line_segment.intersects(expanded_obstacle):
                    return True  # Colisão detectada
        return False  # Nenhuma colisão

    def plot_scenario(self, grid=False):
        fig, ax = plt.subplots()
            
        ax.set_xlim(0, self.grid_size[0])
        ax.set_ylim(0, self.grid_size[1])

        if self.start:
            plot_points(self.start.get_point(), ax=ax, color='green', markersize=10, label='Start')

        if self.end:
            plot_points(self.end.get_point(), ax=ax, color='red', markersize=10, label='End')

        for obstacle in self.obstacles:
            plot_polygon(obstacle, ax=ax, add_points=False, color='grey')
        
        if grid:
            plt.grid(True)
        plt.gca().set_aspect('equal', adjustable='box')
        #plt.show()