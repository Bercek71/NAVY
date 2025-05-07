import numpy as np
from scipy.integrate import odeint


class DoublePendulum:
    def __init__(self, l1=1.0, l2=1.0, m1=1.0, m2=1.0, g=9.81):
        self.l1 = l1  # délka prvního kyvadla
        self.l2 = l2  # délka druhého kyvadla
        self.m1 = m1  # hmotnost prvního závaží
        self.m2 = m2  # hmotnost druhého závaží
        self.g = g  # gravitační zrychlení

    def derivatives(self, state, t):
        theta1, omega1, theta2, omega2 = state

        delta = theta1 - theta2
        sin_delta = np.sin(delta)
        cos_delta = np.cos(delta)

        denominator = self.l1 * (self.m1 + self.m2 * np.sin(delta) ** 2)

        # úhlové zrychlení prvního kyvadla
        alpha1 = (self.m2 * self.g * np.sin(theta2) * cos_delta -
                  self.m2 * sin_delta * (self.l1 * omega1 ** 2 * cos_delta + self.l2 * omega2 ** 2) -
                  (self.m1 + self.m2) * self.g * np.sin(theta1)) / denominator

        # úhlové zrychlení druhého kyvadla
        # složitější kvůli vazbě na první kyvadlo
        alpha2 = ((self.m1 + self.m2) * (self.l1 * omega1 ** 2 * sin_delta - self.g * np.sin(theta2) +
                                         self.g * np.sin(theta1) * cos_delta) +
                  self.m2 * self.l2 * omega2 ** 2 * sin_delta * cos_delta) / (self.l2 * denominator)

        # Vracíme rychlosti a zrychlení
        return [omega1, alpha1, omega2, alpha2]

    def calculate_positions(self, theta1, theta2):
        # Výpočet kartézských souřadnic z úhlů
        # První kyvadlo
        x1 = self.l1 * np.sin(theta1)
        y1 = -self.l1 * np.cos(theta1)

        # Druhé kyvadlo - pozor na připočtení pozice prvního
        x2 = x1 + self.l2 * np.sin(theta2)
        y2 = y1 - self.l2 * np.cos(theta2)

        return x1, y1, x2, y2

    def simulate(self, theta1_0, theta2_0, T, dt):
        # počáteční podmínky - úhly a nulové úhlové rychlosti
        state_0 = [theta1_0, 0, theta2_0, 0]
        t = np.arange(0, T, dt)

        states = odeint(self.derivatives, state_0, t)

        # úhly
        theta1 = states[:, 0]
        theta2 = states[:, 2]

        # Převod na kartézské souřadnice pro vizualizaci
        positions = np.array([self.calculate_positions(theta1[i], theta2[i]) for i in range(len(t))])

        return t, positions
