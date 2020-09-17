


import PySimpleGUI as sg

sg.theme('DarkAmber')

statustext = sg.Text(key='-OUTPUT-', text='Waiting on you below...', text_color='white', size=(50, 2))

layout =    \
    [
        [sg.Text('Status:'), statustext],
        [sg.Input(key='-IN-')],
        [sg.Button('Show', auto_size_button=True), sg.Button('Exit', auto_size_button=True)]
    ]

window = sg.Window('Steam appid sample GUI', layout, size=(1600, 800), auto_size_text=True, auto_size_buttons=True)

while True:  # Event Loop
    event, values = window.read()
    # print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        # window['-OUTPUT-'].update(values['-IN-'])
        game_title = str(values['-IN-'])

        if game_title in ('', len(game_title) <= 0):

            status_row = layout[0]
            status_text_ind = status_row[1]
            status_raw = 'Error - you entered nothing. \n Please type the game/application in the box below.'
  


            window['-OUTPUT-'].update(statustext.update(value=status_raw, text_color='red'))
        


window.close()





