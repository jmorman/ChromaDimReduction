import numpy as np
import math
import pickle

#o   o   o reconstruction
#          weights_decode = weights_encode.T, c
#  o   o   hidden_vec
#          weights_encode = weights_decode.T, b
#o   o   o input_vec
class Autoencoder:
    
    def __init__(self, input_data, hidden_size):
        self._n = len(input_data)
        self._m = len(input_data[0])
        self._k = hidden_size
        
        self._indata = input_data
        
        self.initialize_params()
        
    def initialize_params(self):
        self._b = np.zeros(self._k)
        self._c = np.zeros(self._m)
        
        bound = math.sqrt(6) / math.sqrt(self._n+self._m)
        self._weights = 2 * bound * np.random.rand(self._k, self._m)
        self._weights = self._weights - bound
        
    def sigmoid(self, vec):
        return np.array([1.0 / (1.0+np.exp(-comp)) for comp in vec])
    
    #Tied weights
    def encode_input(self, input_vec):
        return self.sigmoid(np.dot(self._weights, input_vec) + self._b)
    
    def decode_hidden(self, hidden_vec):
        return self.sigmoid(np.dot(self._weights.T, hidden_vec) + self._c)
    
    def weights_grad(self, input_vec, hidden_vec, reconstruction):
        return np.outer(reconstruction-input_vec, hidden_vec)
    
    def c_grad(self, input_vec, reconstruction):
        return (reconstruction-input_vec)
    
    def b_grad(self, input_vec, reconstruction):
        left = np.dot(self._weights, reconstruction-input_vec)
        preactivation = self._b + np.dot(self._weights, input_vec)
        right = np.array(self.sigmoid(preactivation) * (np.ones(len(preactivation))-self.sigmoid(preactivation)))
        #Numpy elementwise multiplication of arrays (vectors here):
        return left * right

    def update_params(self, invec, hidden, recon, rate):
        new_weights = self._weights - rate*self.weights_grad(invec, hidden, recon).T
        new_c = self._c - rate*self.c_grad(invec, recon)
        new_b = self._b - rate*self.b_grad(invec, recon)
        
        self._weights = new_weights
        self._c = new_c
        self._b = new_b
        
    def cross_ent_loss(self, input_vec, reconstruction): 
        #Maybe add -sum(in*log(in)+(1-in)(1-log(in))) term to give accurate losses for non-binary inputs?
        return -sum(input_vec*np.log(reconstruction) + 
                    (np.ones(self._m)-input_vec)*np.log(np.ones(self._m)-reconstruction))
    
    def total_ave_loss(self):
        tl = 0
        for input_vector in self._indata:
            reconstruct = self.decode_hidden(self.encode_input(input_vector))
            tl = tl + self.cross_ent_loss(input_vector, reconstruct)
        return tl / self._n
        
    def train(self, num_epochs=50000, verbose=False, blr=1, delta=1e-6):
        self.initialize_params()

        #Stochastic gradient descent: estimating gradient and updating params from a single example at a time
        for i in range(num_epochs+1):
            for input_vector in self._indata:
                learning_rate = blr / (1+delta*i)
                
                #Forward propagation:
                hidden_layer = self.encode_input(input_vector)
                reconstruction = self.decode_hidden(hidden_layer)

                #Backward propagation:
                self.update_params(input_vector, hidden_layer, reconstruction, learning_rate)
            
            if(verbose and i%(num_epochs/10) == 0):
                print i, self.total_ave_loss()
        return self.total_ave_loss()


    def gridsearch(self, blr_vals, delta_vals, epochs):
        for blrv in blr_vals:
            for deltav in delta_vals:
                loss = self.train(blr=blrv, delta=deltav, num_epochs=epochs)
                print 'BLR=' + str(blrv) + ', delta=' + str(deltav) + ', finalaveloss=' + str(loss)

    def save_params(self):
        weights_filename = str(self._k) + 'x' + str(self._m) + 'weights0noise.p'
        b_filename = str(self._k) + 'x' + str(self._m) + 'b0noise.p'
        c_filename = str(self._k) + 'x' + str(self._m) + 'c0noise.p'

        weights_file = open(weights_filename, 'wb')
        b_file = open(b_filename, 'wb')
        c_file = open(c_filename, 'wb')

        pickle.dump(self._weights, weights_file)
        pickle.dump(self._b, b_file)
        pickle.dump(self._c, c_file)

        weights_file.close()
        b_file.close()
        c_file.close()
