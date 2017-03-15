import numpy as np
#from scipy.spatial.distance import cdist
from random import shuffle
import collections
import pandas as pd

# TODO:
# - Add documentation
# - Remove possible redundancy
# - Graphical tools to plot the result from the SOM

def normalize(df):
    df1 = df.sub(df.mean(axis=1), axis=0)
    df2 = df1.divide(df.max(axis=1)-df.min(axis=1), axis=0)
    return df2


class SelfOrganizingMap():

    def __init__(self, train_data, num_units, sigma_initial, num_epochs=100, learning_rate_initial=1, topology="line"):
        # Train data
        self.train_data = train_data#normalize(train_data)
        self.num_features , self.num_samples = train_data.shape

        # Units
        self.num_units = num_units
        if(self.num_units%2==0):
            self.num_units += 1
        self.units = np.random.rand(self.num_units, self.num_features)

        # Epochs
        self.num_epochs = num_epochs

        # Learning Rate
        self.learning_rate_initial = learning_rate_initial
        self.learning_rate_decrease = self.num_epochs/8
        self.learning_rate = learning_rate_initial

        # Neighbourhood
        self.sigma_initial = sigma_initial
        self.sigma_decrease = self.num_epochs/(np.log(4*self.sigma_initial))
        self.sigma = self.sigma_initial

        # Topology of out space
        self.topology = topology
        self.size_neighbourhood = int(np.floor(self.num_units/2))-1
        self.map = TopologicalMap(self)

    def train(self):
        # Get list of users
        users = list(self.train_data)
        # Start training for num_epochs
        print("")
        print("* Training *")
        print("- Starting parameters: ")
        print("\t learning rate =", self.learning_rate)
        print("\t sigma =", self.sigma)
        for epoch in range(self.num_epochs):
            # Update learning rate and sigma (neighbourhood)
            self.update_learning_rate(epoch)
            self.update_sigma(epoch)

            # Shuffle users list (prevent noise fitting) and iterate over it
            shuffle(users)
            for user in users:
                # Obtain vector for user and find winning unit
                sample = np.array(self.train_data.get(user))
                diff = sample - self.map.units
                winning_unit = np.argmin(np.linalg.norm(diff,axis=1))
                # Obtain neighbourhood levels and update units accordingly
                neighbour_levels = self.map.get_neighbour_levels(winning_unit, self.sigma)
                #print(self.learning_rate)
                #s = ', '.join([str(round(vv,5)) for vv in neighbour_levels])
                #print(str(user) + " -> unit " + str(winning_unit) + "  ---:--- " + s)
                self.map.units += neighbour_levels.reshape(-1,1)*self.learning_rate*diff

        print("- Ending parameters: ")
        print("\t learning rate =", round(self.learning_rate,5))
        print("\t sigma =", round(self.sigma,5))



    # Update learning rate
    def update_learning_rate(self, epoch):
        self.learning_rate = self.learning_rate_initial*np.exp(-epoch/self.learning_rate_decrease)


    # Update sigma (neighbourhood)
    def update_sigma(self, epoch):
        self.sigma = self.sigma_initial*np.exp(-epoch/self.sigma_decrease)


    # Print results
    def print_results(self):
        print("")
        print("* Results Self Organizing Map *")
        print("")
        users = list(self.train_data)
        results = {}
        for user in users:
            sample = np.array(self.train_data.get(user))
            diff = sample - self.map.units
            winning_unit = np.argmin(np.linalg.norm(diff,axis=1))
            if (results.get(winning_unit) is None):
                 results[winning_unit] = [user]
            else:
                results[winning_unit].append(user)

        # Plot as a matrix for 2D-Grids
        if ((self.topology == "2dgrid") or (self.topology == "2dgridcirc")):
            s = []
            for i in range(self.map.side):
                ss = []
                for j in range(self.map.side):
                    if results.get(self.map.side*i+j) is not None:
                        ss.append(', '.join(results.get(self.map.side*i+j)))
                    else:
                        ss.append(' ')
                s.append(ss)
            pd.set_option('display.expand_frame_repr', False)
            print(pd.DataFrame(s))

        # Regular plot
        else:
            for i in range(self.map.num_units):
                if results.get(i) is None:
                    print(i)
                else:
                    s = ', '.join(results.get(i))
                    print(str(i) + " - " + s)


# Class for the topological out space
class TopologicalMap():

    def __init__(self, som):
        self.topology = som.topology
        if (self.topology == "2dgrid"):
            self.num_units = som.num_units**2
            self.side = int(np.sqrt(self.num_units))
            self.grid = np.mgrid[0:self.side:1, 0:self.side:1]
        elif (self.topology == "2dgridcirc"):
            self.num_units = som.num_units**2
            self.side = int(np.sqrt(self.num_units))
            X,Y = np.mgrid[-self.side//2:self.side//2+.1:1, -self.side//2:self.side//2+.1:1]
            self.neighbourhood_idx = abs(X)+abs(Y)
        else:
            self.num_units = som.num_units
            self.neighbourhood_idx = np.array([k for k in range(self.num_units)])
        self.units = np.random.rand(self.num_units, som.num_features)


    def get_neighbour_levels(self, win_idx, sigma):

        # Simple line
        if (self.topology == "line"):
            # Obtain upper and lower limits
            #lower_limit = max(unit_idx-self.size_neigh, 0)
            #upper_limit = min(unit_idx+self.size_neigh+1, self.num_units-1)

            # Obtain neighbourhood of winning unit
            neighbourhood_levels = np.exp(-(self.neighbourhood_idx-win_idx)**2/(2*sigma**2))
            return neighbourhood_levels
            #v[range(lower_limit, upper_limit)] = 1

        # Like the line, but first and last coefficients are connected
        elif (self.topology == "circle"):
            dist = self.neighbourhood_idx - int((self.num_units-1)/2)
            neighbourhood_levels = np.exp(-(dist)**2/(2*sigma**2))
            neighbourhood_levels = np.roll(neighbourhood_levels, win_idx-int(self.num_units/2))
            return neighbourhood_levels

        elif (self.topology == "2dgrid"):
            # Define grid with distances to the wining unit
            x = self.grid[0][win_idx//int(self.side)][win_idx%int(self.side)]
            y = self.grid[1][win_idx//int(self.side)][win_idx%int(self.side)]
            dist = abs(self.grid[0]-x) + abs(self.grid[1]-y)
            # Apply 2D Gaussian
            neighbourhood_levels = np.exp(-(dist)**2/(2*sigma**2))
            #print("winning unit: " + str(win_idx))
            #print(neighbourhood_levels)
            # Convert to array
            neighbourhood_levels = neighbourhood_levels.reshape(1,-1)
            return neighbourhood_levels

        # TODO: Circular 2D-Grid
        elif (self.topology == "2dgridcirc"):
            # Shift matrix to the winning unit
            dist = np.roll(self.neighbourhood_idx,win_idx-int((num_units+1)/2))
            # Apply 2D Gaussian
            neighbourhood_levels = np.exp(-(dist)**2/(2*sigma**2))
            # Convert to array
            neighbourhood_levels = neighbourhood_levels.reshape(1,-1)
            return neighbourhood_levels
        #elif (self.topology is "sphere"):

        else:
            print("not valid topology")
            return 0