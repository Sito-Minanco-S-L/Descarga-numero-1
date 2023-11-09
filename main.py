import os
import csv
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
import sqlite3
import PySimpleGUI as sg
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import magic 





def interface():
    layout0 = [
        [sg.Button('Cargar archivo')],
        [sg.Button('Mostrar modelos')],
        [sg.Button('Cargar modelo')]
    ]
    
    layout1 = [
        [sg.Text('Selecciona un archivo')],
        [sg.InputText(key='Archivo'), sg.FileBrowse(file_types=(("All Files", "*.*"),))],
        [sg.Checkbox('X', key='X'), sg.Checkbox('Y', key='Y')],
        [sg.Button('Realizar Regresión'), sg.Button('Salir')],
        [sg.Text('Resultado de la Regresión Lineal:', size=(30, 1), key='ResultadoRegresion')],
        [sg.Button('Guardar Modelo')]
    ]

    layout2 = [
        [sg.Text('Guardar Modelo de Regresión Lineal')],
        [sg.FileSaveAs(key='fig_save',file_types=(('FARLOPA', '.farlopa')))]
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
                
                if 'csv' in mime_type.lower():
                    df = pd.read_csv(selected_file)
                    df_numeric = df.select_dtypes(include=[np.number])
                    file_content = df_numeric.to_string(index=False)
                    window['-FILE_CONTENT-'].update(file_content)

                if 'db' in mime_type.lower():
                    df = pd.read_excel(selected_file)
                    df_numeric = df.select_dtypes(include=[np.number])
                    file_content = df_numeric.to_string(index=False)
                    window['-FILE_CONTENT-'].update(file_content)
                
                else:
                    with open(selected_file, 'r') as file:
                        file_content = file.read()
                    window['-FILE_CONTENT-'].update(file_content)
                num_lines = file_content.count('\n')+1
                window['-FILE_CONTENT-'].Widget.config(height=num_lines) 

            except Exception as e:
                sg.popup_error(f'Error: {str(e)}')
        

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


        if event == 'Guardar Modelo':
            window = sg.Window('Aplicación de Regresión', layout2)


    

# Cerrar la ventana de la interfaz gráfica al salir
    window.close()


'''
if event == 'Submit':
        selected_file = values['-FILENAME-']
         #sg.popup(f'File selected: {selected_file}') #para mostrar el nombre del archivo que se selecciona.
        try:
            mime = magic.Magic()
            mime_type = mime.from_file(selected_file)

            if 'excel' in mime_type.lower():
                df = pd.read_excel(selected_file)
                file_content = df.to_string(index=False)
                window['-FILE_CONTENT-'].update(file_content)
            else:
                with open(selected_file, 'r') as file:
                    file_content = file.read()
                window['-FILE_CONTENT-'].update(file_content)
            num_lines = file_content.count('\n')+1
            window['-FILE_CONTENT-'].Widget.config(height=num_lines)
        
        except Exception as e:
            sg.popup_error(f'Error: {str(e)}')
    
    
    if event == '-HSCROLL-':
        scroll_value = int(values['-HSCROLL-'])
        window['-FILE_CONTENT-'].update(file_content[scroll_value:scroll_value + 50])

'''

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

def menu1(dfs):
    
    print("""
- · MENU DE OPCIONES · -
          
-> 1: Cargar datos csv
-> 2: Cargar datos excel
-> 3: Cargar base de datos
-> 4: Mostrar archivos cargados
-> 5: Hacer regresion lineal
-> 6: Cargar modelo
-> 0: Salir del programa
""")
    option = int(input(": "))

    if option == 1:
        file_name = str(input("file_name: "))
        os.system('clear')
        df = cargar_csv(file_name)
        dfs[file_name] = df
        menu1(dfs)
        

    if option == 2:
        file_name = str(input("file_name: "))
        os.system('clear')
        df = cargar_excel(file_name)
        dfs[file_name] = df
        menu1(dfs)

    if option == 3:
        file_name = str(input("file_name: "))
        os.system('clear')
        df = cargar_basededatos(file_name)
        dfs[file_name] = df
        menu1(dfs)
    
    if option == 4:
        for i in dfs.keys():
            print(i)

        menu1(dfs)

    
    if option == 5:
        print("Seleciona el archivo: ")
        for i in dfs.keys():
            print(i)
        nombre_archivo = str(input(": "))
        df = dfs[nombre_archivo]
        print('\nColumnas a selecionnar:\n ')
        columnas = []
        for i in range(len(df.columns)):
            columna = df.columns[i]
            columnas.append(columna)
            print("->", i, ":", columna)

        op_columna1 = int(input("\nSelecciona la variable predictora: "))
        op_columna2= int(input("\nSelecciona la variable a predecir: "))


        X = df[columnas[op_columna1]]
        Y = df[columnas[op_columna2]]

        print("\n Variable X:")
        print("\n\t",df.columns[op_columna1])
        print(X)
        print("\n Variable Y:")
        print("\n\t",df.columns[op_columna2])
        print(Y)

        X = df.iloc[:, op_columna1]
        Y = df.iloc[:, op_columna2 ]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            Y,
            test_size=0.2,
            random_state=1234,
            shuffle=True
                    )
        X_train = sm.add_constant(X_train, prepend=True)
        modelo = sm.OLS(endog=y_train, exog=X_train,)
        modelo = modelo.fit()
        print("\n", modelo.summary())
        
        print("¿Desea guardar el modelo? (s/n): ")
        op = str(input(": "))

        if op == 's':
            nombre_modelo = str(input("Nombre modelo: "))
            modelo.save(nombre_modelo+'.chantada')

        [sg.Text('Resultado de la Regresión Lineal:', size=(30, 1), key='ResultadoRegresion')]
        
        menu1(dfs)

    if option == 6:
        nombre_modelo = str(input("Introduzca el nombre del modelo a cagar: "))
        modelo1 = sm.load(nombre_modelo+'.chantada')
        print("\n", modelo1.summary())

        menu1(dfs)



        



if __name__ == '__main__':    
    dfs = {}

    #menu1(dfs)
    interface()

