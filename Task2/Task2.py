import numpy as np
from Neuron import Neuron

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, lr=0.1, epochs=10000):
        self.lr = lr
        self.epochs = epochs
        self.hidden_layer = [Neuron(input_size, lr, epochs) for _ in range(hidden_size)]
        self.output_layer = [Neuron(hidden_size, lr, epochs) for _ in range(output_size)]

    def forward(self, x):
        hidden_outputs = np.array([neuron.predict(x) for neuron in self.hidden_layer])
        output = np.array([neuron.predict(hidden_outputs) for neuron in self.output_layer])
        return hidden_outputs, output

    def train(self, X, y):
        y = y.reshape(-1, 1)
        for _ in range(self.epochs):
            for i in range(len(X)):

                hidden_outputs, output = self.forward(X[i])

                output_error = y[i] - output
                output_delta = output_error * self.output_layer[0].sigmoid_derivative(output)


                for j, neuron in enumerate(self.output_layer):
                    neuron.weights += neuron.lr * output_delta[j] * hidden_outputs
                    neuron.bias += neuron.lr * output_delta[j]


                hidden_error = np.dot(output_delta, np.array([neuron.weights for neuron in self.output_layer]))

                hidden_delta = hidden_error * np.array([neuron.sigmoid_derivative(hidden_outputs[j]) for j, neuron in enumerate(self.hidden_layer)])

                for j, neuron in enumerate(self.hidden_layer):
                    neuron.weights += neuron.lr * hidden_delta[j] * X[i]
                    neuron.bias += neuron.lr * hidden_delta[j]


X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 1, 1, 0])

nn = NeuralNetwork(input_size=2, hidden_size=2, output_size=1, lr=0.1, epochs=10000)

nn.train(X, y)

predictions = np.array([nn.forward(x)[1] for x in X])

print("Predictions:")
print(predictions)