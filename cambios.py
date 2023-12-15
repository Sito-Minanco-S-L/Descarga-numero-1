import statsmodels.api as sm
import PySimpleGUI as sg
from sklearn.model_selection import train_test_split
import regression
import files
from modelo import Modelo

def interface(dfs:dict):
    """
    Interfaz principal que permite cargar archivos, realizar regresiones lineales y gestionar modelos.

    Parameters:
    - dfs (dict): Diccionario que contiene los DataFrames cargados.
    """
    column_1 = sg.Column([[sg.Frame(' X ', [[sg.Column([],key='--COLUMN_X--')]])]],pad=(0,0))

    column_2 = sg.Column([[sg.Frame(' Y ', [[sg.Column([],key='--COLUMN_Y--')]])]],pad=(0,0))

    layout = [
    [sg.InputText(default_text = 'Seleccione el archivo: ', key='-Archivo-', disabled=True, change_submits=True, enable_events=True), sg.FileBrowse(file_types=(("Archivos CSV y Excel y Base de Datos", "*.csv;*.xlsx;*.db"),))],
    [sg.Frame(' X ', [[sg.Column([],key='--COLUMN_X--')]])],
    [sg.Frame(' Y ', [[sg.Column([],key='--COLUMN_Y--')]])],
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

                modelo.guardar()
                print('hola')
                # Muestra la gráfica de regresión lineal
                regression.show_regression_graph(modelo.get_modelo(), modelo.get_x_data(),modelo.get_y_data(), window)
                regression.regression_elements(modelo.get_modelo(), window)

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
            regression.regression_elements(modelo, window)
            #Muestra la gráfica de regresión lineal
            regression.show_regression_graph(modelo, X, Y, window)

# Cerrar la ventana de la interfaz gráfica al salir
    window.close()
















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