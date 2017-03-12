import numpy as np
from scipy.spatial.distance import cdist
from random import shuffle
import collections

class self_organizing_map():

    def __init__(self, train_data, num_units, topology="line", num_epochs=100, learning_rate=0.1):
        self.map = topological_map(num_units, topology='circle')
        self.train_data = train_data
        self.num_features , self.num_samples = train_data.shape
        self.num_units = num_units
        self.num_epochs = num_epochs
        self.units = np.random.rand(num_units, self.num_features)
        self.learning_rate = learning_rate

    def train(self):
        users = list(self.train_data)
        for i in range(self.num_epochs):
            if (i == 25):
                self.map.set_size_neighbourhood(1)
            elif (i == 60):
                self.map.set_size_neighbourhood(0)

            shuffle(users)
            for user in users:
                sample = np.array(self.train_data.get(user))
                diff = sample - self.units
                winning_unit = np.argmin(np.linalg.norm(diff,axis=1))
                distance = self.map.get_neighbours(winning_unit)
                self.units += distance.reshape(-1,1)*self.learning_rate*diff

    def print_results(self):
        print("")
        print("** Results Self Organizing Map **")
        print("")
        users = list(self.train_data)
        results = {}
        for user in users:
            sample = np.array(self.train_data.get(user))
            diff = sample - self.units
            winning_unit = np.argmin(np.linalg.norm(diff,axis=1))
            if (results.get(winning_unit) is None):
                 results[winning_unit] = [user]
            else:
                results[winning_unit].append(user)

        for i in range(self.num_units):
            if results.get(i) is None:
                print(i)
            else:
                s = ', '.join(results.get(i))
                print(str(i) + " - " + s)


class topological_map():

    def __init__(self, num_units, topology="line", size_neighbourhood=2):
        self.topology = topology
        self.num_units = num_units
        self.size_neigh = size_neighbourhood


    def set_size_neighbourhood(self, size_neighbourhood):
        self.size_neigh = size_neighbourhood


    def get_neighbours(self, unit_idx):
        v = np.zeros(self.num_units)
        if (self.topology is "line"):
            lower_limit = max(unit_idx-self.size_neigh, 0)
            upper_limit = min(unit_idx+self.size_neigh+1, self.num_units-1)
            v[range(lower_limit, upper_limit)] = 1

        elif (self.topology is "circle"):
            lower_limit = unit_idx-self.size_neigh
            upper_limit = unit_idx+self.size_neigh+1

            if (lower_limit < 0):
                v = np.ones(self.num_units)
                lower_limit = self.num_units + lower_limit
                v[upper_limit+1:lower_limit] = 0
            elif(upper_limit > self.num_units-1):
                v = np.ones(self.num_units)
                upper_limit = (upper_limit)%self.num_units +1
                v[upper_limit+1:lower_limit] = 0
            else:
                v[range(lower_limit, upper_limit)] = 1

        #elif (self.topology is "2dgrid"):

        #elif (self.topology is "sphere"):

        else:
            print("not valid topology")

        return v