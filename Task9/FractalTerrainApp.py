import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from TerrainLayer import TerrainLayer


class FractalTerrainApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Fractal Terrain")
        self.root.geometry("1200x800")

        self.layers = []
        self.current_color = "#000000"

        self.setup_variables()
        self.create_layout()
        self.create_widgets()

    def setup_variables(self):
        self.start_x = tk.StringVar(value="0")
        self.start_y = tk.StringVar(value="200")
        self.end_x = tk.StringVar(value="800")
        self.end_y = tk.StringVar(value="400")
        self.iterations = tk.StringVar(value="8")
        self.roughness = tk.StringVar(value="0.5")
        self.status_var = tk.StringVar(value="Ready")

    def create_layout(self):
        """Create the application layout"""
        self.control_frame = ttk.Frame(self.root, padding="10")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def create_widgets(self):
        # Parameter frame
        param_frame = ttk.LabelFrame(self.control_frame, text="Terrain Parameters", padding=10)
        param_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(param_frame, text="Start X position:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.start_x, width=10).grid(row=0, column=1, pady=2)

        ttk.Label(param_frame, text="Start Y position:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.start_y, width=10).grid(row=1, column=1, pady=2)

        ttk.Label(param_frame, text="End X position:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.end_x, width=10).grid(row=2, column=1, pady=2)

        ttk.Label(param_frame, text="End Y position:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.end_y, width=10).grid(row=3, column=1, pady=2)

        ttk.Label(param_frame, text="Iterations:").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.iterations, width=10).grid(row=4, column=1, pady=2)

        ttk.Label(param_frame, text="Roughness (0-1):").grid(row=5, column=0, sticky=tk.W, pady=2)
        ttk.Entry(param_frame, textvariable=self.roughness, width=10).grid(row=5, column=1, pady=2)

        color_frame = ttk.LabelFrame(self.control_frame, text="Terrain Color", padding=10)
        color_frame.pack(fill=tk.X, padx=5, pady=5)

        self.color_preview = tk.Canvas(color_frame, width=20, height=20, bg=self.current_color)
        self.color_preview.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(color_frame, text="Pick Color", command=self.pick_color).grid(row=0, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self.control_frame, padding=10)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Add Terrain Layer", command=self.add_terrain_layer).pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="Clear Canvas", command=self.clear_canvas).pack(fill=tk.X, pady=5)

        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def pick_color(self):
        color = colorchooser.askcolor(initialcolor=self.current_color)
        if color[1]:
            self.current_color = color[1]
            self.color_preview.config(bg=self.current_color)

    def add_terrain_layer(self):
        try:
            start_x = float(self.start_x.get())
            start_y = float(self.start_y.get())
            end_x = float(self.end_x.get())
            end_y = float(self.end_y.get())
            iterations = int(self.iterations.get())
            roughness = float(self.roughness.get())

            layer = TerrainLayer(start_x, start_y, end_x, end_y, roughness, iterations, self.current_color)
            self.layers.append(layer)

            layer.generate()

            self.draw_layer(layer)

            self.status_var.set(f"Added terrain layer with color {self.current_color}")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid parameter value: {str(e)}")

    def draw_layer(self, layer):
        x_values, y_values = layer.get_points_as_arrays()

        points = []
        for i in range(len(x_values)):
            points.append(x_values[i])
            points.append(y_values[i])

        points.append(x_values[-1])
        points.append(self.canvas.winfo_height())
        points.append(x_values[0])
        points.append(self.canvas.winfo_height())

        polygon_id = self.canvas.create_polygon(points, fill=layer.color, outline=layer.color)
        layer.canvas_elements.append(polygon_id)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.layers = []
        self.status_var.set("Canvas cleared")
