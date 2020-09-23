# TODO: will add functionality to query game name searches, after which 
#       i could get the appid and do a search for the title something like that...
#       and there'd be a better way to save the files... per game... modularity
#       

# use a local copy of the requested query if it exists.
# otherwise, form the query, send it, and write the json response to a file.
from os import getcwd
from os.path import isfile
from inout import rw_json
from errorchecking import is_query_response_valid
from textprocessing import get_string_from_params
import requests

def get_check_query(url, appid, payload):
    cwpath = getcwd() + '/'
    filename = cwpath + 'GUI_CACHE_TEST/' + get_string_from_params(payload, appid)

    if isfile(filename):                    # the file exists, so load local query data
        print("the local query " + filename + " exists!")
        json_dict = rw_json(filename, 'r') 
 
    else:                                           # its not cached locally, so query Steam
        print("the local query " + filename + " does NOT exist!")

        full_url = url + appid + '?json=1?'         # form the complete URL,
        r = requests.get(full_url, params=payload, timeout=(3.05, 27))  # send a GET request,

        # validate the response we got
        json_dict = is_query_response_valid(r)
        if json_dict is False: return False

        # it was valid, so write the query to a file locally
        rw_json(filename, 'w', json_dict=json_dict)   
    
    return json_dict


# Send a GET request to Steam if the game database doesn't exist, otherwise load it locally.
def get_gameslist(url, filename):
    filename += 'steamgamelistraw'

    if isfile(filename):                        # the file exists, so load local query data
        print("the local query " + filename + " exists!")
        json_dict = rw_json(filename, 'r') 

    else:                                               # its not cached locally, so query Steam
        print("the local query " + filename + " does NOT exist!")

        urldb = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
        
        r = requests.get(urldb, timeout=(3.05, 27))     # send a GET request,

        if r.status_code != 200: return False           # ensure response status code is 200 
        if r.text == '{"response":{}}': return False    # ensure the (JSON-encoded) response list isnt empty

        json_dict = r.json()  

        rw_json(filename, 'w', json_dict)         # write the query to a file locally   
    return json_dict