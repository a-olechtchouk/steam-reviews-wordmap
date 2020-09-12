import re, string
from funcmodule import *

 # set-up the initial url and payload
url = 'http://store.steampowered.com/appreviews/393380?json=1?'
payload = {'filter': 'recent', 'language': 'english', 'day_range': '1', 'review_type': 'all', 'purchase_type': 'all', 'num_per_page': '20'}

# query Steam to get information about all reviews and users
query = form_and_send_query(url, payload, "*")

# get a list of everything about all reviews
review_list = list(query.get('reviews'))

# get a list of 'key' words from each review text
key_words = []
for x in review_list:

    rev_text = x.get('review').lower()                                      # filter the review text by setting each sentence to lowercase,
    rev_text = rev_text.translate(str.maketrans('', '', string.punctuation))# removing punctuation, 
    rev_text = re.findall(r"(?i)\b[a-z]+\b", rev_text)                      # keeping only english alphabet characters,
    rev_text = list(dict.fromkeys(rev_text))                                # removing duplicate words,

    key_words += removeStopwords(rev_text, stopwords)                       # and removing stopwords



# finally convert the list of filtered words into one long string
text = ' '.join(key_words)

# create and display a wordcloud
createWordCloud(text)



# write all text reviews to file
# f = open('workfile', 'w')
# write_reviews_to_file('testout.txt', key_words)
