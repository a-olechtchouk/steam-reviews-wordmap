import requests, os.path, re
import errorchecking as err
import inout

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
    key_words = []
    prev_cursor = ''

    for x in range(iters):

        # get query GET response (json_dict) data, either locally or from Steam, and get its validity
        query = get_query_data(url, appid, payload)

        # ensure that its valid, and that it differs from the previous query response.
        # if not, break the loop and exit 
        if (query is False) or (prev_cursor == query['cursor']):
            break
        
        # the response is new and valid, so update the 'cursor' for the next payload (next GET request)
        payload['cursor'] = query['cursor']

        review_list = list(query.get('reviews'))            # specify only review information
        key_words += filter_key_words(review_list)          # get a list of 'key' words by filtering out the words from each review text

        num_reviews = query.get('query_summary').get('num_reviews')
        total_processed = total_processed + num_reviews
        prev_cursor = query.get('cursor')

        print(('query_summary is : ') + str(query.get('query_summary')))
   


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


# Create the wordcloud and save the image/s
def produce_wordcloud(mask_img, text, name):
    import matplotlib.pyplot as plt
    import numpy as np
    from wordcloud import WordCloud, ImageColorGenerator
    from PIL import Image

    # Init the wordcloud mask from an image
    mask = np.array(Image.open(mask_img + ".png"))

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









            # f = open(filename, 'r')
        # json_form = json.load(f)
        # f.close()


                # f = open(filename, 'w')
        # json.dump(json_form, f)
        # f.close()


        # import matplotlib.pyplot as plt
# import numpy as np
# import requests, re, string, json, os.path
# from wordcloud import WordCloud, ImageColorGenerator
# from PIL import Image



    # IMPORTANT! MAKE SURE TO STOP GETTING REQ'S FOR THIS URL
    # full_url = url + appid + '?json=1?'
    # requests.get(full_url, timeout=0.001)