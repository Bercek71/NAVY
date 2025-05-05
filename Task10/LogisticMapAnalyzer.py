from LogisticMap import LogisticMap
from Visualizer import Visualizer
from NeuralNetwork import NeuralNetwork


class LogisticMapAnalyzer:
    def __init__(self):
        self.logistic_map = LogisticMap()
        self.visualizer = Visualizer()
        self.neural_network = NeuralNetwork()

    def run_analysis(self):
        print("Starting logistic map analysis with extended training...")

        a_values, x_values = self.logistic_map.generate_data(
            a_min=2.8,
            a_max=4.0,
            n_a=300,
            n_iterations=200,
            n_skip=100
        )

        self.visualizer.plot_bifurcation_diagram(a_values, x_values)

        sequence_length = 10
        X_train, y_train = self.neural_network.prepare_training_data(a_values, x_values, sequence_length)

        model, history = self.neural_network.build_and_train_model(X_train, y_train)

        self.visualizer.plot_training_history(history)

        a_predictions, predicted_values = self.neural_network.generate_predictions(
            model, a_values, self.logistic_map, sequence_length
        )

        self.visualizer.plot_point_predictions(a_values, x_values, a_predictions, predicted_values)

        print("Analysis complete!")
