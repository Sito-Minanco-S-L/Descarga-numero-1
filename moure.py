import PySimpleGUI as sg
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Definir el diseño de la interfaz gráfica
layout = [
    [sg.Text('Selecciona un archivo CSV')],
    [sg.InputText(key='Archivo'), sg.FileBrowse()],
    [sg.Radio('Variable 1', 'VAR', key='Variable1'), sg.Radio('Variable 2', 'VAR', key='Variable2')],
    [sg.Button('Realizar Regresión'), sg.Button('Salir')],
    [sg.Text('', size=(30, 1), key='Resultado')]
]

# Crear la ventana de la interfaz gráfica
window = sg.Window('Aplicación de Regresión', layout)

# Bucle principal para la interfaz gráfica
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Salir':
        break
    if event == 'Realizar Regresión':
        # Leer los datos del archivo seleccionado
        archivo = values['Archivo']
        datos = pd.read_csv(archivo)
        
        # Seleccionar la variable según el radiobutton seleccionado
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

# Cerrar la ventana de la interfaz gráfica al salir
window.close()