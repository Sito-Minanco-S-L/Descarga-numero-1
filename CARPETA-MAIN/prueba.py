import statsmodels.api as sm
import PySimpleGUI as sg
from sklearn.model_selection import train_test_split
import regression
import files
from modelo import Modelo, cargar_modelo, realizar_predicción
from regression import *

modelo = cargar_modelo('Modelo.pickle')

def interface():
    layout=[[sg.Button('Realizar Predicción', size=(20, 2), button_color=('white', 'grey'), visible=True,enable_events=True)],
            [sg.Frame('', [], key='-jaja-')]]
    window = sg.Window('Aplicación de Regresión', layout, finalize=True, resizable= False)
    while True:
        event, values = window.read()

        if event == 'Realizar Predicción':
            window.extend_layout(window['-jaja-'], [[sg.Text(modelo.nombres_columnas())],[sg.Input('',size=(30,5), key='-valores-pred-')], [sg.Button('Submit')]])
            event, values = window.read()
            
            if event == 'Submit':
                realizar_predicción(modelo,values['-valores-pred-'])




interface()