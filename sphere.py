import numpy as np
from constants import G

class Sphere(object):
    def __init__(self, radius, mass):
        self.radius = radius
        self.mass = mass
        self.volume = 4.0 * np.pi * radius ** 3 / 3.0
        self.impact_area = np.pi * radius ** 2
        self.density = self.mass / self.volume
        self.attraction = G * self.mass
