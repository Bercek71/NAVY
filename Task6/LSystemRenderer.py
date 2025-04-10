import math

class LSystemRenderer:

    def __init__(self, canvas):

        self.canvas = canvas

    def draw(self, l_system, iterations, start_x, start_y, start_angle_deg, line_size):

        l_system_str = l_system.generate(iterations)
        # konverze úhlu na radiány
        start_angle_rad = math.radians(start_angle_deg)
        x, y = start_x, start_y
        angle = start_angle_rad
        stack = []

        self.canvas.create_text(10, 10, text=f"L-System: {l_system.axiom} with {iterations} iterations", anchor="nw")

        for char in l_system_str:
            if char == 'F' or char == 'X':  # dopředu
                new_x = x + line_size * math.cos(angle)
                new_y = y + line_size * math.sin(angle)
                self.canvas.create_line(x, y, new_x, new_y, fill="black")
                x, y = new_x, new_y
            elif char == 'b':  # dopředu
                x += line_size * math.cos(angle)
                y += line_size * math.sin(angle)
            elif char == '+':  # doprava
                angle += l_system.angle_rad
            elif char == '-':  # doleva
                angle -= l_system.angle_rad
            elif char == '[':  # uložení pozice
                stack.append((x, y, angle))
            elif char == ']':  # obnovení pozice
                if stack:
                    x, y, angle = stack.pop()

        return len(l_system_str)