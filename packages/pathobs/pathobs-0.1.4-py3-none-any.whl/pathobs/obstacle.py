from shapely.geometry import Point, Polygon, LineString
from shapely.affinity import translate, rotate, scale
import matplotlib.pyplot as plt
from shapely.plotting import plot_polygon, plot_points
from shapely.geometry import CAP_STYLE
import numpy as np

class ObstacleFactory:

    L_SHAPE = [(0, 5), (0, 0), (5, 0), (5, -5), (-5, -5), (-5, 5), (0, 5)]

    H_SHAPE = [(-12, -20), (-12, 20), (-4, 20), (-4, 4), (4, 4), (4, 20), (12, 20), (12, -20),
     (4, -20), (4, -4), (-4, -4), (-4, -20), (-12, -20)]

    @staticmethod
    def _reduce_polygon(polygon, scale_factor):
        
        centroid = polygon.centroid
        reduced_geom = scale(polygon, xfact=scale_factor, yfact=scale_factor, origin=centroid)
        return reduced_geom

    @staticmethod
    def create_circle(radius, rotation=0):
        # Cria um círculo com o raio especificado
        circle = Point(0, 0).buffer(radius)
        return rotate(circle, rotation, origin='centroid')

    @staticmethod
    def create_square(side_length, rotation=0):
        # Cria um quadrado com lado especificado
        half_side = side_length / 2
        square = Polygon([
            (-half_side, -half_side),
            (half_side, -half_side),
            (half_side, half_side),
            (-half_side, half_side),
            (-half_side, -half_side)
        ])
        return rotate(square, rotation, origin='centroid')

    @staticmethod
    def create_L(size=1, rotation=0):
        # Cria um L com o tamanho especificado
        polygon = Polygon(ObstacleFactory.L_SHAPE)
        scaled_polygon = ObstacleFactory._reduce_polygon(polygon, size)
        return rotate(scaled_polygon, rotation, origin='centroid')

    @staticmethod
    def create_H(size=1, rotation=0):
        # Cria um H com o tamanho especificado
        polygon = Polygon(ObstacleFactory.H_SHAPE)
        scaled_polygon = ObstacleFactory._reduce_polygon(polygon, size)
        return rotate(scaled_polygon, rotation, origin='centroid')
