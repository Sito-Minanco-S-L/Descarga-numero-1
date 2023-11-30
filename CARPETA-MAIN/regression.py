import matplotlib.pyplot as plt
import statsmodels.api as sm
import PySimpleGUI as sg



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


def mostrar_grafica_regresion(modelo, X, y):
    """
    Muestra la gráfica de la regresión lineal.

    Parameters:
    - modelo: Modelo de regresión lineal ajustado.
    - X: Variables predictoras.
    - y: Variable a predecir.

    La función utiliza el modelo de regresión para predecir los valores y_pred. Si hay más de una variable predictora,
    muestra una gráfica de dispersión entre los valores observados y predichos. Si solo hay una variable predictora,
    muestra la gráfica de dispersión junto con la regresión lineal.

    Returns:
    - None
    """
    # Predice los valores
    X_with_const = sm.add_constant(X)
    y_pred = modelo.predict(X_with_const)
    
    # Verifica si hay más de una variable predictora
    if X.shape[1] > 1:
        # Si hay más de una variable predictora, no se puede graficar en 2D,
        # así que muestra solo la predicción vs. observado
        plt.scatter(y, y_pred, label='Observado vs. Predicho')
        plt.xlabel('Observado')
        plt.ylabel('Predicho')
    else:
        # Si solo hay una variable predictora, muestra la gráfica de dispersión,
        # y la regresión lineal
        plt.scatter(X.iloc[:, 0], y, label='Datos')
        plt.plot(X.iloc[:, 0], y_pred, color='red', label='Regresión Lineal')
        plt.xlabel('Variable Predictora')
        plt.ylabel('Variable a Predecir')

    plt.legend()
    plt.show()


def cosas_regresion(modelo):
    r_squared = modelo.rsquared
    color, interpretacion = interpretar_r_cuadrado(r_squared)

    layout_resultados = [
        [sg.Text(f'R-cuadrado: {r_squared:.4f}', font=('Helvetica', 12), text_color=color)],
        [sg.Text(f'Interpretación: {interpretacion}', font=('Helvetica', 12))]
    ]
    window_resultados = sg.Window('Resultados del Modelo', layout_resultados)
    event, values = window_resultados.read()
    window_resultados.close()



if __name__ == '__main__':
    pass