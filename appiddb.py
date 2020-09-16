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

    print('There are' , len(tuple_list), 'applications/games in the database.')
    sorted_tuple_list = sorted(tuple_list, key=itemgetter(0))

    return sorted_tuple_list

def build_trie_from_games(gamesdict: dict):

    gamelist = list(gamesdict.get('applist').get('apps'))
    print(gamelist[5])

    sorted_gamelist = sorted(gamelist, key=attrgetter('name'))
    print(sorted_gamelist[5])
    

    # parent trie
    # root_trie = trie.Node()
    # for game in gamelist:

    #     trie.insert

    # return root_trie


def get_id_and_name(appid=None, name=None):

    # if (appid==None) and (name==None):
    try:
        check_valid_user_input(appid, name)
    except AssertionError as error:
        print(error)
        print('Please enter a valid appid OR name!')
        check_valid_user_input(appid, name)

# get the dictionary of all {appid, name} pairings for apps from Steam.
# if the local query response exists load it, otherwise send 1 request to Steam and store it.
def get_gameslist(url, filename):

    filename += 'steamgamelistraw'

    if os.path.isfile(filename):                    # the file exists, so load local query data
        print("the local query " + filename + " exists!")
        json_dict = inout.rw_json(filename, 'r') 

    else:                                           # its not cached locally, so query Steam
        print("the local query " + filename + " does NOT exist!")

        r = requests.get(urldb, timeout=(3.05, 27))  # send a GET request,

        if r.status_code != 200: return False            # ensure response status code is 200 
        if r.text == '{"response":{}}': return False     # ensure the (JSON-encoded) response list isnt empty

        # print(r.text)

        # validate the response we got
        json_dict = r.json()  

        # print(json_dict)

        # it was valid, so write the query to a file locally
        inout.rw_json(filename, 'w', json_dict=json_dict)   
    return json_dict


urldb = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'

# query_json = query(url=urldb)
cwpath = os.getcwd() + '/'
filename = cwpath + 'appiddump/'
json_dict = get_gameslist(urldb, filename)

sorted_games_tuple_list = get_tuples_from_games(json_dict)
# build_trie_from_games(json_dict)

# get_id_and_name(appid=None, name='g')




        # if appid: return game[appid]
        # if name: return game[name]

        # if game['name'] == 'Squad': print(game)


    # next(item for item in dicts if item["name"] == "Pam")