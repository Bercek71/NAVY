import time
import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, Dropout
from keras.callbacks import ReduceLROnPlateau
from keras.optimizers import Adam


class NeuralNetwork:
    def __init__(self):
        pass

    def prepare_training_data(self, a_values, x_values, sequence_length=10):
        print("Preparing training data...")

        X_train = []
        y_train = []

        for i, a in enumerate(a_values):
            values = x_values[i]

            for j in range(0, len(values) - sequence_length - 1, 3):
                features = [a] + values[j:j + sequence_length]
                X_train.append(features)
                y_train.append(values[j + sequence_length])

        print(f"Training data: {len(X_train)} samples with {len(X_train[0])} features")

        return np.array(X_train), np.array(y_train)

    def build_and_train_model(self, X_train, y_train):
        print("Training neural network...")
        start_time = time.time()

        model = Sequential([
            Dense(512, activation='relu', input_shape=(X_train.shape[1],)),
            BatchNormalization(),
            Dropout(0.3),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dense(64, activation='relu'),
            # sigmoid protože predikujeme hodnotu mezi 0 a 1
            Dense(1, activation='sigmoid')
        ])

        optimizer = Adam(learning_rate=0.0003)
        model.compile(optimizer=optimizer, loss='mse')

        reduce_lr = ReduceLROnPlateau(
            monitor='loss',
            factor=0.5,
            patience=5,
            min_lr=0.00001,
            verbose=1
        )

        history = model.fit(
            X_train, y_train,
            epochs=100,
            batch_size=1024,
            callbacks=[reduce_lr],
            verbose=1
        )

        print(f"Training completed in {time.time() - start_time:.2f} seconds")
        return model, history

    def generate_predictions(self, model, a_values, logistic_map, sequence_length=10):
        print("Generating minimal predictions...")

        interesting_a_values = a_values[::10]
        a_predictions = []
        predictions = []

        for target_a in interesting_a_values:
            idx = np.abs(a_values - target_a).argmin()
            a = a_values[idx]
            a_predictions.append(a)

            x = 0.5
            x_sequence = []

            for _ in range(sequence_length):
                x = logistic_map.compute(x, a)
                x_sequence.append(x)

            attractor_points = []
            for _ in range(30):
                features = np.array([[a] + x_sequence])
                x_next = model.predict(features, verbose=0)[0][0]
                x_sequence = x_sequence[1:] + [x_next]

                if _ >= 10:
                    attractor_points.append(x_next)

            predictions.append(attractor_points)

        return a_predictions, predictions
