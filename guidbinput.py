


import PySimpleGUI as sg
from trie import search_trie
from appiddb import main

sg.theme('DarkAmber')

statustext = sg.Text(key='-OUTPUT-', text='Enter Steam game/app..', text_color='white', size=(50, 2), font=('', 30))
outputtext = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT1-', font=('', 30))
outputtext2 = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT2-', font=('', 30))
outputtext3 = sg.Text('', size=(50, 1), visible=False, key='-OUTPUT3-', font=('', 30))
layout =    \
    [
        [sg.Text('Status:', font=('', 30), size=(8, 2)), statustext],
        [sg.Input(key='-IN-')],
        [sg.Button('Show', auto_size_button=True), sg.Button('Exit', auto_size_button=True)],
        [outputtext, outputtext2, outputtext3]
    ]

window = sg.Window('Steam appid sample GUI', layout, size=(1600, 800), auto_size_text=True, auto_size_buttons=True)

root_trie = main()

while True:  # Event Loop
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        game_title = str(values['-IN-'])

        if game_title in ('', len(game_title) <= 0):
            status_raw = 'Error - you entered nothing.\nPlease type the game/application in the box below.'
            window['-OUTPUT-'].update(statustext.update(value=status_raw, text_color='red'))
        else:
            status_raw = 'Searching...'
            window['-OUTPUT-'].update(statustext.update(value=status_raw, text_color='yellow'))

            search_results = search_trie(root_trie, game_title)

            if len(search_results) <= 0:
                status_raw = 'Error - no results. \n Try typing the name of a different game/application.'
                window['-OUTPUT-'].update(statustext.update(value=status_raw, text_color='red'))
            else:
                status_raw = 'Ready!'
                window['-OUTPUT-'].update(statustext.update(value=status_raw, text_color='lime'))

                first_result = search_results[0]
                result = 'This was the first result:\n'
                result2 = first_result + '\n'
                result3 = 'Is this correct?'
                window['-OUTPUT1-'].update(outputtext.update(value=result, text_color='pink', visible=True))
                window['-OUTPUT2-'].update(outputtext2.update(value=result2, text_color='cyan', visible=True))
                window['-OUTPUT3-'].update(outputtext3.update(value=result3, text_color='pink', visible=True))

window.close()



# Update the "output" text element to be the value of "input" element
# window['-OUTPUT-'].update(values['-IN-'])




