import numpy as np
import plotly.graph_objects as go

# Generování náhodných bodů
x = np.random.uniform(-10, 10, 100)
y = np.random.uniform(-10, 10, 100)

# Koeficienty pro rovnici přímky y = ax + b
a, b = 0.5, 2

# signum activation function
def signum(x):
    return np.where(x >= 0, 1, -1)

class Perceptron:
    def __init__(self, lr=0.1, epochs=100):
        self.lr = lr  # learning rate
        self.epochs = epochs  # počet epoch
        self.weights = np.random.randn(2)  # váhy (pro x a y)
        self.bias = np.random.randn()  # bias

    def predict(self, x):
        linear_output = np.dot(self.weights, x) + self.bias
        return signum(linear_output)

    def train(self, X, y):
        for _ in range(self.epochs):
            for i in range(len(X)):
                prediction = self.predict(X[i])
                error = y[i] - prediction
                self.weights += self.lr * error * X[i]  # aktualizace vah
                self.bias += self.lr * error  # aktualizace biasu

# Příprava dat na trénování
X_train = np.column_stack((x, y))
y_train = np.where(y > (a * x + b), 1, -1)  # Labely pro trénování

# Trénování perceptronu
perceptron = Perceptron()
perceptron.train(X_train, y_train)

# Predikce
labels = np.array([perceptron.predict([x[i], y[i]]) for i in range(len(x))])

colors = {1: 'blue', -1: 'red'}

fig = go.Figure()

# Vykreslení bodů
for label in np.unique(labels):
    mask = labels == label
    fig.add_trace(go.Scatter(
        x=x[mask], y=y[mask],
        mode='markers',
        marker=dict(color=colors[label]),
        name={1: 'Above', -1: 'Below'}[label]
    ))

# Nakreslení přímky
x_line = np.linspace(-10, 10, 100)
y_line = a * x_line + b
fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name='Decision Boundary', line=dict(color='black')))

fig.update_layout(title='Perceptron Classification of Points', xaxis_title='x', yaxis_title='y')
fig.show()