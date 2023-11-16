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


def mostrar_resultados(modelo):
    """
    Muestra los resultados de un modelo de regresión lineal, incluido el R-cuadrado.

    Parameters:
    - modelo: Modelo de regresión lineal ajustado.
    """
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

    def mostrar_grafica_regresion(modelo, X, y):
        plt.scatter(X, y, label='Datos')
        plt.plot(X, modelo.predict(sm.add_constant(X)), color='red', label='Regresión Lineal')
        plt.xlabel('Variable Predictora')
        plt.ylabel('Variable a Predecir')
        plt.legend()
        plt.show()

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
    window = sg.Window('Gráfica de la regresión',mostrar_grafica_regresion(modelo, X, y),finalize=True)
    window.close()
    '''
def regression_interface(dfs, selected_file):
    """
    Interfaz gráfica para realizar una regresión lineal.

    Parameters:
    - dfs (dict): Diccionario que contiene los DataFrames cargados.
    - selected_file (str): Nombre del archivo seleccionado.
    """
    df = dfs[selected_file]
    columnas = list(df.columns)

    sg.theme('DarkGrey2')

    layout = [
        [sg.Text('Regresión Lineal', font=('Helvetica', 20), justification='center')],
        [sg.Text('Seleccione la variable predictora:', font=('Helvetica', 12), size=(25, 1)),
         sg.InputCombo(values=columnas, key='predictora')],
        [sg.Text('Seleccione la variable a predecir:', font=('Helvetica', 12), size=(25, 1)),
         sg.InputCombo(values=columnas, key='predecir')],
        [sg.Button('Realizar Regresión Lineal', size=(20, 2), button_color=('white', 'green')),
         sg.Button('Salir', size=(20, 2), button_color=('white', 'red'))],]

    window = sg.Window('Regresión Lineal', layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break
        elif event == 'Realizar Regresión Lineal':
            predictora = values['predictora']
            predecir = values['predecir']

            X = df[predictora]
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

    

def interface(dfs:dict):
    """
    Interfaz principal que permite cargar archivos, realizar regresiones lineales y gestionar modelos.

    Parameters:
    - dfs (dict): Diccionario que contiene los DataFrames cargados.
    """
    layout0 = [
        [sg.Button('Cargar archivo')],
        [sg.Button('Mostrar modelos')],
        [sg.Button('Cargar modelo')]]
    
    layout1 = [
        [sg.Text('Selecciona un archivo')],
        [sg.InputText(key='-Archivo-'), sg.FileBrowse(file_types=(("All Files", "*.*"),))],
        [sg.Button('Cargar Archivo'), sg.Button('Realizar Regresión Lineal'), sg.Button('Salir')]]

    layout2 = [
        [sg.Text('Guardar Modelo de Regresión Lineal')],
        [sg.FileSaveAs(key='fig_save',file_types=(('FARLOPA', '.farlopa'),))]]

    # Crear ventana menu
    window = sg.Window('Aplicación de Regresión', layout0, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Cargar archivo':
            #ventana opcion cargar archivos
            window = sg.Window('Aplicación de Regresión', layout1)
            break
        if event == 'Mostrar modelos':
            window = sg.Window('Aplicación de Regresión', [[sg.Text('Esta merda esta sin facer')]])
        if event == 'Cargar modelo':
            window = sg.Window('Aplicación de Regresión', [[sg.Text('Esta merda esta sin facer')]])

    while True:
        event, values = window.read()
       
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Cargar Archivo':
            selected_file = values['-Archivo-'] 
            try:
                extension = file_extension(selected_file)
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
                
            except Exception as e:
                sg.popup_error(f'Error: {str(e)}')

        if event == 'Realizar Regresión Lineal':#PARTE DE NATHAN
            window = sg.Window('Aplicacion de regresion', [
            [sg.Text('Seleccione el archivo:', font=('Helvetica', 12), size=(25, 1)),
             sg.InputCombo(values=list(dfs.keys()), key='archivo')],
            [sg.Button('Seleccionar', size=(20, 2), button_color=('white', 'green')),
             sg.Button('Salir', size=(20, 2), button_color=('white', 'red'))],])

            while True:
                event, values = window.read()

                if event == sg.WINDOW_CLOSED or event == 'Salir':
                    break
                elif event == 'Seleccionar':
                    selected_file = values['archivo']
                    window.close()
                    regression_interface(dfs, selected_file)

        if event == 'Guardar Modelo':
            window = sg.Window('Aplicación de Regresión', layout2)

    # Cerrar la ventana de la interfaz gráfica al salir
    window.close()




if __name__ == '__main__':    
    dfs = {}
    interface(dfs)

