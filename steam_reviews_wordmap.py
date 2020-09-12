import re, string
from funcmodule import *

steamwords = ['game', 'good', 'great', 'lot', 'youre', 'your'] # the list of steam words are being updated as time goes on
removedwords = stopwords + steamwords    

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
url = 'http://store.steampowered.com/appreviews/393380?json=1?'
payload = {'filter': 'recent', 'language': 'english', 'day_range': '1', 'review_type': 'all', 'purchase_type': 'all', 'num_per_page': '20'}

query = form_and_send_query(url, payload, "*")      # query Steam to get information about all reviews and users

review_list = list(query.get('reviews'))            # specify only review information

key_words = filter_key_words(review_list)           # get a list of 'key' words by filtering out the words from each review text

text = ' '.join(key_words)                          # finally convert the list of filtered words into one long string

createWordCloud(text)                               # create and display a wordcloud