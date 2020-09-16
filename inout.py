from json import load, dump

# read and write JSON-formatted files
def rw_json(name, mode, json_dict=None):
    f = open(name, mode)
    if mode == 'r': json_dict = load(f)
    if mode == 'w': dump(json_dict, f)
    f.close()
    return json_dict

#  read and write text files
def rw_txt(name, mode, text=None):
    f = open(name, mode)
    if mode == 'r': text = f.read(text)
    if mode == 'w': f.write(text)
    f.close()
    return text