import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class HopfieldNetwork:
    def __init__(self, size):
        """
        Konstruktor třídy HopfieldNetwork
        :param size: Velikost vzorů
        """
        self.size = size
        self.weights = np.zeros((size, size))

    def train(self, patterns):
        """
        :param patterns: přijímá pole vzorů
        :return:
        """
        for pattern in patterns:
            pattern = 2 * np.array(pattern) - 1
            self.weights += np.outer(pattern, pattern)
        np.fill_diagonal(self.weights, 0)

    def energy(self, pattern):
        """
        Slouží k výpočtu energie daného vzoru
        :param pattern: vzor
        :return:
        """
        pattern = 2 * np.array(pattern) - 1
        energy = -0.5 * np.sum(np.dot(self.weights, pattern) * pattern)
        return energy

    def recover_async(self, input_pattern, max_iter=100, energy_threshold=0.0, patience=10):
        """
        Asynchronní obnova vzoru
        :param input_pattern: vstpní rozbitý vzor
        :param max_iter: počet iterací
        :param energy_threshold: threshold pro energii
        :param patience: tolerance pro energii
        :return:
        """
        input_pattern = 2 * np.array(input_pattern) - 1
        prev_energy = self.energy(input_pattern)
        stable_count = 0

        for _ in range(max_iter):
            for i in range(self.size):
                sum = np.dot(self.weights[i], input_pattern)
                input_pattern[i] = 1 if sum >= 0 else -1

            # Check if the energy has changed
            curr_energy = self.energy(input_pattern)
            if np.abs(curr_energy - prev_energy) < energy_threshold:
                stable_count += 1
            else:
                stable_count = 0

            # If energy hasn't changed for 'patience' iterations, stop
            if stable_count >= patience:
                break

            prev_energy = curr_energy

        return (input_pattern + 1) // 2  # Convert back to 0/1

    def recover_sync(self, input_pattern, max_iter=100, energy_threshold=0.0, patience=10):
        """
        Synchronní obnova vzoru
        :param input_pattern:
        :param max_iter:
        :param energy_threshold:
        :param patience:
        :return:
        """
        input_pattern = 2 * np.array(input_pattern) - 1  # Convert 0/1 to -1/1
        prev_energy = self.energy(input_pattern)
        stable_count = 0

        for _ in range(max_iter):
            sum_vector = np.dot(self.weights, input_pattern)
            input_pattern = np.sign(sum_vector)

            curr_energy = self.energy(input_pattern)
            if np.abs(curr_energy - prev_energy) < energy_threshold:
                stable_count += 1
            else:
                stable_count = 0

            if stable_count >= patience:
                break

            prev_energy = curr_energy

        return (input_pattern + 1) // 2

hopfield = None
patterns = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_pattern', methods=['POST'])
def save_pattern():
    global patterns, hopfield

    pattern = request.json['pattern']
    patterns.append(pattern)

    if hopfield is None:
        hopfield = HopfieldNetwork(len(pattern))

    hopfield.train(patterns)

    return jsonify({"status": "success"})

@app.route('/recover_pattern', methods=['POST'])
def recover_pattern():
    global hopfield

    noisy_pattern = request.json['pattern']

    recovered_async = hopfield.recover_async(noisy_pattern)
    recovered_sync = hopfield.recover_sync(noisy_pattern)

    return jsonify({
        "recovered_async": recovered_async.tolist(),
        "recovered_sync": recovered_sync.tolist(),
    })

if __name__ == '__main__':
    app.run(debug=True)