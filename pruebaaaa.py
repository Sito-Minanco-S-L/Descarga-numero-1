import PySimpleGUI as sg

def main():
    # Definir el diseño inicial de la interfaz
    layout = [[sg.Button('Botón', key='-BOTON-')]]

    # Crear la ventana
    window = sg.Window('Ejemplo PySimpleGUI', layout, resizable=True)

    # Bucle principal de eventos
    while True:
        event, values = window.read()

        # Salir del bucle si se cierra la ventana
        if event == sg.WIN_CLOSED:
            break

        # Si se hace clic en el botón, agregar otro botón
        if event == '-BOTON-':
            new_button_key = f'-BOTON-{len(layout[0])+1}-'
            layout[0].append(sg.Button('Botón', key=new_button_key))
            window.close()
            window = sg.Window('Ejemplo PySimpleGUI', layout, resizable=True)

    # Cerrar la ventana y salir del programa
    window.close()

if __name__ == '__main__':
    main()
