import numpy as np

class System(object):
    def __init__(self, actors, test_mass_field, evolver, dt, edges, spawner, constraints=(), starttime=0.0):
        self.actors = actors
        self.tmf = test_mass_field
        self.constraints = constraints
        self.time = starttime
        self.evolver = evolver
        self.dt = dt
        self.currstep = 0
        self.collisions = []
        self.spawner = spawner
        self.edges = edges

    def step(self):
        actor_acc = self.get_actor_acc()
        testmass_acc = self.get_testmass_acc()
        for i in xrange(len(self.actors)):
            self.evolver(self, self.actors[i], actor_acc[i])
        self.evolver(self, self.tmf, testmass_acc)
        self.time += self.dt
        collision = self.check_collisions()
        self.check_outside_edges()
        return collision

    def get_actor_acc(self):
        acc = np.zeros((len(self.actors), 3))
        for i in xrange(len(self.actors)):
            for j in xrange(len(self.actors)):
                if i != j:
                    acc[i] += self.actors[j].attraction * (self.actors[j].pos - self.actors[i].pos) / np.linalg.norm(self.actors[j].pos - self.actors[i].pos) ** 3
        return acc

    def get_testmass_acc(self):
        acc = np.zeros(np.shape(self.tmf.pos))
        for j in xrange(len(self.actors)):
            distancecubed = np.sqrt(np.sum((self.actors[j].pos - self.tmf.pos) ** 2, 1)) ** 3
            acc += (self.actors[j].attraction * (self.actors[j].pos - self.tmf.pos) / distancecubed[:, None])
        return acc
    
    def check_collisions(self):
        ret = False
        for j in xrange(len(self.actors)):
            distance = np.sqrt(np.sum((self.actors[j].pos - self.tmf.pos)**2, 1))
            if any(distance < self.actors[j].radius):
                ret = True
                self.collisions.append(j)
                collision_event(distance<self.actors[j].radius)
#                collision_event(np.arange(len(self.tmf.pos))[distance<self.actors[j].radius])
        return ret
    
    def collision_event(self, test_mass_numbers):
        if "constant test mass number" in constraint:
            self.tmf.pos[test_mass_numbers], self.tmf.vel[test_mass_numbers] = self.spawner(np.sum(test_mass_numbers == True))

    def check_outside_edges(self):
        replace_ast = self.tmf.pos[:, 0] < self.edges[0, 0]
        replace_ast = replace_ast | (self.tmf.pos[:, 0] > self.edges[0, 1])
        replace_ast = replace_ast | (self.tmf.pos[:, 1] < self.edges[1, 0])
        replace_ast = replace_ast | (self.tmf.pos[:, 1] > self.edges[1, 1])
        replace_ast = replace_ast | (self.tmf.pos[:, 2] < self.edges[2, 0])
        replace_ast = replace_ast | (self.tmf.pos[:, 2] > self.edges[2, 1])
        self.tmf.pos[replace_ast], self.tmf.vel[replace_ast] = self.spawner(np.sum(replace_ast == True))
