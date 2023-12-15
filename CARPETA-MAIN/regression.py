import matplotlib.pyplot as plt
import statsmodels.api as sm
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont


def convert_text_to_image(text):
    # Configuración de la imagen
    img = Image.new('RGB', (800, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    font_size = 18
    font = ImageFont.load_default()

    # Agregar el texto al lienzo de la imagen
    d.text((10, 10), text, fill=(0, 0, 0), font=font)

    # Guardar la imagen temporalmente
    img_path = 'summary_image.png'
    img.save(img_path)
    return img_path



def interpretar_r_cuadrado(r_cuadrado):
    """
    Interpreta el valor de R-cuadrado y devuelve el color y la interpretación correspondientes.

    Parameters:
    - r_cuadrado (float): Valor de R-cuadrado.

    Returns:
    - Tuple: (str) Color para visualización, (str) Interpretación del R-cuadrado.
    """
    if 0.8 <= r_cuadrado <= 1:
        color = 'green'
        interpretacion = 'Ajuste óptimo, el modelo explica a la perfección la relación de las variables'
    elif 0.6 <= r_cuadrado < 0.8:
        color = 'yellow'
        interpretacion = 'Buen Ajuste'
    elif 0.4 <= r_cuadrado < 0.6:
        color = 'yellow'
        interpretacion = 'Ajuste Aceptable'
    elif 0.2 <= r_cuadrado < 0.4:
        color = 'red'
        interpretacion = 'Ajuste Débil'
    else:
        color = 'red'
        interpretacion = 'Ajuste Pésimo, el modelo no es explicativo'

    return color, interpretacion


def mostrar_grafica_regresion(modelo, X, y, window):
    """
    Muestra la gráfica de la regresión lineal.

    Parameters:
    - modelo: Modelo de regresión lineal ajustado.
    - X: Variables predictoras.
    - y: Variable a predecir.
    - window: Ventana de la interfaz gráfica donde se mostrará la gráfica.

    La función utiliza el modelo de regresión para predecir los valores y_pred. Si hay más de una variable predictora,
    muestra una gráfica de dispersión entre los valores observados y predichos. Si solo hay una variable predictora,
    muestra la gráfica de dispersión junto con la regresión lineal.

    Returns:
    - None
    """
    # Predice los valores
    X_with_const = sm.add_constant(X)
    y_pred = modelo.predict(X_with_const)

    # Crear la figura para la gráfica
    fig, ax = plt.subplots()
    
    # Verifica si hay más de una variable predictora
    if X.shape[1] > 1:
        # Si hay más de una variable predictora, no se puede graficar en 2D,
        # así que muestra solo la predicción vs. observado
        ax.scatter(y, y_pred, label='Observado vs. Predicho')
        ax.set_xlabel('Observado')
        ax.set_ylabel('Predicho')
    else:
        # Si solo hay una variable predictora, muestra la gráfica de dispersión,
        # y la regresión lineal
        ax.scatter(X.iloc[:, 0], y, label='Datos')
        ax.plot(X.iloc[:, 0], y_pred, color='red', label='Regresión Lineal')
        ax.set_xlabel('Variable Predictora')
        ax.set_ylabel('Variable a Predecir')

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


## ESTA FUNCION FIXENA COPIANDO UN CACHO DO CODIGO DE NATHAN
## ALCULA COUSAS E MOSTRA COUSAS POR PANTALLA UNHA VEZ ESTA FEITO 
## O MODELO, FACIAME FALTA PA CANDO SE CARGASE O MODELO, ENTONCES CONVERTINO NUNHA FUNCION
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
    window['-IMAGE1-'].update(filename=img_path)
    
    layout_resultados = [
        [sg.Text(f'R-cuadrado: {r_squared:.4f}', font=('Helvetica', 12), text_color=color)],
        [sg.Text(f'Interpretación: {interpretacion}', font=('Helvetica', 12))]
    ]
    window_resultados = sg.Window('Resultados del Modelo', layout_resultados)
    event, values = window_resultados.read()
    window_resultados.close()



if __name__ == '__main__':
    pass