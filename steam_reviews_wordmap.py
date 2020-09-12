import re, string
from funcmodule import *

steamwords = ['game', 'good', 'great', 'lot', 'youre', 'your', 'fun', 'play', 'dont', 'ive'] # the list of steam words are being updated as time goes on
removedwords = stopwords + steamwords    

def process_multiple_queries(url, appid, payload, iters):

    total_processed = 0
    key_words = []

    for x in range(iters):

        prev_cursor = query.get('cursor')

        query = get_query_data(url, appid, payload)         # get query data, either locally or from Steam.\

        if prev_cursor == query.get('cursor'):
            break

        review_list = list(query.get('reviews'))            # specify only review information
        key_words += filter_key_words(review_list)          # get a list of 'key' words by filtering out the words from each review text

        num_reviews = query.get('query_summary').get('num_reviews')
        total_processed = total_processed + num_reviews
        payload['cursor'] = query.get('cursor')

        
    # IMPORTANT! MAKE SURE TO STOP GETTING REQ'S FOR THIS URL
    full_url = url + appid + '?json=1?'
    requests.get(full_url, timeout=1)

    print('processed a total of: ' + str(total_processed) + ' reviews.')
    return key_words

# filter the review text
def filter_key_words(reviews):
    key_words = []
    for x in reviews:
        rev_text = x.get('review').lower()                                          # set the text to lowercase,
        rev_text = rev_text.translate(str.maketrans('', '', string.punctuation))    # remove punctuation, 
        rev_text = re.findall(r"(?i)\b[a-z]+\b", rev_text)                          # keep english alphabet characters,
        rev_text = list(dict.fromkeys(rev_text))                                    # remove duplicate words,
        key_words += removeWords(rev_text, removedwords)                            # remove specific words (common to Steam and stopwords)
    return key_words


# set-up the initial url and payload
appid = str(393380)
url = 'http://store.steampowered.com/appreviews/'
payload = {'filter': 'recent', 'language': 'english', 'day_range': '1', 'review_type': 'all', 'purchase_type': 'all', 'num_per_page': '100'}

num_total_requests = int(34000 / 100)


key_words = process_multiple_queries(url, appid, payload, num_total_requests)

text = ' '.join(key_words)                          # finally convert the list of filtered words into one long string

createWordCloud(text)                               # create and display a wordcloud