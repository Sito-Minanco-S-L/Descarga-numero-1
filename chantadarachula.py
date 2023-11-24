'''import PySimpleGUI as sg
import random, string

# ------ Some functions to help generate data for the table ------
def word():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))
def number(max_val=1000):
    return random.randint(0, max_val)

def make_table(num_rows, num_cols):
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    data[0] = [word() for _ in range(num_cols)]
    for i in range(0, num_rows):
        data[i] = [i, word(), *[number() for i in range(num_cols - 1)]]
    return data


def main_example1():
    global edit

    edit = False
    # ------ Make the Table Data ------
    # sg.Print('Creating table...')
    data = make_table(num_rows=1_000, num_cols=6)
    # headings = [str(data[0][x])+'     ..' for x in range(len(data[0]))]
    headings = [f'Col {col}' for col in range(len(data[0]))]
    # sg.Print('Done creating table.  Creating GUI...')
    sg.set_options(dpi_awareness=True)
    layout = [[sg.Table(values=data, headings=headings, max_col_width=25,
                        auto_size_columns=True,
                        # display_row_numbers=True,
                        justification='right',
                        num_rows=20,
                        alternating_row_color=sg.theme_button_color()[1],
                        key='-TABLE-',
                        # selected_row_colors='red on yellow',
                        # enable_events=True,
                        # select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True,
                        expand_y=True,
                        enable_click_events=True,  # Comment out to not enable header and other clicks
                        )],
              
              [sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')]]


    window = sg.Window('Table Element - Example 1', layout, resizable=True, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif isinstance(event, tuple):
            cell = row, col = event[2]
            window['-CLICKED-'].update(cell)
            

    window.close()

main_example1()'''



import PySimpleGUI as sg
import pandas as pd
import numpy as np
import random
import string

# ------ Some functions to help generate data for the table ------
def word():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))

def number(max_val=1000):
    return random.randint(0, max_val)

def make_table(num_rows, num_cols):
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    data[0] = [word() for _ in range(num_cols)]
    for i in range(0, num_rows):
        data[i] = [i, word(), *[number() for i in range(num_cols - 1)]]
    return data

def main_example1():
    global edit

    edit = False
    # ------ Make the Table Data ------
    data = make_table(num_rows=1_000, num_cols=6)
    headings = [f'Col {col}' for col in range(len(data[0]))]
    sg.set_options(dpi_awareness=True)

    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=headings)

    # Convert DataFrame to a list of lists
    table_data = df.to_numpy().tolist()

    layout = [
        [sg.Table(values=table_data, headings=headings, max_col_width=25,
                  auto_size_columns=True,
                  justification='right',
                  num_rows=20,
                  alternating_row_color=sg.theme_button_color()[1],
                  key='-TABLE-',
                  expand_x=True,
                  expand_y=True,
                  enable_click_events=True),
         ],
        [sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')],
    ]

    window = sg.Window('Table Element - Example 1', layout, resizable=True, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif isinstance(event, tuple):
            cell = row, col = event[2]
            window['-CLICKED-'].update(cell)

    window.close()

main_example1()