import gym
import numpy as np
import tensorflow as tf
from tensorflow import keras
import tkinter as tk
import math
import matplotlib.pyplot as plt

try:
    # For training, disable human rendering to speed up
    env = gym.make('CartPole-v1', render_mode=None)
except:
    env = gym.make('CartPole-v1')

# Increase learning rate for faster convergence
LEARNING_RATE = 0.2  # Increased from 0.1
DISCOUNT = 0.95
# Reduce number of episodes
EPISODES = 100000  # Reduced from 2000
AGGREGATE_STATS_EVERY = 25  # More frequent feedback

# Faster exploration decay
epsilon = 1.0
EPSILON_DECAY = 0.99  # More aggressive decay
MIN_EPSILON = 0.01

# Reduce state space discretization for faster learning
STATE_SPACE_DISCRETIZATION = 8  # Reduced from 10
discrete_os_size = [STATE_SPACE_DISCRETIZATION] * 4
discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / discrete_os_size

# Initialize q-table with optimistic values to encourage exploration
q_table = np.random.uniform(low=0, high=1, size=discrete_os_size + [env.action_space.n])

ep_rewards = []
aggr_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': []}

# Add early stopping threshold
SOLVED_THRESHOLD = 195  # Consider environment solved when average reward over 100 episodes exceeds this


def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low) / discrete_os_win_size
    discrete_state = np.clip(discrete_state, 0, [STATE_SPACE_DISCRETIZATION - 1] * 4)
    return tuple(discrete_state.astype(int))


print("Starting optimized Q-learning training...")
for episode in range(EPISODES):
    state = env.reset()

    if isinstance(state, tuple):
        state = state[0]

    discrete_state = get_discrete_state(state)
    done = False
    episode_reward = 0

    # Fast training without rendering
    while not done:
        if np.random.random() > epsilon:
            action = np.argmax(q_table[discrete_state])
        else:
            action = np.random.randint(0, env.action_space.n)

        try:
            next_state, reward, done, info = env.step(action)
        except:
            try:
                next_state, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated
            except:
                step_result = env.step(action)
                next_state = step_result[0]
                reward = step_result[1]
                done = step_result[2]

        episode_reward += reward
        next_discrete_state = get_discrete_state(next_state)

        if not done:
            max_future_q = np.max(q_table[next_discrete_state])
            current_q = q_table[discrete_state + (action,)]
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[discrete_state + (action,)] = new_q

        discrete_state = next_discrete_state

    ep_rewards.append(episode_reward)

    if epsilon > MIN_EPSILON:
        epsilon *= EPSILON_DECAY
        epsilon = max(MIN_EPSILON, epsilon)

    if not episode % AGGREGATE_STATS_EVERY or episode == 1:
        average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:]) / len(ep_rewards[-AGGREGATE_STATS_EVERY:])
        min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
        max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
        aggr_ep_rewards['ep'].append(episode)
        aggr_ep_rewards['avg'].append(average_reward)
        aggr_ep_rewards['min'].append(min_reward)
        aggr_ep_rewards['max'].append(max_reward)
        print(f"Episode: {episode}, avg: {average_reward:.2f}, min: {min_reward}, max: {max_reward}")

    # Early stopping with more aggressive threshold
    if len(ep_rewards) >= 50 and np.mean(ep_rewards[-50:]) >= SOLVED_THRESHOLD:
        print(f"Environment solved in {episode} episodes!")
        break

print("Q-learning training completed!")

# Plot training progress
plt.figure(figsize=(10, 6))
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label='Average Rewards')
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label='Min Rewards')
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label='Max Rewards')
plt.legend()
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('Training Progress')
plt.savefig('training_progress.png')
plt.close()

print("Generating training data from Q-learning...")
# Generate fewer samples for faster neural network training
X = []
y = []

for _ in range(10000):  # Reduced from 20000
    state = env.observation_space.sample()
    discrete_state = get_discrete_state(state)
    q_values = q_table[discrete_state]
    X.append(state)
    y.append(q_values)

X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.float32)


def create_model():
    # Slightly more efficient model with better initialization
    model = keras.Sequential([
        keras.layers.Dense(32, input_shape=(env.observation_space.shape[0],), activation='relu',
                           kernel_initializer='he_uniform'),
        keras.layers.Dense(16, activation='relu', kernel_initializer='he_uniform'),
        keras.layers.Dense(env.action_space.n, activation='linear')
    ])
    # Increase learning rate for faster training
    model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=0.002), metrics=['accuracy'])
    return model


print("Training neural network...")
model = create_model()
# Reduce epochs, increase batch size for faster training
model.fit(X, y, batch_size=128, epochs=3, validation_split=0.1, verbose=1)
print("Neural network training completed!")

