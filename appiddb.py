from os import getcwd
from os.path import isfile
from operator import itemgetter
from handlerequests import get_gameslist
from sys import setrecursionlimit
import pickle, trie

# def check_valid_user_input(appid=None, name):
#     assert((appid != None) or (name != None)), 'The appid and name was empty!'
    
# def get_id_and_name(appid=None, name=None):
#     try:
#         check_valid_user_input(appid, name)
#     except AssertionError as error:
#         print(error)
#         print('Please enter a valid appid OR name!')
#         check_valid_user_input(appid, name)    

def get_tuples_from_games(gamesdict: dict):
    gamelist = list(gamesdict.get('applist').get('apps'))

    tuple_list = []
    for game in gamelist:
        title = game['name']
        appid = int(game['appid'])

        cur_tuple = (title, appid)
        tuple_list.append(cur_tuple)

    sorted_tuple_list = sorted(tuple_list, key=itemgetter(0))       # sort the list alphabetically (based on title)
    print('There are' , len(sorted_tuple_list), 'applications/games in the database.')
    return sorted_tuple_list

if __name__ == '__main__':
    main()

def main():
    urldb = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
    cwpath = getcwd() + '/'
    filename = cwpath + 'appiddump/'
    db_filename = filename + 'Steam_game_db'

    if isfile(db_filename):                                             # check if we can load the local Steam app database                      
        print("the local database " + db_filename + " exists!")

        # load a local copy of the Trie database
        f = open(db_filename, 'rb')
        root_trie = pickle.load(f)                                      
        f.close()
    else:
        print("the local database " + db_filename + " DOESNT EXIST!")

        json_dict = get_gameslist(urldb, filename)                      # send a GET request to Steam and get its response
        sorted_games_tuple_list = get_tuples_from_games(json_dict)      # convert the dict to a list of tuples and sort by name alphabetically
        root_trie = trie.build_trie_from_games(sorted_games_tuple_list) # insert each tuple to make a Trie (gives us searchable prefixes)

        # store (dump) the new Trie database locally
        f = open(db_filename, 'wb')
        setrecursionlimit(3000)
        pickle.dump(root_trie, f)
        f.close()

    return root_trie
    # search the Trie by application title, and return its appid.

    # search_results = trie.search_trie(root_trie, title)
    # print(search_results)