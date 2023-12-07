import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import statsmodels.api as sm
#import statsmodels.formula.api as smf
import sqlite3
import PySimpleGUI as sg
#from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
#from sklearn.metrics import mean_squared_error
import regression


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







def interface(dfs:dict):
    """
    Interfaz principal que permite cargar archivos, realizar regresiones lineales y gestionar modelos.

    Parameters:
    - dfs (dict): Diccionario que contiene los DataFrames cargados.
    """
    col1 = sg.Column([[sg.Frame(' X ', [[sg.Column([],key='--COLX--')]])]],pad=(0,0))

    col2 = sg.Column([[sg.Frame(' Y ', [[sg.Column([],key='--COLY--')]])]],pad=(0,0))

    layout = [
    [sg.InputText(default_text = 'Seleccione el archivo: ', key='-Archivo-', disabled=True, change_submits=True, enable_events=True), sg.FileBrowse(file_types=(("Archivos CSV y Excel y Base de Datos", "*.csv;*.xlsx;*.db"),))],
    [sg.Frame(' X ', [[sg.Column([],key='--COLX--')]])],
    [sg.Frame(' Y ', [[sg.Column([],key='--COLY--')]])],
    [sg.Frame('',[],key='--TABLA--')],
    [sg.Column([
        [sg.Image(key='-IMAGE1-', size=(300, 200)), sg.Image(key='-IMAGE2-', size=(300, 200))]
    ], justification='center')],

    [sg.Frame('',[[
        sg.Button('Realizar Regresión Lineal', size=(20, 2), button_color=('white', 'green'),visible=False),
        sg.Button('Salir', size=(20, 2), button_color=('white', 'red'), visible=False),
        sg.Button('', size=(20, 2), button_color=('white', 'grey'),visible=True, key='1'),
        sg.Button('', size=(20, 2), button_color=('white', 'grey'), visible=True, key='2'),
        sg.Button('', size=(20, 2), button_color=('white', 'grey'),visible=True, key='3'),
        sg.Button('', size=(20, 2), button_color=('white', 'grey'), visible=True, key='4'),
        sg.InputText(change_submits=True, key='--FILENAME--', visible=False, enable_events=True),
        sg.FileSaveAs('Guardar', size=(20,2), button_color=('white', 'blue'), visible=False, enable_events=True, default_extension=".flp"),
        sg.InputText(change_submits=True, key='--MODELO--', visible=False, enable_events=True),
        sg.FileBrowse('Cargar Modelo', size=(20,2), button_color=('black', 'orange'), visible=False, file_types='.flp', enable_events=True)

      ]])]
    ]


    # Crear ventana menu
    window = sg.Window('Aplicación de Regresión', layout, finalize=True, resizable= False)


    while True:
        event, values = window.read()
        # Salir de la aplicación si se cierra la ventana o se presiona el botón 'Salir'
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        # Cargar archivo si se presiona el botón 'Cargar Archivo'
        if event == '-Archivo-':
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
                lista_columnas = []

                for i in dfs[selected_file].keys():                    
                    listX.append(sg.Checkbox(str(i)))
                    listY.append(sg.Radio(str(i), group_id='--VAR_Y--'))
                    lista_columnas.append(i)


                window.extend_layout(window['--COLX--'], [listX])
                window.extend_layout(window['--COLY--'], [listY])

                table_data = dfs[selected_file].to_numpy().tolist()
                table_headings = dfs[selected_file].columns.tolist()
                window.extend_layout(window['--TABLA--'], [[sg.Table(table_data, table_headings)]])

                if window['1'].visible:
                    window['Realizar Regresión Lineal'].update(visible=True)
                    window['1'].update(visible=False)
                if window['2'].visible:
                    window['2'].update(visible=False)
                    window['2'].update(visible=True)

                window['Cargar Modelo'].update(visible=True)
                window['3'].update(visible=False)

                window['Salir'].update(visible=True)
                window['4'].update(visible=False)

            except Exception as e:
                sg.popup_error(f'Error: {str(e)}')

        # Abrir la interfaz para realizar la regresión lineal si se presiona el botón 'Realizar Regresión Lineal'

        if event == 'Realizar Regresión Lineal':
            selected_X = [key for key, value in values.items() if value is True and key != '--VAR Y--']
            selected_Y = selected_X[-1] - len(dfs[selected_file].columns)
            selected_X = selected_X[:-1]
            x = [lista_columnas[key] for key in selected_X]
            y = lista_columnas[selected_Y]

            # Verificar si se seleccionaron variables tanto para X como para Y
            if x and y:
                # Obtener el DataFrame seleccionado
                selected_file = values['-Archivo-']
                df = dfs[selected_file]

                # Verificar si las claves seleccionadas existen como columnas en el DataFrame

                # Separar claramente las variables de X e Y
                X = df[x]
                Y = df[y]

                X = X.fillna(X.mean())

                X_train, X_test, y_train, y_test = train_test_split(X,
                                                                    Y,
                                                                    test_size=0.2,
                                                                    random_state=1234,
                                                                    shuffle=True)
                X_train = sm.add_constant(X_train)
                modelo = sm.OLS(endog=y_train, exog=X_train)
                modelo = modelo.fit()
                # Muestra la gráfica de regresión lineal
                regression.mostrar_grafica_regresion(modelo, X,Y, window)
                regression.cosas_regresion(modelo, window)

            window['Salir'].update(visible=False)
            window['Cargar Modelo'].update(visible=False)

            window['Guardar'].update(visible=True)
            window['2'].update(visible=False)

            window['Cargar Modelo'].update(visible=True)
            
            window['Salir'].update(visible=True)


        if event == '--FILENAME--':
            modelo.save(values['--FILENAME--'])

        if event == '--MODELO--':
            selected_model = values['--MODELO--'] 
            modelo = sm.load(selected_model)
            regression.cosas_regresion(modelo, window)
            #Muestra la gráfica de regresión lineal
            regression.mostrar_grafica_regresion(modelo, X, Y, window)

                



    window.close()


    # Cerrar la ventana de la interfaz gráfica al salir




if __name__ == '__main__':    
    dfs = {}
    interface(dfs)

