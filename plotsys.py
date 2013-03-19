import matplotlib.pyplot as plt
import numpy as np

def plot_sphere(sphere, marker='o', color='k'):
    plt.scatter(sphere.pos[0], sphere.pos[1], marker=marker, color=color)

def plot_asteroid(field, number, marker='+', color='b'):
    plt.scatter(field.pos[number, 0], field.pos[number, 1], marker=marker, color=color)

def plot_step(system):
    number = 37
    plot_sphere(system.actors[0], 'o', 'k')
    plot_sphere(system.actors[1], 'x', 'r')
    plot_asteroid(system.tmf, number)
    for i in range(1000):
        system.step()

