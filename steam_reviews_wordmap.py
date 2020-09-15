import requests, os.path, re
import errorchecking as err
import inout
import textprocessing as tp

cwpath = os.getcwd() + '/'

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

    filename = cwpath + 'testcache/' + get_string_from_params(payload, appid)

    if os.path.isfile(filename):                    # the file exists, so load local query data
        print("the local query " + filename + " exists!")
        json_dict = inout.rw_json(filename, 'r') 
 
    else:                                           # its not cached locally, so query Steam
        print("the local query " + filename + " does NOT exist!")

        full_url = url + appid + '?json=1?'         # form the complete URL,
        r = requests.get(full_url, params=payload)  # send a GET request,

        # validate the response we got
        json_dict = err.is_query_response_valid(r)
        if json_dict is False: return False

        # it was valid, so write the query to a file locally
        inout.rw_json(filename, 'w', json_dict=json_dict)   
    
    return json_dict


def process_multiple_queries(url, appid, payload, iters):

    total_processed = 0
    filtered_review_words = []
    prev_cursor = ''
    new_cursor = ''

    for x in range(iters):

        # get query GET response (json_dict) data, either locally or from Steam, and get its validity
        query = get_query_data(url, appid, payload)

        if query is False:                  # ensure the new query response is valid
            break

        new_cursor = query['cursor']
        if prev_cursor == new_cursor:       # ensure the new query cursor differs from the previous
            break

                                            # the response is new and valid, so update the 'cursor' for:
        payload['cursor'] = new_cursor      # - the next payload (next GET request)
        prev_cursor = new_cursor            # - the previous cursor


        review_list = list(query['reviews'])                        # get a list of reviews for this response
        filtered_review_words += tp.filter_review(review_list)      # filter out the words from each review


        # record how many reviews we recieved and add it to the total
        query_summary = query['query_summary']

        num_reviews = query_summary['num_reviews']
        total_processed = total_processed + num_reviews
        
        print(('query_summary is : ') + str(query.get('query_summary')))
   
    print('processed a total of: ' + str(total_processed) + ' reviews.')
    return filtered_review_words


# set-up the appid, initial url, and payload
appid = str(393380)
url = 'http://store.steampowered.com/appreviews/'
payload = {'filter': "recent", 'language': "english", 'cursor': "*",
 'day_range': "3650", 'review_type': "all", 'purchase_type': "all", 'num_per_page': "100"}

# we can recieve up to 100 reviews per request.
# since there are about 39,000 English reviews, we only need to send about 400 requests.
num_total_requests = int(40000 / 100)

# Process those 400 queries
filtered_review_words = process_multiple_queries(url, appid, payload, num_total_requests)

text = ' '.join(filtered_review_words)      # convert the list of filtered words into one long string

inout.rw_txt(cwpath + 'outputword.txt', 'w', text)   # save the final string of words to a textfile

mask_img = 'squadgradientbest10.png'
mask_path = cwpath + 'usedimgs/' + mask_img
produce_wordcloud(text, cwpath + 'testreqs/' + 'nicewordcloud', mask_path)  # create and save an image of the new wordcloud

# Create the wordcloud and save the image/s
def produce_wordcloud(text, name, mask_path):
    import matplotlib.pyplot as plt
    import numpy as np
    from wordcloud import WordCloud, ImageColorGenerator
    from PIL import Image

    # Init the wordcloud mask from an image
    mask = np.array(Image.open(mask_path))

    # Generate a word cloud from text, and bound it inside the mask contour outline
    wc = WordCloud(scale=1, stopwords=None, width=2560, height=1440,mask=mask, contour_width=4, contour_color='white')
    wc.generate(text)

    # Init the color function, so the wordcloud can use colors from the mask
    image_colors = ImageColorGenerator(mask)

    plt.figure(dpi=300)
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    
    # Save the image/s in various file formats (png, tiff, and jpg)
    plt.savefig(name + '.png')
    wc.to_file(name + '.png')
    wc.to_file(name + '.tiff')
    wc.to_file(name + '.jpg')