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


## ESTA FUNCION FIXENA COPIANDO UN CACHO DO CODIGO DE NATHAN
## ALCULA COUSAS E MOSTRA COUSAS POR PANTALLA UNHA VEZ ESTA FEITO 
## O MODELO, FACIAME FALTA PA CANDO SE CARGASE O MODELO, ENTONCES CONVERTINO NUNHA FUNCION
def cosas_regresion(modelo, window):
    r_squared = modelo.rsquared
    color, interpretacion = interpretar_r_cuadrado(r_squared)

    resultados = modelo.summary()
    resultados_str = str(resultados)
    #window['-OUTPUT-'].update(value=resultados_str)
    
    layout_resultados = [
        [sg.Text(f'R-cuadrado: {r_squared:.4f}', font=('Helvetica', 12), text_color=color)],
        [sg.Text(f'Interpretación: {interpretacion}', font=('Helvetica', 12))]
    ]
    window_resultados = sg.Window('Resultados del Modelo', layout_resultados)
    event, values = window_resultados.read()
    window_resultados.close()



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
    [sg.InputText(default_text = 'Seleccione el archivo: ', key='-Archivo-', disabled=True, change_submits=True, enable_events=True), sg.FileBrowse(file_types=(("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx"), ("Archivos de Base de Datos", "*.db"),))],
    [col1],
    [col2],
    [sg.Frame('',[],key='--TABLA--')],
    [sg.Frame('',[[
        sg.Button('Realizar Regresión Lineal', size=(20, 2), button_color=('white', 'green'),visible=False, key='-Regresion-'),
        sg.Button('Salir', size=(20, 2), button_color=('white', 'red'), visible=False, key='-Salir-'),
        sg.InputText(change_submits=True, key='--FILENAME--', visible=False, enable_events=True),
        sg.FileSaveAs('Guardar', size=(20,2), button_color=('white', 'blue'), visible=False, key='-Guardar-', enable_events=True, default_extension=".flp"),
        sg.InputText(change_submits=True, key='--MODELO--', visible=False, enable_events=True),
        sg.FileBrowse('Cargar Modelo', size=(20,2), button_color=('black', 'orange'), visible=False, key='-Cargar-', file_types='.flp', enable_events=True)
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
                window['-Regresion-'].update(visible=True)
                
                window['-Salir-'].update(visible=True)

                table_data = dfs[selected_file].to_numpy().tolist()
                table_headings = dfs[selected_file].columns.tolist()
                window.extend_layout(window['--TABLA--'], [[sg.Table(table_data, table_headings)]])

                event, values = window.read()

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
                cosas_regresion(modelo, window)
                # Muestra la gráfica de regresión lineal
                mostrar_grafica_regresion(modelo, X,Y)
                
        if event == '--FILENAME--':
            modelo.save(values['--FILENAME--'])

        if event == '--MODELO--':
            selected_model = values['--MODELO--'] 
            modelo = sm.load(selected_model)
            cosas_regresion(modelo, window)
            #Muestra la gráfica de regresión lineal
            mostrar_grafica_regresion(modelo, X, Y)
        window['-Cargar-'].update(visible=True)
                
            




    window.close()


    # Cerrar la ventana de la interfaz gráfica al salir




if __name__ == '__main__':    
    dfs = {}
    interface(dfs)

