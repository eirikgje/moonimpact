import numpy as np

def spawn_edge_asteroids(num_asteroids, velprior, posprior, edges):
    tot_num_asteroids = 0
    for edgedir in xrange(len(edges)):
        if not np.all(edges[edgedir, :]) == 0:
            tot_num_asteroids += 2 * num_asteroids
    velocities = np.empty([tot_num_asteroids, 3])
    positions = np.empty([tot_num_asteroids, 3])
    count = 0
    for edgedir in xrange(len(edges)):
        if np.all(edges[edgedir,:]) == 0:
            continue
        for direction in xrange(len(velprior)):
            vels = velprior[direction].draw_samples(2 * num_asteroids)
            if edgedir == direction:
                pos = np.array(num_asteroids * [edges[edgedir, 0]])
                pos = np.append(pos, np.array(num_asteroids * [edges[edgedir, 1]]))
            else:
                pos = posprior[direction].draw_samples(2 * num_asteroids)
            positions[count*2*num_asteroids:(count+1)*2*num_asteroids, direction] = pos
            velocities[count*2*num_asteroids:(count+1)*2*num_asteroids, direction] = vels
        count += 1
    return AsteroidField(positions, velocities)

class AsteroidField(object):
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def append_field(self, field):
        npos = np.append(self.pos, field.pos)
        nvels = np.append(self.vel, field.vel)
        return AsteroidField(npos, nvels)

class AsteroidEdgeSpawner(object):
    def __init__(self, velprior, posprior, edges):
        self.velprior = velprior
        self.posprior = posprior
        self.edges = edges

    def __call__(self, num_asteroids):
        velocities = np.empty([num_asteroids, 3])
        positions = np.empty([num_asteroids, 3])
        for i in range(num_asteroids):
            found = False
            while not found:
                edgedir = np.floor(3 * np.random.rand())
                if not np.all(self.edges[edgedir, :] == 0):
                    found = True
            sec_ind = np.floor(2 * np.random.rand())
            for direction in xrange(len(self.velprior)):
                velocities[i, direction] = self.velprior[direction].draw_samples(1)
                if edgedir == direction:
                    positions[i, direction] = self.edges[edgedir, sec_ind]
                else:
                    positions[i, direction] = self.posprior[direction].draw_samples(1)
        return positions, velocities
