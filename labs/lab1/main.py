import json
import ast
from os import listdir
from os.path import isfile, join

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

# Given a path, returns a list of all the files in the path
def get_file_list(path):
    onlyfiles = [path + f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles

if __name__ == "__main__":
    file = "data/train/activity-team1-Driving-0.txt"
    data = read_txt_file(file)
    save_file("output.json",data)

    filepath = "data/train/"
    print(get_file_list(filepath))
