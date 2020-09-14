import re, string
from funcmodule import *
import funcmodule as 
from datetime import datetime

def process_multiple_queries(url, appid, payload, iters):

    total_processed = 0
    key_words = []
    prev_cursor = ''

    for x in range(iters):

        query = get_query_data(url, appid, payload)         # get query data, either locally or from Steam.\

        print(('query_summary is : ') + str(query.get('query_summary')))

        payload['cursor'] = query.get('cursor')

        if check_empty_query_response(query, prev_cursor):
            break

        review_list = list(query.get('reviews'))            # specify only review information
        key_words += filter_key_words(review_list)          # get a list of 'key' words by filtering out the words from each review text

        num_reviews = query.get('query_summary').get('num_reviews')
        total_processed = total_processed + num_reviews
        prev_cursor = query.get('cursor')
   
    # IMPORTANT! MAKE SURE TO STOP GETTING REQ'S FOR THIS URL
    # full_url = url + appid + '?json=1?'
    # requests.get(full_url, timeout=0.001)

    print('processed a total of: ' + str(total_processed) + ' reviews.')
    return key_words






# set-up the initial url and payload
appid = str(393380)
url = 'http://store.steampowered.com/appreviews/'
payload = {'filter': "recent", 'language': "english", 'cursor': "*", 'day_range': "3650", 'review_type': "all", 'purchase_type': "all", 'num_per_page': "100"}

num_total_requests = int(40000 / 100)

key_words = process_multiple_queries(url, appid, payload, num_total_requests)

text = ' '.join(key_words)                          # finally convert the list of filtered words into one long string

# save the final string of words to a textfile
f2 = open('output.txt', 'w')
f2.write(text)
f2.close()

createWordCloud(text)                               # create and display a wordcloud