# Save model for future use without retraining
model.save('cartpole_model.h5')
print("Model saved to cartpole_model.h5")


class CartPoleVisualizer:
    def __init__(self, model):
        self.model = model
        self.root = tk.Tk()
        self.root.title("Cart-Pole Balancing with Neural Network")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack(pady=20)

        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(fill=tk.X, padx=20)

        self.reward_var = tk.StringVar(value="Total Reward: 0")
        self.action_var = tk.StringVar(value="Action: None")
        self.episode_count = 0
        self.episode_var = tk.StringVar(value="Episode: 0")

        tk.Label(self.info_frame, textvariable=self.reward_var, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Label(self.info_frame, textvariable=self.action_var, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Label(self.info_frame, textvariable=self.episode_var, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(self.button_frame, text="Start New Episode", command=self.start_episode,
                  font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(self.button_frame, text="Auto Run (5 Episodes)", command=self.auto_run,
                  font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(self.button_frame, text="Stop", command=self.stop, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(self.button_frame, text="Exit", command=self.root.destroy, font=("Arial", 12)).pack(side=tk.RIGHT,
                                                                                                      padx=10)

        self.speed_frame = tk.Frame(self.root)
        self.speed_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(self.speed_frame, text="Simulation Speed:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.IntVar(value=50)

        tk.Radiobutton(self.speed_frame, text="Fast", variable=self.speed_var, value=10,
                       font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(self.speed_frame, text="Medium", variable=self.speed_var, value=50,
                       font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(self.speed_frame, text="Slow", variable=self.speed_var, value=100,
                       font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        self.ground_y = 300
        self.canvas.create_line(50, self.ground_y, 750, self.ground_y, width=2)

        self.cart_width = 50
        self.cart_height = 30
        self.pole_length = 150

        self.running = False
        self.auto_running = False
        self.total_reward = 0
        self.episodes_to_run = 0

    def start_episode(self):
        if self.running:
            return

        self.running = True
        self.total_reward = 0
        self.episode_count += 1
        self.episode_var.set(f"Episode: {self.episode_count}")
        self.reward_var.set(f"Total Reward: {self.total_reward}")

        state = env.reset()
        if isinstance(state, tuple):
            state = state[0]

        self.run_simulation(state)

    def auto_run(self):
        if self.running or self.auto_running:
            return

        self.auto_running = True
        self.episodes_to_run = 5
        self.start_episode()

    def stop(self):
        self.running = False
        self.auto_running = False
        self.episodes_to_run = 0

    def run_simulation(self, state):
        if not self.running:
            return

        self.canvas.delete("cart", "pole")

        q_values = self.model.predict(np.array([state], dtype=np.float32), verbose=0)[0]
        action = np.argmax(q_values)
        self.action_var.set(f"Action: {'Right' if action == 1 else 'Left'}")

        try:
            next_state, reward, done, info = env.step(action)
        except:
            try:
                next_state, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated
            except:
                step_result = env.step(action)
                next_state = step_result[0]
                reward = step_result[1]
                done = step_result[2]

        self.total_reward += reward
        self.reward_var.set(f"Total Reward: {self.total_reward:.1f}")

        cart_x = 400 + state[0] * 50
        cart_y = self.ground_y

        # Draw cart
        self.canvas.create_rectangle(
            cart_x - self.cart_width / 2,
            cart_y - self.cart_height / 2,
            cart_x + self.cart_width / 2,
            cart_y + self.cart_height / 2,
            fill="black",
            tags="cart"
        )

        pole_angle = state[2]
        pole_end_x = cart_x + self.pole_length * math.sin(pole_angle)
        pole_end_y = cart_y - self.pole_length * math.cos(pole_angle)

        self.canvas.create_line(
            cart_x,
            cart_y - self.cart_height / 2,
            pole_end_x,
            pole_end_y,
            width=6,
            fill="red",
            tags="pole"
        )

        if done:
            self.canvas.create_text(
                400, 150,
                text=f"Episode ended with reward: {self.total_reward:.1f}",
                font=("Arial", 20),
                fill="red",
                tags="pole"
            )
            self.running = False

            # If in auto run mode, start next episode
            if self.auto_running and self.episodes_to_run > 1:
                self.episodes_to_run -= 1
                self.root.after(1000, self.start_episode)
            elif self.auto_running:
                self.auto_running = False

            return

        delay = self.speed_var.get()  # Use the selected speed
        self.root.after(delay, lambda: self.run_simulation(next_state))

    def start(self):
        self.root.mainloop()


print("Starting visualization...")
# Create a separate environment for visualization
try:
    viz_env = gym.make('CartPole-v1', render_mode="human")
except:
    viz_env = gym.make('CartPole-v1')

# Replace the global env with the visualization environment
env = viz_env
visualizer = CartPoleVisualizer(model)
visualizer.start()