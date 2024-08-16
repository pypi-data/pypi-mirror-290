import matplotlib.pyplot as plt
import numpy as np

def plot_contrast(color1, color2):
    """
    Plotea el contraste entre dos colores en formato RGBA.

    Args:
    color1: Array de forma [R, G, B, A] para el primer color.
    color2: Array de forma [R, G, B, A] para el segundo color.
    """

    # Crear una matriz que contenga los dos colores RGBA
    colors = np.array([color1, color2], dtype=float)

    # Normalizar los valores RGBA si es necesario (en caso de que no estén entre 0 y 1)
    colors_normalized = colors[:, :3] / 255.0
    alpha_values = colors[:, 3]

    # Crear una figura para ploteo
    fig, ax = plt.subplots(1, 2, figsize=(6, 3))

    # Plotear los dos colores
    for i in range(2):
        ax[i].imshow([[colors_normalized[i]]], alpha=alpha_values[i])
        ax[i].axis('off')

    # Mostrar la figura
    plt.show()


