import numpy as np
import matplotlib.pyplot as plt

from DoublePendulum import DoublePendulum
from Visualizer import Visualizer


def main():
    pendulum = DoublePendulum(l1=1.0, l2=1.0, m1=1.0, m2=1.0)

    # Počáteční úhly vychýlení
    theta1_0 = 2 * np.pi / 6  # 60 stupňů
    theta2_0 = 5 * np.pi / 8  # 112.5 stupňů

    T = 20.0  # celkový čas simulace
    dt = 0.01  # časový krok

    # simulace
    t, positions = pendulum.simulate(theta1_0, theta2_0, T, dt)


    visualizer = Visualizer(pendulum)
    print("Creating animation..., please wait around 20 seconds")
    ani = visualizer.create_animation(t, positions, save_file='pendulum.gif')
    visualizer.plot_angles(t, positions)
    visualizer.plot_trajectory(positions)

    plt.show()


if __name__ == "__main__":
    main()