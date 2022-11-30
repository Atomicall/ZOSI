import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from tqdm import tqdm

class Hopfield_Network:
    weights: np.matrix
    num_neuron: int
    vectors_list: list[np.ndarray]
    num_iter: int
    threshold: int

    def train_weights(self, vector_list):
        self.vectors_list = vector_list
        num_data =  len(self.vectors_list)
        self.num_neuron = self.vectors_list[0].shape[0]
        # initialize weights
        W = np.zeros((self.num_neuron, self.num_neuron))
        # rho = np.sum([np.sum(t) for t in self.vectors_list]) / (num_data*self.num_neuron)
        
        # Hebb rule
        for i in tqdm(range(num_data)):
            t = self.vectors_list[i] 
            W += np.outer(t, t)
        
        # Make diagonal element of W into 0
        diagW = np.diag(np.diag(W))
        W = W - diagW
        #W /= num_data
        self.weights = W 


    def energy(self, s):
        return -0.5 * s @ self.weights @ s  + np.sum(s * self.threshold)


    def _run(self, init_s):
        """
        Synchronous update
        """
        # Compute initial state energy
        s = init_s
        e = self.energy(s)
        
        # Iteration
        for i in range(self.num_iter):
            # Update s
            s = np.sign(self.weights @ s - self.threshold)
            # Compute new state energy
            e_new = self.energy(s)
            
            # s is converged
            if e == e_new:
                return s
            # Update energy
            e = e_new
        return s


    def predict(self, test_vector_list, num_iter=20, threshold=0):
        self.num_iter = num_iter
        self.threshold = threshold
        
        predicted_list = []
        # Copy to avoid call by reference 
        for i, test in enumerate(test_vector_list):
            print(f"\tStarting predicting image #{i}...")
            copied_data = np.copy(test)

            predicted = []
            # Define predict list
            for i in tqdm(range(len(copied_data))):
                predicted.append(self._run(copied_data[i]))
            predicted_list.append(predicted)
        return predicted_list
