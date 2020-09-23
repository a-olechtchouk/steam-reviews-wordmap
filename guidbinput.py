


import PySimpleGUI as sg
from trie import search_trie, find
from appiddb import main

sg.theme('DarkAmber')

statustext = sg.Text(key='-OUTPUT-', text='Enter Steam game/app..', text_color='white', size=(50, 2), font=('', 30))
outputtext = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT1-', font=('', 30))
outputtext2 = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT2-', font=('', 30))
outputtext3 = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT3-', font=('', 30))
outputtext4 = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT4-', font=('', 30))
outputtext5 = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT5-', font=('', 30))
acceptbutton = sg.Button('Yes', key='_BUTTON_KEY0_', auto_size_button=True, visible=False)
denybutton = sg.Button('No', key='_BUTTON_KEY1_', auto_size_button=True, visible=False)
layout =    \
    [
        [sg.Text('Status:', font=('', 30), size=(8, 2)), statustext],
        [sg.Input(key='-IN-')],
        [sg.Button('Show', auto_size_button=True), sg.Button('Exit', auto_size_button=True)],
        [outputtext, outputtext2, outputtext3, outputtext4, outputtext5],
        [acceptbutton, denybutton]
    ]

window = sg.Window('Steam appid sample GUI', layout, size=(1600, 800), auto_size_text=True, auto_size_buttons=True)

root_trie = main()

gameappid = 0

def gen_wordcloud_from_appid(appid):
    return 'yo'


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
                result3 = 'It has appid:\n'
                gameappid = find(root_trie, first_result)
                result4 = str(gameappid) + '\n'
                result5 = 'Is this correct?'
                window['-OUTPUT1-'].update(outputtext.update(value=result, text_color='pink', visible=True))
                window['-OUTPUT2-'].update(outputtext2.update(value=result2, text_color='cyan', visible=True))
                window['-OUTPUT3-'].update(outputtext3.update(value=result3, text_color='pink', visible=True))
                window['-OUTPUT4-'].update(outputtext4.update(value=result4, text_color='cyan', visible=True))
                window['-OUTPUT5-'].update(outputtext5.update(value=result5, text_color='pink', visible=True))
                window['_BUTTON_KEY0_'].update(acceptbutton.update(visible=True))
                window['_BUTTON_KEY1_'].update(denybutton.update(visible=True))
    if event == '_BUTTON_KEY0_':
        break
    if event == '_BUTTON_KEY1_':
        break

window.close()

from steam_reviews_wordmap import main_func
main_func(gameappid)


# Update the "output" text element to be the value of "input" element
# window['-OUTPUT-'].update(values['-IN-'])




