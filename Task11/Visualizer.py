from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class Visualizer:
    def __init__(self, pendulum):
        self.pendulum = pendulum

    def create_animation(self, t, positions, save_file=None):
        x1, y1, x2, y2 = positions.T

        # canvas pro animaci
        fig, ax = plt.subplots(figsize=(10, 10))
        limit = (self.pendulum.l1 + self.pendulum.l2) * 1.2
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_aspect('equal')
        ax.grid()
        ax.set_title('Double Pendulum')


        line, = ax.plot([], [], 'k-', lw=2)  # čára pro tyče kyvadla
        c1 = plt.Circle((0, 0), 0.05 * self.pendulum.m1, fc='r', zorder=3)  # bod pro první závaží
        c2 = plt.Circle((0, 0), 0.05 * self.pendulum.m2, fc='r', zorder=3)  # bod pro druhé závaží
        ax.add_patch(c1)
        ax.add_patch(c2)

        # pohybová trajektorie druhého závaží
        trace, = ax.plot([], [], 'b-', lw=1, alpha=0.5)
        time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes)

        trace_x, trace_y = [], []

        def init():
            line.set_data([], [])
            c1.center = (0, 0) # počáteční pozice prvního závaží
            c2.center = (0, 0) # počáteční pozice druhého závaží
            trace.set_data([], [])
            time_text.set_text('')
            return line, c1, c2, trace, time_text

        # Aktualizační funkce pro každý snímek
        def animate(i):
            line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])

            # aktualizace pozice závaží
            c1.center = (x1[i], y1[i])
            c2.center = (x2[i], y2[i])

            # aktualizace trajektorie
            trace_x.append(x2[i])
            trace_y.append(y2[i])
            trace.set_data(trace_x, trace_y)

            time_text.set_text(f'Time: {t[i]:.2f} s')
            return line, c1, c2, trace, time_text

        ani = FuncAnimation(fig, animate, frames=len(t),
                            interval=1000 * (t[1] - t[0]), blit=True,
                            init_func=init, repeat=False)

        # uložení
        if save_file:
            ani.save(save_file, writer='pillow', fps=30)

        return ani

    def plot_angles(self, t, positions):
        # Vykreslení úhlů v čase
        x1, y1, x2, y2 = positions.T

        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(t, x1)
        plt.grid(True)
        plt.ylabel('Theta 1')
        plt.title('Angular Positions')

        plt.subplot(2, 1, 2)
        plt.plot(t, x2)
        plt.grid(True)
        plt.xlabel('Time')
        plt.ylabel('Theta 2')

        plt.tight_layout()
        plt.savefig('angles.png')

    def plot_trajectory(self, positions):
        # Vykreslení trajektorie druhého závaží
        x1, y1, x2, y2 = positions.T

        plt.figure(figsize=(8, 8))
        plt.plot(x2, y2)
        plt.grid(True)
        plt.xlabel('x2')
        plt.ylabel('y2')
        plt.title('Second Pendulum Trajectory')
        plt.axis('equal')
        plt.savefig('trajectory.png')
