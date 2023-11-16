import PySimpleGUI as sg
import pandas as pd 
'''
actualizar una misma ventana sin crear varias distintas 
sg.theme('BluePurple')

layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15,1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Show'), sg.Button('Exit')]]

window = sg.Window('Pattern 2B', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

window.close()
'''

import PySimpleGUI as sg

sg.theme('DarkGrey5')


def create_row(option):
    
    if option == 0:
        row = [sg.pin(
            sg.Col([[
                sg.Checkbox('hola'), sg.Text('Cosa de prueba')
            ]])
        )]

    elif option == 1:
        row = [sg.pin(
            sg.Col([[
                sg.Radio('prrrueba', group_id='--VAR-X--'), sg.Text('Cosa de prueba')
            ]])
        )]


    return row


# Definir el diseño de las columnas
column_layout1 = [
    [sg.Text('VARIABLES X')],
    [sg.Text('X', size=(10,), key='-VARX-')] 
]

column_layout2 = [
    [sg.Text('VARIABLE Y')],
    [sg.Text('Y', size=(10,), key='-VARY-')]
]

column_layout3 = [
    [sg.Text('BOTONES')],
    [sg.Button('REALIZAR REGRESION')]
]
# Definir el diseño de la ventana con las columnas
layout = [
    [sg.Text('Ventana con Columnas')],
    [sg.Column(column_layout1, key='-COL1-'), sg.Column(column_layout2, key='-COL2-'), sg.Column(column_layout3, key='-COL3-')],
    [sg.Button('Aceptar'), sg.Button('Cancelar')]
]

window = sg.Window('Ventana con Columnas', layout, resizable=True)


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Cancelar':
        break
    elif event == 'Aceptar':
        window.extend_layout(window['-COL1-'], [create_row(0)])
        window.extend_layout(window['-COL2-'], [create_row(1)])

    elif event == 'Enviar':
        sg.popup(f'Texto ingresado: {values["-INPUT-"]}')

window.close()


'''
# Agregar datos al diseño de la primera columna
for i, columna in enumerate(df.columns):
    checkbox = sg.Checkbox(columna, key=f'-CHECKBOX{i}-')
    column_layout1.append([checkbox])

'''