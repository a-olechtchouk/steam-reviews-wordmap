import inout, errorchecking, inout
import requests, os.path, re
import errorchecking as err
import textprocessing as tp
from requests import Response
import simplejson as json

import time
import trie

from operator import itemgetter, attrgetter

def check_valid_user_input(appid, name):
    assert((appid != None) or (name != None)), 'The appid and name was empty!'

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

def search_trie(root: trie.Node, prefix: str):
    return

def build_trie_from_games(games: list):

    root_trie = trie.Node()

    for game in games:
        game = tuple(game)
        trie.insert(root_trie, game[0], game[1])
    

    search_results = trie.keys_with_prefix(root_trie, 'Squa')
    print(search_results)
    return search_results


def get_id_and_name(appid=None, name=None):

    # if (appid==None) and (name==None):
    try:
        check_valid_user_input(appid, name)
    except AssertionError as error:
        print(error)
        print('Please enter a valid appid OR name!')
        check_valid_user_input(appid, name)

# Send a GET request to Steam if the game database doesn't exist
def get_gameslist(url, filename):

    filename += 'steamgamelistraw'

    if os.path.isfile(filename):                        # the file exists, so load local query data
        print("the local query " + filename + " exists!")
        json_dict = inout.rw_json(filename, 'r') 

    else:                                               # its not cached locally, so query Steam
        print("the local query " + filename + " does NOT exist!")

        r = requests.get(urldb, timeout=(3.05, 27))     # send a GET request,

        if r.status_code != 200: return False           # ensure response status code is 200 
        if r.text == '{"response":{}}': return False    # ensure the (JSON-encoded) response list isnt empty

        print(r.text)

        # validate the response we got
        json_dict = r.json()  

        # it was valid, so write the query to a file locally
        inout.rw_json(filename, 'w', json_dict=json_dict)   
    return json_dict


urldb = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
cwpath = os.getcwd() + '/'
filename = cwpath + 'appiddump/'

# get the dictionary containing all Steam {appid, name} application pairings
json_dict = get_gameslist(urldb, filename)

# get the list of tuples (name, appid) for all Steam applications (sorted alphabetically by name)
sorted_games_tuple_list = get_tuples_from_games(json_dict)

# build a Trie data structure from the sorted tuples that allows searchable prefixes
trie_ds = build_trie_from_games(sorted_games_tuple_list)