import numpy as np

def leapfrog(self, obj, acc):
    obj.vel += acc * self.dt
    obj.pos += obj.vel * self.dt
