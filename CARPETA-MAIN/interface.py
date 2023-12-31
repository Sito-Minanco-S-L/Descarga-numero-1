import statsmodels.api as sm
import PySimpleGUI as sg
from sklearn.model_selection import train_test_split
import regression
import files
from modelo import Modelo, load_model, make_prediction
from regression import *



def interface(dfs:dict):
    """
    Interfaz principal que permite cargar archivos, realizar regresiones lineales y gestionar modelos.

    Parameters:
    - dfs (dict): Diccionario que contiene los DataFrames cargados.
    """
    prediction_done = False  # Variable para controlar si ya se ha realizado la predicción
    
    column_1 = sg.Column([[sg.Frame(' X ', [[sg.Column([],key='--COLUMN_X--')]])]],pad=(0,0))

    column_2 = sg.Column([[sg.Frame(' Y ', [[sg.Column([],key='--COLUMN_Y--')]])]],pad=(0,0))

    layout = [

        [sg.InputText(default_text = 'Seleccione el archivo: ', key='-Archivo-', disabled=True, change_submits=True, enable_events=True), sg.FileBrowse(file_types=(("Archivos CSV y Excel y Base de Datos", "*.csv;*.xlsx;*.db"),))],
        [sg.Frame(' X ', [[sg.Column([],key='--COLUMN_X--')]])],
        [sg.Frame(' Y ', [[sg.Column([],key='--COLUMN_Y--')]])],
        [sg.Frame('',[],key='--TABLA--')],
        
        [sg.Frame('',[[
             sg.Column([[sg.Image(key='-IMAGE2-', size=(300, 200))]]),
             sg.Column([[sg.Text('Fórmula del modelo:', key='-COEFICIENTES-', visible=False)],
             [sg.Text('', size=(30, 1), key='-R_SQUARED-', font=('Helvetica', 12))],
             [sg.Text('', size=(90, 1), key='-INTERPRETATION-', font=('Helvetica', 12))]]),
     ]],key='-DATOS_REGRESION-', visible=False)],

        [sg.Frame('',[
             [sg.Frame('Anotaciones', [[sg.Multiline(default_text='Anotaciones sobre la regresión lineal:', size=(30, 5), key='-ANNOTATIONS-', visible=False)]], element_justification='center'),
             sg.Frame('',[[sg.Column([],key='--VARIABLES-PRED--')]],element_justification='centre',title_location='n', font='verdana', key='--HUECO-PRED--')]],
             key='--PREDICCION--', visible=False)],

        [sg.Frame('',[[
            sg.Button('Realizar Regresión Lineal', size=(20, 2), button_color=('white', 'green'),visible=False),
            sg.Button('Salir', size=(20, 2), button_color=('white', 'red'), visible=False),
            sg.Button('', size=(20, 2), button_color=('white', 'grey'),visible=True, key='1'),
            sg.Button('', size=(20, 2), button_color=('white', 'grey'), visible=True, key='2'),
            sg.Button('', size=(20, 2), button_color=('white', 'grey'),visible=True, key='3'),
            sg.Button('', size=(20, 2), button_color=('white', 'grey'),visible=True, key='4'),
            sg.Button('', size=(20, 2), button_color=('white', 'grey'),visible=True, key='5'),
            sg.Button('Realizar Predicción', size=(20, 2), button_color=('white', 'pink'), visible=False,enable_events=True),
            sg.InputText(change_submits=True, key='--FILENAME--', visible=False, enable_events=True),
            sg.FileSaveAs('Guardar', size=(20,2), button_color=('white', 'blue'), visible=False, enable_events=True, default_extension=".flp"),
            sg.InputText(change_submits=True, key='--MODELO--', visible=False, enable_events=True),
            sg.FileBrowse('Cargar Modelo', size=(20,2), button_color=('black', 'orange'), visible=True, enable_events=True)

        ]])],

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
            # Restablecer la variable de estado al cargar un nuevo archivo
            modelo_cargado = False

            if window['-DATOS_REGRESION-'].visible:
                window['-DATOS_REGRESION-'].update(visible=False)
            if window['--HUECO-PRED--'].visible:
                window['--HUECO-PRED--'].update(visible=False)

            selected_file = values['-Archivo-']
            try:
                # Obtener la extensión del archivo                
                extension = files.file_extension(selected_file)
                #testing
                assert extension == 'xlsx' or extension == 'csv' or extension == 'db', "El archivo no tiene un formato adecuado (.xlsx, .csv, .db)"
                # Leer el archivo según la extensión y cargarlo en un DataFrame 
                files.read_file(selected_file, dfs, extension)
                
                list_X = []
                list_Y = []
                list_columns = []

                for i in dfs[selected_file].keys():                    
                    list_X.append(sg.Checkbox(str(i)))
                    list_Y.append(sg.Radio(str(i), group_id='--VARIABLE_Y--'))
                    list_columns.append(i)

                window.extend_layout(window['--COLUMN_X--'], [list_X])
                window.extend_layout(window['--COLUMN_Y--'], [list_Y])

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
            x = [list_columns[key] for key in selected_X]
            y = list_columns[selected_Y]

            if x and y: # Verificar si se seleccionaron variables tanto para X como para Y
                # Obtener el DataFrame seleccionado
                selected_file = values['-Archivo-']
                df = dfs[selected_file]
                # Verificar si las claves seleccionadas existen como columnas en el DataFrame
                # Separar claramente las variables de X e Y
                X = df[x]
                Y = df[y]

                X = X.fillna(X.mean())

                modelo = Modelo(x,y,X,Y)

                regression.show_regression_graph(modelo.get_model(), modelo.get_x_data(), modelo.get_y_data(), window)
        
                # Calcula el R^2, su interpretación y los coeficientes del modelo
                # Calcula el R^2 y su interpretación
                # Construir el texto con el R^2
                # Calcula el R^2 y su interpretación
                r_squared = modelo.get_model().rsquared
                color, interpretation = interpret_r_squared(r_squared)
                # Actualizar el elemento de texto en la interfaz con los detalles del modelo
                window['-R_SQUARED-'].update(value=f'R-cuadrado: {r_squared:.4f}', text_color=color)
                window['-INTERPRETATION-'].update(value=f'Interpretación: {interpretation}')

                regression.regression_elements(modelo.get_model(), window)

                # Obtener el nombre de la variable dependiente (Y)
                variable_dependiente = modelo.get_y_name()
                # Construir la fórmula del modelo
                formula = f"{variable_dependiente} = {modelo.get_coefficients()[0]:.2f}"
                # Agregar los términos para las variables predictoras
                for i, coef in enumerate(modelo.get_coefficients()[1:], start=1):
                    formula += f" {'+' if coef >= 0 else '-'} {abs(coef):.2f} ({modelo.columns_names()[i-1]})"
                # Actualiza el elemento de texto en la interfaz con los coeficientes calculados
                window['-COEFICIENTES-'].update(visible=True, value=formula, font=('Helvetica', 16))
                # Muestra la gráfica de regresión lineal
                regression.show_regression_graph(modelo.get_model(), modelo.get_x_data(),modelo.get_y_data(), window)
                regression.regression_elements(modelo.get_model(), window)

            window['--TABLA--'].update(visible=False)

            window['Realizar Predicción'].update(visible=True)
            window['5'].update(visible=False)

            window['Salir'].update(visible=False)
            window['Cargar Modelo'].update(visible=True)

            window['Guardar'].update(visible=True)
            window['2'].update(visible=False)
            #window['Cargar Modelo'].update(visible=True)
            window['Salir'].update(visible=True)
            window['--PREDICCION--'].update(visible=True)
            window['-DATOS_REGRESION-'].update(visible=True)
            window['-ANNOTATIONS-'].update(visible=True)
            window['Guardar'].update(visible=True)

            
        if event == '--FILENAME--':
            modelo.save_model(values['--FILENAME--'])

        if event == '--MODELO--':
            window['--TABLA--'].update(visible=False)
            
            selected_model = values['--MODELO--'] 
            modelo = load_model(selected_model)
            regression.regression_elements(modelo.get_model(), window)
            
            r_squared = modelo.get_model().rsquared
            color, interpretation = interpret_r_squared(r_squared)
            # Obtener el nombre de la variable dependiente (Y)
            variable_dependiente = modelo.get_y_name()
            # Construir la fórmula del modelo
            formula = f"{variable_dependiente} = {modelo.get_coefficients()[0]:.2f}"
            # Agregar los términos para las variables predictoras
            for i, coef in enumerate(modelo.get_coefficients()[1:], start=1):
                formula += f" {'+' if coef >= 0 else '-'} {abs(coef):.2f} ({modelo.columns_names()[i-1]})"
            # Actualizar los elementos de texto en la interfaz con los detalles del modelo
            window['-R_SQUARED-'].update(value=f'R-cuadrado: {r_squared:.4f}', text_color=color)
            window['-INTERPRETATION-'].update(value=f'Interpretación: {interpretation}')
            window['-COEFICIENTES-'].update(visible=True, value=formula, font=('Helvetica', 16))
            window['Realizar Predicción'].update(visible=True)
            window['5'].update(visible=False)
            window['--TABLA--'].update(visible=True)
            window['--COLUMN_X--'].update(visible=True)
            window['--COLUMN_Y--'].update(visible=True)
            window['--PREDICCION--'].update(visible=True)
            window['-DATOS_REGRESION-'].update(visible=True)
            
        if event == 'Realizar Predicción'and not prediction_done:
            window['-DATOS_REGRESION-'].update(visible=True)
            window['--HUECO-PRED--'].update(visible=True)
            window['--HUECO-PRED--'].update('PREDICCION A PARTIR DEL MODELO')
            layout = []
            for i in range(len(modelo.columns_names())):
                layout.append(sg.Frame(title='',layout=[[sg.Text(modelo.columns_names()[i].upper(), font='verdana')],[sg.Input('',size=(15,40), key=('-valores-pred-'+str(i)))]]))
            layout.append(sg.Frame(title='',layout=[[sg.Button('Submit', size=(6, 2))]]))
            window.extend_layout(window['--VARIABLES-PRED--'], [layout])
            prediction_done = True  # Marcar que la predicción se ha realizado

        if event == 'Submit':
            values_x = []
            for i in range(len(modelo.columns_names())):
                values_x.append(values['-valores-pred-'+str(i)])

            # Verificar si se han ingresado valores
            if all(value for value in values_x):
                result = make_prediction(modelo, values_x)
                texto = 'Resultado --> {:4f}'.format(result)
                window.extend_layout(window['--VARIABLES-PRED--'], [[sg.Text(text=texto,font='verdana',background_color='white',auto_size_text=50, text_color='black')]])
            else:
                sg.popup_error("Por favor, ingresa valores antes de hacer la predicción.")
        # Mostrar la ventana de anotaciones solo en el instante de "Realizar Regresión Lineal" o "Modelo"
        if event in ['Realizar Regresión Lineal', '--MODELO--']:
            
            window['-ANNOTATIONS-'].update(visible=True)

            # Actualizar las anotaciones cuando el usuario escribe en el área de anotaciones
            if event == '-ANNOTATIONS-':
                annotations = values['-ANNOTATIONS-']
                # Puedes hacer lo que desees con el contenido de las anotaciones, como imprimirlo en la consola
                print(annotations)
                
      
    # Cerrar la ventana de la interfaz gráfica al salir
    window.close()