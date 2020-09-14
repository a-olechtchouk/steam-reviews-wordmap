import matplotlib.pyplot as plt
import numpy as np
import requests, re, string, json, os.path
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image

def get_string_from_params(payload, appid):

    p_curs = payload.get('cursor')   
    if p_curs == '*':
        p_curs = 'a'
    else:
        p_curs = re.sub('[/]', '', p_curs)

    return p_curs

# use a local copy of the requested query if it exists.
# otherwise, form the query, send it, and write the json response to a file.
def get_query_data(url, appid, payload):

    filename = get_string_from_params(payload, appid)

    if os.path.isfile(filename) is True:    # the file exists, so use the local query data instead.
        print("the local query " + filename + " exists!")
        f = open(filename, 'r')
        json_form = json.load(f)
        f.close()
        
    else:                                   # otherwise, query Steam and write that data locally.
        print("the local query " + filename + " does NOT exist!")

        full_url = url + appid + '?json=1?'

        # send the request to Steam, check its response, and write the data to a file.
        r = requests.get(full_url, params=payload)

        if r.text == '{"response":{}}':
            return -1

        check_assertions(r.status_code, 'init_stat_code')

        json_form = r.json()

        check_assertions(json_form.get('success'), 'query_success')

        
        f = open(filename, 'w')
        json.dump(json_form, f)
        f.close()

    return json_form