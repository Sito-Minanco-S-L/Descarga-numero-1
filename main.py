import os
import csv
import pandas
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
import sqlite3
import PySimpleGUI as sg



def interface():
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



def cargar_csv(file_name):
    df = pandas.read_csv(file_name, sep = ',')
    df_numeric = df.select_dtypes(include=[np.number])
    #print(df)
    print(df_numeric)
    return(df_numeric)    

def cargar_excell(file_name):
    df = pandas.read_excel(file_name)
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

    df = pandas.DataFrame(resultados, columns=nombres_columnas)


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
        df = cargar_excell(file_name)
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

        menu1(dfs)

    if option == 6:
        nombre_modelo = str(input("Introduzca el nombre del modelo a cagar: "))
        modelo1 = sm.load(nombre_modelo+'.chantada')
        print("\n", modelo1.summary())

        menu1(dfs)



        
    
    

    


if __name__ == '__main__':    
    dfs = {}

    menu1(dfs)

