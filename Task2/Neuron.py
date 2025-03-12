import numpy as np
from Task1.Perceptron import Perceptron

class Neuron(Perceptron):
    def __init__(self, input_size, lr=0.1, epochs=100):
        super().__init__(lr, epochs)
        self.weights = np.random.randn(input_size)
        self.bias = np.random.randn()

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def predict(self, x):
        linear_output = np.dot(self.weights, x) + self.bias
        return self.sigmoid(linear_output)