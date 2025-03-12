import numpy as np

class Perceptron:
    def __init__(self, lr=0.1, epochs=100):
        self.lr = lr  # learning rate
        self.epochs = epochs  # počet epoch
        self.weights = np.random.randn(2)  # váhy (pro x a y)
        self.bias = np.random.randn()  # bias

    # signum activation function
    def signum(self, x):
        return np.where(x >= 0, 1, -1)


    def predict(self, x):
        linear_output = np.dot(self.weights, x) + self.bias
        return self.signum(linear_output)

    def train(self, X, y):
        for _ in range(self.epochs):
            for i in range(len(X)):
                prediction = self.predict(X[i])
                error = y[i] - prediction
                self.weights += self.lr * error * X[i]  # aktualizace vah
                self.bias += self.lr * error  # aktualizace biasu