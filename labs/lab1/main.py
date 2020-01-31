import json
import ast
import glob
import pandas as pd

# Saves data from dictionary/list into json file
def save_file(filepath, data):
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=2)

# reads json formatted data from text file
# NOTE: DO NOT LOAD JSON FILE WITH THIS FUNCTION
def read_txt_file(filepath):
    with open(filepath,'r') as file:
        text_data = "".join(file.read().splitlines())
        json_data = ast.literal_eval(text_data)
    return json_data

# reads json formatted data from json file
def read_json_file(filepath):
    with open(filepath,'r') as file:
        json_data = json.load(file)
    return json_data

def chemas_a_hoe():
    files = glob.glob("data/train/*.txt")
    for f in files:
        data = read_txt_file(f)
        action = data['type']
        seq = [{**s['data'], **{'time': s['time']}} for s in data['seq']]
        df = pd.DataFrame(seq)
        print(action)
        print("x=%d, y=%d, z=%d" % (df['xAccl'].std(), df['yAccl'].std(),df['zAccl'].std()))





if __name__ == "__main__":
    chemas_a_hoe()
    