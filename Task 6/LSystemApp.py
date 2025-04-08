import tkinter as tk
from tkinter import ttk, messagebox
from LSystem import LSystem, PREDEFINED_SYSTEMS
from LSystemRenderer import LSystemRenderer

class LSystemApp:

    def __init__(self, root):

        self.root = root
        self.root.title("L-System Fractal Generator")
        self.root.geometry("1200x800")

        self.setup_variables()
        self.create_layout()
        self.create_widgets()

    def setup_variables(self):
        # nastavení proměnných pro parametry
        self.start_x = tk.StringVar(value="600")
        self.start_y = tk.StringVar(value="400")
        self.start_angle = tk.StringVar(value="0")
        self.nesting = tk.StringVar(value="2")
        self.line_size = tk.StringVar(value="5")
        self.custom_axiom = tk.StringVar(value="F+F+F+F")
        self.custom_rule = tk.StringVar(value="F -> F+F-F-FF+F+F-F")
        self.custom_angle = tk.StringVar(value="90")
        self.status_var = tk.StringVar(value="Ready")

    def create_layout(self):

        self.control_frame = ttk.Frame(self.root, padding="10")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.renderer = LSystemRenderer(self.canvas)

    def create_widgets(self):
        notebook = ttk.Notebook(self.control_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        preset_tab = ttk.Frame(notebook)
        custom_tab = ttk.Frame(notebook)
        notebook.add(preset_tab, text="Preset L-Systems")
        notebook.add(custom_tab, text="Custom L-System")

        self.create_parameter_frame()

        self.create_preset_tab(preset_tab)

        self.create_custom_tab(custom_tab)

        status_bar = ttk.Label(self.control_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    def create_parameter_frame(self):
        param_frame = ttk.LabelFrame(self.control_frame, text="Common Parameters", padding=10)
        param_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(param_frame, text="Start X Position:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.start_x, width=10).grid(row=0, column=1, pady=2)

        ttk.Label(param_frame, text="Start Y Position:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.start_y, width=10).grid(row=1, column=1, pady=2)

        ttk.Label(param_frame, text="Start Angle (degrees):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.start_angle, width=10).grid(row=2, column=1, pady=2)

        ttk.Label(param_frame, text="Nesting Level:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.nesting, width=10).grid(row=3, column=1, pady=2)

        ttk.Label(param_frame, text="Line Size:").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.line_size, width=10).grid(row=4, column=1, pady=2)

        ttk.Button(param_frame, text="Clear Canvas", command=self.clear_canvas).grid(row=5, column=0, columnspan=2,
                                                                                     pady=10)

    def create_preset_tab(self, parent):
        for i, system in enumerate(PREDEFINED_SYSTEMS):
            btn = ttk.Button(parent, text=f"Draw {system['name']}",
                             command=lambda s=system: self.draw_preset_system(s))
            btn.pack(fill=tk.X, pady=5)

            info_text = f"Axiom: {system['axiom']}\nRule: {system['rule']}\nAngle: {system['angle']}°"
            ttk.Label(parent, text=info_text, justify=tk.LEFT).pack(fill=tk.X, pady=2)
            ttk.Separator(parent, orient='horizontal').pack(fill=tk.X, pady=5)

    def create_custom_tab(self, parent):
        ttk.Label(parent, text="Axiom:").pack(anchor=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.custom_axiom, width=40).pack(fill=tk.X, pady=2)

        ttk.Label(parent, text="Rule (format: X -> Y or X -> Y, Z -> W):").pack(anchor=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.custom_rule, width=40).pack(fill=tk.X, pady=2)

        ttk.Label(parent, text="Angle (degrees):").pack(anchor=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.custom_angle, width=40).pack(fill=tk.X, pady=2)

        ttk.Button(parent, text="Draw Custom System", command=self.draw_custom_system).pack(fill=tk.X, pady=10)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.status_var.set("Canvas cleared")

    def get_common_parameters(self):
        try:
            start_x = int(self.start_x.get())
            start_y = int(self.start_y.get())
            start_angle = float(self.start_angle.get())
            iterations = int(self.nesting.get())
            line_size = float(self.line_size.get())
            return start_x, start_y, start_angle, iterations, line_size
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid parameter value: {str(e)}")
            raise

    def draw_preset_system(self, system):
        """
        Draw a preset L-system.

        Args:
            system (dict): Dictionary with axiom, rule, and angle for the L-system
        """
        try:
            # Get parameters
            start_x, start_y, start_angle, iterations, line_size = self.get_common_parameters()

            # Create the L-system
            l_system = LSystem.from_rule_string(system["axiom"], system["rule"], system["angle"])

            # Clear and draw
            self.clear_canvas()
            elements = self.renderer.draw(l_system, iterations, start_x, start_y, start_angle, line_size)

            self.status_var.set(f"Drew L-system with {elements} elements")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error drawing L-system")

    def draw_custom_system(self):
        try:
            # nastavení parametrů
            start_x, start_y, start_angle, iterations, line_size = self.get_common_parameters()

            axiom = self.custom_axiom.get()
            rule_str = self.custom_rule.get()
            angle = float(self.custom_angle.get())

            if not axiom or not rule_str:
                messagebox.showwarning("Warning", "Please provide both axiom and rules")
                return

            # vytvoření L-systému
            try:
                l_system = LSystem.from_rule_string(axiom, rule_str, angle)

                # kontrola pravidel
                if not l_system.rules:
                    messagebox.showwarning("Warning", "Invalid rule format. Use 'X -> Y' format.")
                    return

                self.clear_canvas()
                elements = self.renderer.draw(l_system, iterations, start_x, start_y, start_angle, line_size)

                self.status_var.set(f"Drew custom L-system with {elements} elements")

            except ValueError as e:
                messagebox.showerror("Error", f"Invalid L-system parameter: {str(e)}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error drawing L-system")


def main():
    root = tk.Tk()
    app = LSystemApp(root)
    root.mainloop()

