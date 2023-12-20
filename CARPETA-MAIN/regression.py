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



def interpretar_r_cuadrado(r_squared):
    """
    Interpreta el valor de R-cuadrado y devuelve el color y la interpretación correspondientes.

    Parameters:
    - r_squared (float): Valor de R-cuadrado.

    Returns:
    - Tuple: (str) Color para visualización, (str) Interpretación del R-cuadrado.
    """
    if 0.8 <= r_squared <= 1:
        color = 'green'
        interpretation = 'Ajuste óptimo, el modelo explica a la perfección la relación de las variables'
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
        interpretation = 'Ajuste Pésimo, el modelo no es explicativo'

    return color, interpretation


def mostrar_grafica_regresion(modelo, X, y, window):
    """
    Muestra la gráfica de la regresión lineal.

    Parameters:
    - modelo: Modelo de regresión lineal ajustado.
    - X: Variables predictoras.
    - y: Variable a predecir.
    - window: Ventana de la interfaz gráfica donde se mostrará la gráfica.

    La función utiliza el modelo de regresión para predecir los valores y_pred. Si hay más de una variable predictora,
    muestra una gráfica 3D de dispersión entre los valores observados y predichos. Si solo hay una variable predictora,
    muestra la gráfica de dispersión junto con la regresión lineal.

    Returns:
    - None
    """
    # Predice los valores
    X_with_const = sm.add_constant(X)
    y_pred = modelo.predict(X_with_const)

    # Crear la figura para la gráfica
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Verifica si hay más de una variable predictora
    if X.shape[1] > 1:
        # Si hay más de una variable predictora, muestra la gráfica 3D de dispersión
        ax.scatter(X.iloc[:, 0], X.iloc[:, 1], y, label=f'Observado vs. Predicción')
        ax.set_xlabel(X.columns[0])
        ax.set_ylabel(X.columns[1])
        ax.set_zlabel(y.name)
    else:
        # Si solo hay una variable predictora, muestra la gráfica de dispersión,
        # y la regresión lineal
        ax.scatter(X.iloc[:, 0], y, label=f'{X.columns[0]} vs. {y.name}')
        ax.plot(X.iloc[:, 0], y_pred, color='red', label='Regresión Lineal')
        ax.set_xlabel(X.columns[0])
        ax.set_ylabel(y.name)

    ax.legend()

    # Ajustar el tamaño de la figura
    fig.set_size_inches(6, 4)  # Ajusta el tamaño de la figura

    # Guardar la gráfica en un archivo temporal
    temp_plot = 'temp_plot.png'
    plt.savefig(temp_plot)
    plt.close()

    # Mostrar la gráfica en la interfaz
    with open(temp_plot, "rb") as file:
        img_bytes = file.read()
    
    # Actualizar el elemento de imagen en la ventana con los nuevos bytes de la imagen
    window['-IMAGE2-'].update(data=img_bytes)



def cosas_regresion(modelo, window):
    r_squared = modelo.rsquared
    color, interpretacion = interpretar_r_cuadrado(r_squared)

    resultados = modelo.summary()
    resultados_str = str(resultados)
    #window['-OUTPUT-'].update(value=resultados_str)
    img_path = convert_text_to_image(resultados_str)
    img = Image.open(img_path)
    img = img.resize((700, 400))  # Ajusta el tamaño de la imagen
    img.save(img_path)

    # Actualizar el elemento de imagen en la interfaz con la nueva imagen generada




if __name__ == '__main__':
    pass