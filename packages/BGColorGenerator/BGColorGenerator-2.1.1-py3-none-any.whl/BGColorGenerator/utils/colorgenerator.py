from .visualization import plot_contrast  
import tensorflow as tf  
import os  

# Define la ruta donde se encuentra el modelo preentrenado 'best_model.keras'
model_path = os.path.join(os.path.dirname(__file__), 'best_model.keras')

# Carga el modelo de Keras desde la ruta especificada
best_model = tf.keras.models.load_model(model_path)

def get_bg_color(rgba_array, turn_off_visualization=False):
    """
    Predice el color de fondo basado en un array RGBA utilizando un modelo preentrenado.
    
    Parámetros:
    - rgba_array: array de 4 elementos que representan los valores de Rojo (R), Verde (G), Azul (B) y Alfa (A) del color.
    - turn_off_visualization: booleano opcional (False por defecto). Si se establece en True, se desactiva la visualización del contraste.

    Retorna:
    - Un array de 4 elementos (RGBA) que representa el color de fondo predicho.
    """
    
    # Convertir el array RGBA en un tensor de TensorFlow para que pueda ser procesado por el modelo
    rgba_tensor = tf.constant([rgba_array], dtype=tf.float32)
    
    # Utiliza el modelo cargado para predecir el color de fondo basado en el array RGBA proporcionado
    y_pred = best_model.predict(rgba_tensor)
    
    # Si la visualización no está desactivada, muestra el contraste entre el color original y el predicho
    if not turn_off_visualization:
        plot_contrast(rgba_array, y_pred[0])
    
    # Retorna el color de fondo predicho (el primer y único elemento de y_pred)
    return y_pred[0]


