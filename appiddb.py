import inout, errorchecking, inout
import requests, os.path, re
import errorchecking as err
import textprocessing as tp
from requests import Response
import simplejson as json

import time

def process_gameslist(json_dict: dict):

    applist = json_dict['applist']
    print(applist)

def get_gameslist(url, filename):

    filename += 'steamgamelist'

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
process_gameslist(json_dict)