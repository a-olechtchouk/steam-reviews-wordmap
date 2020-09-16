from os import getcwd
from operator import itemgetter
import trie

def check_valid_user_input(appid, name):
    assert((appid != None) or (name != None)), 'The appid and name was empty!'
    
def get_id_and_name(appid=None, name=None):
    try:
        check_valid_user_input(appid, name)
    except AssertionError as error:
        print(error)
        print('Please enter a valid appid OR name!')
        check_valid_user_input(appid, name)    

def get_tuples_from_games(gamesdict: dict):
    gamelist = list(gamesdict.get('applist').get('apps'))

    tuple_list = []
    for game in gamelist:
        title = game['name']
        appid = int(game['appid'])

        cur_tuple = (title, appid)
        tuple_list.append(cur_tuple)

    sorted_tuple_list = sorted(tuple_list, key=itemgetter(0))   # sort the list alphabetically (based on title)
    print('There are' , len(sorted_tuple_list), 'applications/games in the database.')
    return sorted_tuple_list

urldb = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
cwpath = getcwd() + '/'
filename = cwpath + 'appiddump/'

database = trie.get_game_database(filename)     # fetch or load the local Steam app database

# search the Trie by application title, and return its appid.
search_results = trie.search_trie(database, 'Squad')