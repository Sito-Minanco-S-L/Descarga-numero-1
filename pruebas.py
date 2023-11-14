import os
import csv
import pandas
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
import sqlite3
import PySimpleGUI as sg
import pandas as pd
import magic 


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

def menu1(dfs):
    
    print("""
- · MENU DE OPCIONES · -
          
-> 1: Cargar datos csv
-> 2: Cargar datos excel
-> 3: Mostrar archivos cargados
-> 4: Hacer regresion lineal
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
        for i in dfs.keys():
            print(i)

        menu1(dfs)

    
    if option == 4:
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

        menu1(dfs)

        


        
    

import PySimpleGUI as sg
import pandas as pd
import magic 
def interface1():
    sg.ChangeLookAndFeel('GreenTan')
    # ------ Menu Definition ------ #
    menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
                ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Help', '&About...'], ]

    # ------ Column Definition ------ #
    column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
            [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
            [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
            [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]
    
    column2 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
            [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
            [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
            [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

    layout = [
        [sg.Menu(menu_def, tearoff=True)],
        [sg.Text('(Almost) All widgets in one Window!', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
        [sg.Text('Here is some text.... and a place to enter text')],
        [sg.InputText('This is my text')],
        [sg.Frame(layout=[
        [sg.Checkbox('Checkbox', size=(10,1)),  sg.Checkbox('My second checkbox!', default=True)],
        [sg.Radio('My first Radio!     ', "RADIO1", default=True, size=(10,1)), sg.Radio('My second Radio!', "RADIO1")]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
        [sg.Multiline(default_text='This is the default Text should you decide not to type anything', size=(35, 3)),
        sg.Multiline(default_text='A second multi-line', size=(35, 3))],
        [sg.InputCombo(('Combobox 1', 'Combobox 2'), size=(20, 1)),
        sg.Slider(range=(1, 100), orientation='h', size=(34, 20), default_value=85)],
        [sg.InputOptionMenu(('Menu Option 1', 'Menu Option 2', 'Menu Option 3'))],
        [sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3)),
        sg.Frame('Labelled Group',[[
        sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=25, tick_interval=25),
        sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=75),
        sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=10),
        sg.Column(column1, background_color='lightblue')]])],
        [sg.Text('_' * 80)],
        [sg.Text('Choose A Folder', size=(35, 1))],
        [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
        sg.InputText('Default Folder'), sg.FolderBrowse()],
        [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]]

    window = sg.Window('Everything bagel', layout, default_element_size=(40, 1), grab_anywhere=False)
    event, values = window.read()
    sg.Popup('Title',
         'The results of the window.',
         'The button clicked was "{}"'.format(event),
         'The values are', values)



def interface2():
    sg.ChangeLookAndFeel('GreenTan')

    # ------ Menu Definition ------ #
    menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
                ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Help', '&About...'], ]

    menu_def = [ ]

    layout = [
        [sg.Menu(menu_def, tearoff=True)],
        [sg.Text('INTERFACE', size=(30, 1), justification='centre', font=("Helvetica", 15), relief=sg.RELIEF_RAISED, expand_x=True)],
        [sg.Text('File', size=(15, 1), auto_size_text=False, justification='right'),
        sg.InputText('Default File',  key = '-FILENAME-', expand_x=True), sg.FileBrowse(file_types=(("All Files", "*.*"),))], #se puede limitar el tipo de archivo al que se quiere permitir seleccionar.                                                                   #estableccemos el parámetro key para poder acceder posteriormente al elemento.
        [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()],
        [sg.Multiline('', size=(110, 50), key='-FILE_CONTENT-', disabled=True, auto_refresh=True)],
        
        ]                                                                 #cambiando filebrowse por folderbrowse seleccionamos o archivos o carpetas.

    window = sg.Window('Everything bagel', layout,size=(800,600), default_element_size=(40, 1), grab_anywhere=False)
    event, values = window.read()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

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
        

    window.close()
    


if __name__ == '__main__':
    dfs = {}

    menu1(dfs)
