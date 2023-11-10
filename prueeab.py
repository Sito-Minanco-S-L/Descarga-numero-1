import os
import csv
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sqlite3
import PySimpleGUI as sg
import magic

def interpretar_r_cuadrado(r_cuadrado):
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
        [sg.Button('OK', size=(10, 2), pad=((20, 0), 3), button_color=('white', 'green'))]
    ]

    window = sg.Window('Resultados', layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'OK':
            break

    window.close()



def interface(dfs:dict):
    layout0 = [
        [sg.Button('Cargar archivo')],
        [sg.Button('Mostrar modelos')],
        [sg.Button('Cargar modelo')]
    ]
    
    layout1 = [
        [sg.Text('Selecciona un archivo')],
        [sg.InputText(key='Archivo'), sg.FileBrowse(file_types=(("All Files", "*.*"),))],
        [sg.Checkbox('X', key='X'), sg.Checkbox('Y', key='Y')],
        [sg.Button('Realizar Regresión Lineal'), sg.Button('Salir')],
        [sg.Button('Guardar Modelo')]
    ]

    layout2 = [
        [sg.Text('Guardar Modelo de Regresión Lineal')],
        [sg.FileSaveAs(key='fig_save',file_types=(('FARLOPA', '.farlopa')))]
    ]
    
    layout3 = [
            [sg.Text('Seleccione el archivo:', font=('Helvetica', 12), size=(25, 1)),
             sg.InputCombo(values=list(dfs.keys()), key='archivo')],
            [sg.Button('Seleccionar', size=(20, 2), button_color=('white', 'green')),
             sg.Button('Salir', size=(20, 2), button_color=('white', 'red'))],
        ]

    
    # Crear ventana menu
    window = sg.Window('Aplicación de Regresión', layout0)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Cargar archivo':
            #ventana opcion cargar archivos
            window = sg.Window('Aplicación de Regresión', layout1)
            break


    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        if event == 'Submit':
            selected_file = values['-FILENAME-'] 
            try:
                mime = magic.Magic()
                mime_type = mime.from_file(selected_file)
                if 'excel' in mime_type.lower():
                    df = pd.read_excel(selected_file)
                    df_numeric = df.select_dtypes(include=[np.number])
                    file_content = df_numeric.to_string(index=False)
                    window['-FILE_CONTENT-'].update(file_content)
                    print(selected_file)
                    dfs[selected_file] = df_numeric
                
                if 'csv' in mime_type.lower():
                    df = pd.read_csv(selected_file)
                    df_numeric = df.select_dtypes(include=[np.number])
                    file_content = df_numeric.to_string(index=False)
                    window['-FILE_CONTENT-'].update(file_content)
                    dfs[selected_file] = df_numeric


                if 'db' in mime_type.lower():
                    df = pd.read_excel(selected_file)
                    df_numeric = df.select_dtypes(include=[np.number])
                    file_content = df_numeric.to_string(index=False)
                    window['-FILE_CONTENT-'].update(file_content)
                    dfs[selected_file] = df_numeric

                
                else:
                    with open(selected_file, 'r') as file:
                        file_content = file.read()
                    window['-FILE_CONTENT-'].update(file_content)
                num_lines = file_content.count('\n')+1
                window['-FILE_CONTENT-'].Widget.config(height=num_lines) 

            except Exception as e:
                sg.popup_error(f'Error: {str(e)}')
        



        if event == 'Realizar Regresion Lineal':#PARTE DE NATHAN
            window = sg.Window('Regresión Lineal', layout3, finalize=True)

            while True:
                event, values = window.read()

                if event == sg.WINDOW_CLOSED or event == 'Salir':
                    break
                elif event == 'Seleccionar':
                    selected_file = values['archivo']
                    window.close()


        if event == 'Guardar Modelo':
            window = sg.Window('Aplicación de Regresión', layout2)


    

# Cerrar la ventana de la interfaz gráfica al salir
    window.close()


def cargar_csv(file_name):
    df = pd.read_csv(file_name, sep = ',')
    df_numeric = df.select_dtypes(include=[np.number])
    #print(df)
    print(df_numeric)
    return(df_numeric)    

def cargar_excel(file_name):
    df = pd.read_excel(file_name)
    df_numeric = df.select_dtypes(include=[np.number])
    #print(df)
    print(df_numeric)
    return(df_numeric)

def cargar_basededatos(file_name):
    conexion = sqlite3.connect(file_name)
    cursor = conexion.cursor()


    consulta_sql = 'SELECT * FROM california_housing_dataset'
    cursor.execute(consulta_sql)
    resultados = cursor.fetchall()


    nombres_columnas = [descripcion[0] for descripcion in cursor.description]

    df = pd.DataFrame(resultados, columns=nombres_columnas)


    df_numeric = df.select_dtypes(include=[np.number])
    print(df_numeric)

    conexion.close()
    return(df_numeric)





if __name__ == '__main__':    
    dfs = {}

    #menu1(dfs)
    interface(dfs)

