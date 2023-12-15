import matplotlib.pyplot as plt
import statsmodels.api as sm
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont


def convert_text_to_image(text):
    # Configuración de la imagen
    image = Image.new('RGB', (800, 600), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    font_size = 18
    font = ImageFont.load_default()

    # Agregar el texto al lienzo de la imagen
    draw.text((10, 10), text, fill=(0, 0, 0), font=font)

    # Guardar la imagen temporalmente
    image_path = 'summary_image.png'
    image.save(image_path)
    return image_path



def interpret_r_squared(r_squared):
    """
    Interpreta el valor de R-cuadrado y devuelve el color y la interpretación correspondientes.

    Parameters:
    - r_squared (float): Valor de R-cuadrado.

    Returns:
    - Tuple: (str) Color para visualización, (str) Interpretación del R-cuadrado.
    """
    if 0.8 <= r_squared <= 1:
        color = 'green'
        interpretation = 'Ajuste óptimo, el model explica a la perfección la relación de las variables'
    elif 0.6 <= r_squared < 0.8:
        color = 'yellow'
        interpretation = 'Buen Ajuste'
    elif 0.4 <= r_squared < 0.6:
        color = 'yellow'
        interpretation = 'Ajuste Aceptable'
    elif 0.2 <= r_squared < 0.4:
        color = 'red'
        interpretation = 'Ajuste Débil'
    else:
        color = 'red'
        interpretation = 'Ajuste Pésimo, el model no es explicativo'

    return color, interpretation


def show_regression_graph(model, X, y, window):
    """
    Muestra la gráfica de la regresión lineal.

    Parameters:
    - model: Modelo de regresión lineal ajustado.
    - X: Variables predictoras.
    - y: Variable a predecir.
    - window: Ventana de la interfaz gráfica donde se mostrará la gráfica.

    La función utiliza el modelo de regresión para predecir los valores y_prediction. Si hay más de una variable predictora,
    muestra una gráfica de dispersión entre los valores observados y predichos. Si solo hay una variable predictora,
    muestra la gráfica de dispersión junto con la regresión lineal.

    Returns:
    - None
    """
    # Predice los valores
    X_with_const = sm.add_constant(X)
    y_prediction = model.predict(X_with_const)

    # Crear la figura para la gráfica
    figure, ax = plt.subplots()
    
    # Verifica si hay más de una variable predictora
    if X.shape[1] > 1:
        # Si hay más de una variable predictora, no se puede graficar en 2D,
        # así que muestra solo la predicción vs. observado
        ax.scatter(y, y_prediction, label='Observado vs. Predicho')
        ax.set_xlabel('Observado')
        ax.set_ylabel('Predicho')
    else:
        # Si solo hay una variable predictora, muestra la gráfica de dispersión,
        # y la regresión lineal
        ax.scatter(X.iloc[:, 0], y, label='Datos')
        ax.plot(X.iloc[:, 0], y_prediction, color='red', label='Regresión Lineal')
        ax.set_xlabel('Variable Predictora')
        ax.set_ylabel('Variable a Predecir')

    ax.legend()

    # Ajustar el tamaño de la figura
    figure.set_size_inches(6, 4)  # Ajusta el tamaño de la figura

    # Guardar la gráfica en un archivo temporal
    temporary_plot = 'temporary_plot.png'
    plt.savefig(temporary_plot)
    plt.close()

    # Mostrar la gráfica en la interfaz
    with open(temporary_plot, "rb") as file:
        image_bytes = file.read()
    
    # Actualizar el elemento de imagen en la ventana con los nuevos bytes de la imagen
    window['-IMAGE2-'].update(data=image_bytes)


## ESTA FUNCION FIXENA COPIANDO UN CACHO DO CODIGO DE NATHAN
## ALCULA COUSAS E MOSTRA COUSAS POR PANTALLA UNHA VEZ ESTA FEITO 
## O modelo, FACIAME FALTA PA CANDO SE CARGASE O modelo, ENTONCES CONVERTINO NUNHA FUNCION
def regression_elements(model, window):
    r_squared = model.rsquared
    color, interpretation = interpret_r_squared(r_squared)

    results = model.summary()
    results_str = str(results)
    #window['-OUTPUT-'].update(value=results_str)
    image_path = convert_text_to_image(results_str)
    image = Image.open(image_path)
    image = image.resize((700, 400))  # Ajusta el tamaño de la imagen
    image.save(image_path)

    # Actualizar el elemento de imagen en la interfaz con la nueva imagen generada
    window['-IMAGE1-'].update(filename=image_path)
    
    layout_results = [
        [sg.Text(f'R-cuadrado: {r_squared:.4f}', font=('Helvetica', 12), text_color=color)],
        [sg.Text(f'Interpretación: {interpretation}', font=('Helvetica', 12))]
    ]
    window_results = sg.Window('Resultados del modelo', layout_results)
    event, values = window_results.read()
    window_results.close()



if __name__ == '__main__':
    pass