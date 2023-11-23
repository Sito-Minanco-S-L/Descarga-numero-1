import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sqlite3
import PySimpleGUI as sg
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import magic

def file_extension(file):
    """
    Obtiene la extensión de un archivo a partir de su nombre.

    Parameters:
    - file (str): Nombre del archivo.

    Returns:
    - str: Extensión del archivo.
    """
    # Divide el nombre del archivo y retorna la última parte como extensión
    L = file.split('.')
    return L[-1]


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
    y_pred = modelo.predict(sm.add_constant(X))
    # Verifica si hay más de una variable predictora
    if X.shape[1] > 1:
        # Si hay más de una variable predictora, no se puede graficar en 2D, así que muestra solo la predicción vs. observado
        plt.scatter(y, y_pred, label='Observado vs. Predicho')
        plt.xlabel('Observado')
        plt.ylabel('Predicho')
    else:
        # Si solo hay una variable predictora, muestra la gráfica de dispersión y la regresión lineal
        plt.scatter(X.iloc[:, 1], y, label='Datos')
        plt.plot(X.iloc[:, 1], y_pred, color='red', label='Regresión Lineal')
        plt.xlabel('Variable Predictora')
        plt.ylabel('Variable a Predecir')

    plt.legend()
    plt.show()


def mostrar_resultados(modelo):
    """
    Muestra los resultados de un modelo de regresión lineal, incluido el R-cuadrado.

    Parameters:
    - modelo: Modelo de regresión lineal ajustado.
    """
    # Obtiene los resultados del modelo y los muestra en una ventana gráfica
    resultados = modelo.summary()
    resultados_str = str(resultados)
    resultados_list = resultados_str.split('\n')

    # Obtener encabezados y datos
    encabezados = resultados_list[0].split()
    datos = [line.split() for line in resultados_list[2:-1]]

    # Obtener R-cuadrado
    r_cuadrado = modelo.rsquared
    
    # Interpretar R-cuadrado
    color, interpretacion = interpretar_r_cuadrado(r_cuadrado)

    layout = [
        [sg.Text('Resultados de la Regresión Lineal', font=('Helvetica', 16), justification='center')],
        [sg.Multiline(resultados_str, size=(80, 20), font=('Courier New', 10))],
        [sg.Text(f'Bondad del ajuste: {r_cuadrado:.4f}', font=('Helvetica', 14), text_color=color)],
        [sg.Text(f'Interpretación: {interpretacion}', font=('Helvetica', 12))],
        [sg.Button('OK', size=(10, 2), pad=((20, 0), 3), button_color=('white', 'green')),sg.SaveAs('Guardar Modelo', size=(10, 2), pad=((20, 0), 3), button_color=('white', 'blue'),file_types=(('FLP', '.flp'),),default_extension=str('.flp'),key='--FILE--' )]]

    window = sg.Window('Resultados', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'OK':
            break
        elif event == 'GUARDAR MODELO':
            modelo.save(values('--FILE--'))

    window.close()
    '''
    window = sg.Window('Gráfica de la regresión',mostrar_grafica_regresion(modelo, X, Y),finalize=True)
    window.close()
    '''

def regression_interface(dfs, selected_file):
    """
    Interfaz gráfica para realizar una regresión lineal múltiple.

    Parameters:
    - dfs (dict): Diccionario que contiene los DataFrames cargados.
    - selected_file (str): Nombre del archivo seleccionado.
    """
    df = dfs[selected_file]
    columnas = list(df.columns)

    sg.theme('DarkGrey2')

    layout = [
        [sg.Text('Regresión Lineal Múltiple', font=('Helvetica', 20), justification='center')],
        [sg.Text('Seleccione las variables predictoras:', font=('Helvetica', 12), size=(25, 1)),
         sg.InputCombo(values=columnas, key='predictoras')],
        [sg.Text('Seleccione la variable a predecir:', font=('Helvetica', 12), size=(25, 1)),
         sg.InputCombo(values=columnas, key='predecir')],
        [sg.Button('Realizar Regresión Lineal', size=(20, 2), button_color=('white', 'green')),
         sg.Button('Salir', size=(20, 2), button_color=('white', 'red'))],
    ]

    window = sg.Window('Regresión Lineal Múltiple', layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break
        elif event == 'Realizar Regresión Lineal':
            predictoras = values['predictoras']
            predecir = values['predecir']

            X = df[predictoras]
            Y = df[predecir]

            X_train, X_test, y_train, y_test = train_test_split(X,
                                                                Y,
                                                                test_size=0.2,
                                                                random_state=1234,
                                                                shuffle=True)
            X_train = sm.add_constant(X_train, prepend=True)
            modelo = sm.OLS(endog=y_train, exog=X_train)
            modelo = modelo.fit()

            mostrar_resultados(modelo)

    window.close()

    

def create_row(name,option):
    """
    Crea una fila con un checkbox o un radio button.

    Parameters:
    - name (str): Nombre del elemento.
    - option (int): Opción para determinar el tipo de elemento (0 para checkbox, 1 para radio button).

    Returns:
    - List: Lista que representa la fila.
    """
    if option == 0:
        row = [sg.pin(sg.Col([[sg.Checkbox(str(name))]]))]

    elif option == 1:
        row = [sg.pin(sg.Col([[sg.Radio(str(name), group_id='--VAR-X--')]]))]

    return row


def interface(dfs:dict):
    """
    Interfaz principal que permite cargar archivos, realizar regresiones lineales y gestionar modelos.

    Parameters:
    - dfs (dict): Diccionario que contiene los DataFrames cargados.
    """
    col1 = sg.Column([[sg.Frame(' X ', [[sg.Column([],key='--COLX--')]])]],pad=(0,0))

    col2 = sg.Column([[sg.Frame(' Y ', [[sg.Column([],key='--COLY--')]])]],pad=(0,0))

    
    layout = [
        [sg.Text('Selecciona un archivo')],
        [sg.InputText(key='-Archivo-', disabled=True), sg.FileBrowse(file_types=(("All Files", "*.*"),))],
        [col1],
        [col2],
        [sg.Button('Cargar Archivo'), sg.Button('Realizar Regresión Lineal'), sg.Button('Salir')]]


    # Crear ventana menu
    window = sg.Window('Aplicación de Regresión', layout, finalize=True, resizable= False)


    while True:
        event, values = window.read()
        # Salir de la aplicación si se cierra la ventana o se presiona el botón 'Salir'
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        # Cargar archivo si se presiona el botón 'Cargar Archivo'
        if event == 'Cargar Archivo':
            selected_file = values['-Archivo-'] 
            try:
                # Obtener la extensión del archivo                
                extension = file_extension(selected_file)
                # Leer el archivo según la extensión y cargarlo en un DataFrame
                if extension == 'xlsx':
                    df = pd.read_excel(selected_file)
                    df_numeric = df.select_dtypes(include=[np.number])
                    file_content = df_numeric.to_string(index=False)
                    dfs[selected_file] = df_numeric
                    print(sg.popup_auto_close('¡Archivo cargado con éxito!'))
                    #window['-FILE_CONTENT-'].update(file_content)
                
                if extension == 'csv':
                    #print('hola')
                    df = pd.read_csv(selected_file)
                    df_numeric = df.select_dtypes(include=[np.number])
                    file_content = df_numeric.to_string(index=False)
                    dfs[selected_file] = df_numeric
                    print(sg.popup_auto_close('¡Archivo cargado con éxito!'))

                if extension == 'db':
                    conexion = sqlite3.connect('housing.db')
                    cursor = conexion.cursor()
                    consulta_sql = 'SELECT * FROM california_housing_dataset'
                    cursor.execute(consulta_sql)
                    resultados = cursor.fetchall()
                    nombres_columnas = [descripcion[0] for descripcion in cursor.description]
                    df = pd.DataFrame(resultados, columns=nombres_columnas)
                    
                    df_numeric = df.select_dtypes(include=[np.number])
                    dfs[selected_file] = df_numeric
                    conexion.close()
                    print(sg.popup_auto_close('¡Archivo cargado con éxito!'))

                listX = []
                listY = []
                for i in dfs[selected_file].keys():                    
                    listX.append(sg.Checkbox(str(i)))
                    listY.append(sg.Radio(str(i), group_id='--VAR_Y--'))

                window.extend_layout(window['--COLX--'], [listX])
                window.extend_layout(window['--COLY--'], [listY])
            except Exception as e:
                sg.popup_error(f'Error: {str(e)}')

        # Abrir la interfaz para realizar la regresión lineal si se presiona el botón 'Realizar Regresión Lineal'
        if event == 'Realizar Regresión Lineal':#PARTE DE NATHAN
            window = sg.Window('Aplicacion de regresion', [
            [sg.Text('Seleccione el archivo:', font=('Helvetica', 12), size=(25, 1)),
             sg.InputCombo(values=list(dfs.keys()), key='archivo')],
            [sg.Button('Seleccionar', size=(20, 2), button_color=('white', 'green')),
             sg.Button('Salir', size=(20, 2), button_color=('white', 'red'))],])

            while True:
                event, values = window.read()
                # Salir de la ventana de selección si se cierra la ventana o se presiona el botón 'Salir'
                if event == sg.WINDOW_CLOSED or event == 'Salir':
                    break
                # Abrir la interfaz de regresión lineal si se presiona el botón 'Seleccionar'
                elif event == 'Seleccionar':
                    selected_file = values['archivo']
                    window.close()
                    regression_interface(dfs, selected_file)


    # Cerrar la ventana de la interfaz gráfica al salir
    window.close()




if __name__ == '__main__':    
    dfs = {}
    interface(dfs)

