import numpy as np
from sphere import Sphere
from system import System
from asteroids import spawn_edge_asteroids, AsteroidEdgeSpawner
from priors import GaussianPrior, UniformPrior
from evolution import leapfrog
import matplotlib.pyplot as plt

num_asteroids = 100
x_range = -1e10, 1e10
y_range = -1e10, 1e10
z_range = -1e10, 1e10
x_speedmax = 10e3
y_speedmax = 10e3
z_speedmax = 10e3

M_EARTH = 5.97219e24
M_MOON = 7.34767309e22
PERIOD = 27.321582 * 24 * 60 * 60
MOON_DIS_TO_EARTH = 384405e3
EARTH_DIS_TO_BARYCENTER = M_MOON * MOON_DIS_TO_EARTH / (M_MOON + M_EARTH)
MOON_DIS_TO_BARYCENTER = MOON_DIS_TO_EARTH - EARTH_DIS_TO_BARYCENTER
EARTH_SPEED = 2 * np.pi * EARTH_DIS_TO_BARYCENTER / PERIOD
MOON_SPEED = 2 * np.pi * MOON_DIS_TO_BARYCENTER / PERIOD

earth = Sphere(radius=6.371e3, mass=5.97219e24)
moon = Sphere(radius=1.7374e3, mass=7.34767309e22)
earth.pos = np.array([-EARTH_DIS_TO_BARYCENTER, 0, 0])
moon.pos = np.array([MOON_DIS_TO_BARYCENTER, 0, 0])
earth.vel = np.array([0, -EARTH_SPEED, 0])
moon.vel = np.array([0, MOON_SPEED, 0])

pospriors = [UniformPrior(x_range[0], x_range[1]), UniformPrior(y_range[0], y_range[1]), GaussianPrior(0, 5e3)]
velpriors = [UniformPrior(0, x_speedmax), UniformPrior(0, y_speedmax), UniformPrior(0, z_speedmax)]

#asteroids = spawn_asteroids(num_asteroids, pospriors, velpriors)
#asteroid_field = spawn_edge_asteroids(num_asteroids_per_edge, pospriors, velpriors, 0, x_range[0])
#asteroid_field = asteroid_field.append_field(spawn_edge_asteroids(num_asteroids_per_edge, pospriors, velpriors, 0, x_range[1]))
#asteroid_field = asteroid_field.append_field(spawn_edge_asteroids(num_asteroids_per_edge, pospriors, velpriors, 1, y_range[0]))
#asteroid_field = asteroid_field.append_field(spawn_edge_asteroids(num_asteroids_per_edge, pospriors, velpriors, 1, y_range[1]))
edges = np.array([x_range, y_range, [0, 0]])
asteroid_field = spawn_edge_asteroids(num_asteroids, pospriors, velpriors, edges)
spawner = AsteroidEdgeSpawner(pospriors, velpriors, edges)

edges = np.array([x_range, y_range, z_range])
m_e_sys = System([earth, moon], asteroid_field, leapfrog, 10, edges, spawner, constraints=("constant test mass number"))

plt.figure()
i = 0
#while m_e_sys.time < 60 * 60 * 24 * 10:
#    collision = m_e_sys.step()
#    if i % 100 == 0:
#        plt.scatter(m_e_sys.actors[0].pos[0], m_e_sys.actors[0].pos[1], marker='o', c='k')
#        plt.scatter(m_e_sys.actors[1].pos[0], m_e_sys.actors[1].pos[1], marker='x', c='r')
#        plt.show()
#    if collision:
#        print 'collision'
#    print m_e_sys.time
#    i += 1
