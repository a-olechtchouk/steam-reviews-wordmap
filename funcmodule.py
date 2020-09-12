stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']

import matplotlib.pyplot as plt
import requests, re, string, json, os.path
from wordcloud import WordCloud

def get_string_from_params(payload, appid):

    # filter can be r (recent) u (updated) or a (all). 
    # language is a minimum of 3 characters to store 'all'
    p_filt_lan  = payload.get('filter')[0] + payload.get('language')[0:3]

    p_curs = payload.get('cursor')   
    if p_curs == '*':
        p_curs = 'a'

    # day_range and cursor (unless the cursor is asterisk "*") are directly from the payload
    p_rnge_curs = payload.get('day_range') + p_curs

    # review_type can be a (all) p (positive) or n (negative). 
    # purchase_type can be a (all) n (non_steam_purchase) or s (steam)
    # num_per_page is directly from the payload
    p_types_num = payload.get('review_type')[0] +  payload.get('purchase_type')[0] +  payload.get('num_per_page') 


    return p_filt_lan + p_rnge_curs + p_types_num + appid

# use a local copy of the requested query if it exists.
# otherwise, form the query, send it, and write the json response to a file.
def get_query_data(url, appid, payload, cursor="*"):
    payload['cursor'] = cursor

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

        check_assertions(r.status_code, 'init_stat_code')

        json_form = r.json()

        check_assertions(json_form.get('success'), 'query_success')
        
        f = open(filename, 'w')
        json.dump(json_form, f)
        f.close()

    print_query_response_info(json_form)
    return json_form

# get and print basic info for debugging
def print_query_response_info(json_form):

    cursor_ret = json_form.get('cursor')
    summary_ret = json_form.get('query_summary')

    print(cursor_ret)
    print(summary_ret) 

def createWordCloud(text):
    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # Display the generated image the matplotlib way:
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('wordmap.svg', dpi=600)
    plt.show()

def removeWords(wordlist, removedwords):
    return [w for w in wordlist if w not in removedwords]


def check_assertions(assertion_value, assertion_type):

    if __debug__:
    
        if assertion_type == 'init_stat_code':
            if not assertion_value == 200: raise AssertionError

        elif assertion_type == 'query_success': 
            if not assertion_value == 1: raise AssertionError

def print_simple_review(review):

    author_stats = review.get('author')

    total_hours = author_stats.get('playtime_forever')
    rev_text = review.get('review')

    print('Total hours played: ' + str(total_hours))
    print('Full review: ' + str(rev_text))