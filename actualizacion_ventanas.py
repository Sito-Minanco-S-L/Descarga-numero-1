import PySimpleGUI as sg
'''
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
    [sg.Column(column_layout1, key='-COL1-'), sg.Column(column_layout2, key='-COL2-'), sg.Column(column_layout3, key='-COL2-')],
    [sg.Button('Aceptar'), sg.Button('Cancelar')]
]

window = sg.Window('Ventana con Columnas', layout, resizable=True)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Cancelar':
        break
    elif event == 'Aceptar':
        sg.popup('Botón Aceptar presionado')
    elif event == 'Enviar':
        sg.popup(f'Texto ingresado: {values["-INPUT-"]}')

window.close()
