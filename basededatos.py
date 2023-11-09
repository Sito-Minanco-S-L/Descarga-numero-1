'''
import sqlite3
import pandas 

# Conectar a la base de datos (o crearla si no existe)
conexion = sqlite3.connect('housing.db')

# Crear un cursor para ejecutar consultas SQL
cursor = conexion.cursor()

# Ejemplo de consulta SQL para leer datos de la tabla y convertirlos en un DataFrame de pandas
consulta_sql = 'SELECT * FROM california_housing_dataset'

# Ejecutar la consulta y obtener los resultados como una lista de tuplas
cursor.execute(consulta_sql)
resultados = cursor.fetchall()

# Obtener los nombres de las columnas a partir de la descripción del cursor
nombres_columnas = [descripcion[0] for descripcion in cursor.description]

# Crear un DataFrame de pandas a partir de los resultados y los nombres de las columnas
df = pandas.DataFrame(resultados, columns=nombres_columnas)

# Mostrar el DataFrame
print('DataFrame de usuarios:')
print(df)

# Cerrar la conexión
conexion.close()





def cargar_basededatos(file_name):
    conexion = sqlite3.connect('housing.db')
    cursor = conexion.cursor()


    consulta_sql = 'SELECT * FROM california_housing_dataset'
    cursor.execute(consulta_sql)
    resultados = cursor.fetchall()


    nombres_columnas = [descripcion[0] for descripcion in cursor.description]

    df = pandas.DataFrame(resultados, columns=nombres_columnas)


    print('DataFrame de usuarios:')
    print(df)

    conexion.close()







#ivan bujarrilla

'''








import PySimpleGUI as sg
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Definir el diseño de la interfaz gráfica
layout = [
    [sg.Text('Selecciona un archivo')],
    [sg.InputText(key='Archivo'), sg.FileBrowse(file_types=(("All Files", "*.*"),))],
    [sg.Checkbox('X', key='X'), sg.Checkbox('Y', key='Y')],
    [sg.Radio('Archivo Excell', 'Archivo', key = 'Archivo Excell'), sg.Radio('Archivo CSV', 'Archivo', key = 'Archivo CSV'), sg.Radio('Archivo DB', 'Archivo', key = 'Archivo DB')],
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

    if event == 'Archivo Excell':
        

    if event == 'Realizar Regresión':
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

# Cerrar la ventana de la interfaz gráfica al salir
window.close()





#pip install PySimpleGUI
