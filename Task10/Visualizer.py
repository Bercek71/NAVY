from matplotlib import pyplot as plt


class Visualizer:
    def __init__(self):
        pass

    def plot_bifurcation_diagram(self, a_values, x_values):
        plt.figure(figsize=(10, 6))

        for i, a in enumerate(a_values):
            plt.plot([a] * len(x_values[i]), x_values[i], 'k.', markersize=0.2)

        plt.xlabel('Parameter (a)')
        plt.ylabel('Population (x)')
        plt.title('Bifurcation Diagram')
        plt.xlim(a_values[0], a_values[-1])
        plt.ylim(0, 1)

        plt.savefig('bifurcation_diagram.png', dpi=300)
        plt.close()

    def plot_training_history(self, history):
        plt.figure(figsize=(10, 5))
        plt.plot(history.history['loss'])
        plt.title('Model Loss During Training')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.yscale('log')
        plt.grid(True)
        plt.savefig('training_history.png', dpi=300)
        plt.close()

    def plot_point_predictions(self, a_values, x_values, a_predictions, predicted_values):
        plt.figure(figsize=(12, 8))

        for i, a in enumerate(a_values):
            plt.plot([a] * len(x_values[i]), x_values[i], 'k.', markersize=0.1)

        for i, a in enumerate(a_predictions):
            plt.plot([a] * len(predicted_values[i]), predicted_values[i], 'r.', markersize=2.0)

        plt.xlabel('Parameter (a)')
        plt.ylabel('Population')
        plt.title('Bifurcation Diagram with Predictions')

        plt.plot([], [], 'k.', label='Actual')
        plt.plot([], [], 'r.', label='Predicted')
        plt.legend()

        plt.xlim(a_values[0], a_values[-1])
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.savefig('point_predictions.png', dpi=300)
        plt.close()
