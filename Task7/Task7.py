from AffineTransformation import AffineTransformation
from FractalVisualizer import FractalVisualizer, create_dash_app
from FractalModel import FractalModel

def main():
    # první model
    first_model_transforms = [
        AffineTransformation([0.00, 0.00, 0.01, 0.00, 0.26, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00]),
        AffineTransformation([0.20, -0.26, -0.01, 0.23, 0.22, -0.07, 0.07, 0.00, 0.24, 0.00, 0.80, 0.00]),
        AffineTransformation([-0.25, 0.28, 0.01, 0.26, 0.24, -0.07, 0.07, 0.00, 0.24, 0.00, 0.22, 0.00]),
        AffineTransformation([0.85, 0.04, -0.01, -0.04, 0.85, 0.09, 0.00, 0.08, 0.84, 0.00, 0.80, 0.00])
    ]

    #druhý model
    second_model_transforms = [
        AffineTransformation([0.05, 0.00, 0.00, 0.00, 0.60, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00]),
        AffineTransformation([0.45, -0.22, 0.22, 0.22, 0.45, 0.22, -0.22, 0.22, -0.45, 0.00, 1.00, 0.00]),
        AffineTransformation([-0.45, 0.22, -0.22, 0.22, 0.45, 0.22, 0.22, -0.22, 0.45, 0.00, 1.25, 0.00]),
        AffineTransformation([0.49, -0.08, 0.08, 0.08, 0.49, 0.08, 0.08, -0.08, 0.49, 0.00, 2.00, 0.00])
    ]


    first_model = FractalModel(first_model_transforms, "3D Fern - First Model")
    second_model = FractalModel(second_model_transforms, "3D Fern - Second Model")

    visualizer = FractalVisualizer()

    #vizualizace prvního
    visualizer.set_model(first_model)
    fig1 = visualizer.create_static_plot()
    visualizer.save_plot("first_model_fractal", fig1)


    #vizualizace druhého
    visualizer.set_model(second_model)
    fig2 = visualizer.create_static_plot()
    visualizer.save_plot("second_model_fractal", fig2)

    # Dash aplikace
    # Vytvoření Dash aplikace na http://127.0.0.1:8050/
    app = create_dash_app(first_model, second_model)

    app.run(debug=True)


if __name__ == "__main__":
    main()