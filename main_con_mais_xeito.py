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

"""
def interface():
    layout = []
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
        '''
        # ESTE IF ME PARECE Q NON SE USAAAA!!  (o siguiente e o de nathan)
        if event == 'Realizar Regresión':##ESTO CREO Q NON SE ESTA USANDO
            # Leer los datos del archivo seleccionado
            archivo = values['Archivo']
            datos = pd.read_csv(archivo)   
            # Seleccionar las variables según los checkboxes
            if values['Variable1']:
                x = datos['Variable1'].values.reshape(-1, 1)
            else:
                x = datos['Variable2'].values.reshape(-1, 1)
            
            y = datos['Variable_objetivo'].values
            # Dividir los datos en conjuntos de entrenamiento y prueba
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
            # Crear un modelo de regresión lineal
            modelo = LinearRegression()
            # Entrenar el modelo
            modelo.fit(x_train, y_train)
            # Realizar predicciones en el conjunto de prueba
            y_pred = modelo.predict(x_test)
            # Calcular el error cuadrático medio
            mse = mean_squared_error(y_test, y_pred)
            # Mostrar el error cuadrático medio en la interfaz gráfica
            window['Resultado'].update(f'Error Cuadrático Medio: {mse:.2f}')
            '''

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


def prueba():
    layout = [
        [sg.Text('Selecciona un archivo')],
        [sg.InputText(key='-Archivo-'),sg.FileBrowse(file_types=(("All Files", "*.*"),))],
        [sg.Button('Cargar Archivo'), sg.Button('Realizar Regresión Lineal'), sg.Button('Salir')]]
    
    window = sg.Window('Aplicación de Regresión', layout, finalize=True)

    while True:
        event, values = window.read()

"""

def create_row(row_counter, row_number_view):
    row =  [sg.pin(
        sg.Col([[
            sg.Button("X", border_width=0, button_color=(sg.theme_text_color(), sg.theme_background_color()), key=('-DEL-', row_counter)),
            sg.Input(size=(20,1), key=('-DESC-', row_counter)),
            sg.Text(f'Row {row_number_view}', key=('-STATUS-', row_counter))]],
        key=('-ROW-', row_counter)
        ))]
    return row

def create_row2():
    row = [sg.pin(
        sg.Col()
    )]


layout = [  [sg.Text('Add and "Delete" Rows From a Window', font='15')],
            [sg.Column([create_row(0, 1)], k='-ROW_PANEL-')],
            [sg.Text("Exit", enable_events=True, key='-EXIT-', tooltip='Exit Application'),
            sg.Text("Refresh", enable_events=True, key='-REFRESH-', tooltip='Exit Application'),
            sg.Text('+', enable_events=True, k='-ADD_ITEM-', tooltip='Add Another Item')]]

window = sg.Window('Dynamically Adding Elements', 
    layout,  use_default_focus=False, font='15')

row_counter = 0
row_number_view = 1
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break
    if event == '-ADD_ITEM-':
        row_counter += 1
        row_number_view += 1
        print("Actual Row Number: ", row_counter)
        print("Displayed Row Number: ", row_number_view)
        # Allows you to add items to a layout
        # These items cannot be deleted, but can be made invisible
        window.extend_layout(window['-ROW_PANEL-'], [create_row(row_counter, row_number_view)])
    elif event[0] == '-DEL-':
        row_number_view -= 1
        window[('-ROW-', event[1])].update(visible=False)
window.close()

