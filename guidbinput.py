


import PySimpleGUI as sg
from trie import search_trie, find
from appiddb import main

sg.theme('DarkAmber')

statustext = sg.Text(key='-OUTPUT-', text='Enter Steam game/app..', text_color='white', size=(50, 2), font=('', 30))

outputtext = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT1-', font=('', 28))
outputtext2 = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT2-', font=('', 28))
outputtext3 = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT3-', font=('', 28))
outputtext4 = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT4-', font=('', 28))
outputtext5 = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT5-', font=('', 28))

acceptbutton = sg.Button('Yes', key='_BUTTON_KEY0_', auto_size_button=True, visible=False)
denybutton = sg.Button('No', key='_BUTTON_KEY1_', auto_size_button=True, visible=False)

alt_results_text = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT6-', font=('', 28))
alt_results_out = sg.Text('', size=(50, 2), visible=False, key='-OUTPUT7-', font=('', 28))

layout =    \
    [
        [sg.Text('Status:', font=('', 30), size=(8, 2)), statustext],
        [sg.Input(key='-IN-')],
        [sg.Button('Show', auto_size_button=True), sg.Button('Exit', auto_size_button=True)],
        [outputtext, outputtext2, outputtext3, outputtext4, outputtext5],
        [acceptbutton, denybutton],
        [alt_results_text, alt_results_out]
    ]

window = sg.Window('Steam appid sample GUI', layout, size=(1800, 1000), auto_size_text=True, auto_size_buttons=True)

root_trie = main()

gameappid = 0
alt_res = []
appid_located = False

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
                alt_res = search_results[1:]
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
        appid_located = True
        break
    if event == '_BUTTON_KEY1_':
        res_str = 'These were the other titles found:'
        window['-OUTPUT6-'].update(alt_results_text.update(value=res_str, text_color='pink', visible=True))
        window['-OUTPUT7-'].update(alt_results_out.update(value=str(alt_res), text_color='cyan', visible=True))

window.close()

# ------ Menu Definition ------ #
filter_def = ['&Filter', ['recent', 'updated', 'all']]

lang_def = ['&Language',
    ['Arabic', 'Bulgarian', 'Chinese (Simplified)', 'Chinese (Traditional)', 
    'Czech', 'Danish', 'Dutch', 'English', 'Finnish', 'French', 'German',
    'Greek', 'Hungarian', 'Italian', 'Japanese', 'Korean', 'Norwegian', 
    'Polish', 'Portuguese', 'Portuguese-Brazil', 'Romanian', 'Russian', 'Spanish-Spain',
    'Spanish-Latin America', 'Swedish', 'Thai', 'Turkish', 'Ukrainian', 'Vietnamese']]

rev_def = ['&Revivew type', ['all', 'positive', 'negative']]

purch_def = ['&Purchase type', ['all', 'non_steam_purchase', 'steam']]

layout2 = \
    [
        [sg.Button('Exit', auto_size_button=True)],
        [sg.ButtonMenu('Filter:', filter_def, key='-IN1-')],
        [sg.ButtonMenu('Language:', lang_def, key='-IN2-')],
        [sg.ButtonMenu('Revivew type:', rev_def, key='-IN3-')],
        [sg.ButtonMenu('Purchase type:', purch_def, key='-IN4-')]
    ]

window2 = sg.Window('Create a Word Cloud', layout2, size=(1800, 1000), auto_size_text=True, auto_size_buttons=True)

filter_chosen = ''
lang_chosen = ''
rev_chosen = ''
purch_def = ''

button_clicks = {'-IN1-': None, '-IN2-': None, '-IN3-': None, '-IN4-': None}

while True:  # Event Loop
    event, values = window2.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        print(button_clicks)
        break

    if event in ('-IN1-', '-IN2-', '-IN3-', '-IN4-'):
        button_clicks[event] = values[event]



from steam_reviews_wordmap import main_func
# if appid_located:
    # main_func(gameappid)

    # https://store.steampowered.com/api/appdetails?appids=57690


# Update the "output" text element to be the value of "input" element
# window['-OUTPUT-'].update(values['-IN-'])




