from json import load, dump

# read and write JSON-formatted files
def rw_json(name, mode, json_form=None):

    f = open(name, mode)

    if mode == 'r': json_form = load(f)
    if mode == 'w': dump(json_form, f)

    f.close()
    return json_form


#  read and write text files
def rw_txt(name, mode, text=None):

    f = open(name, mode)

    if mode == 'r': text = f.read(text)
    if mode == 'w': f.write(text)
    
    f.close()
    return text


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