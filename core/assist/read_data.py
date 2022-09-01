import os
import json
import pandas as pd

### core.json
# get token
def get_token():
    with open(os.getcwd() + '/core/assist/config/core.json', 'r', encoding='utf-8')as f:
        return json.load(f)["token"]

# get information
def load_information(key):
    with open(os.getcwd() + '/core/assist/config/core.json', 'r', encoding='utf8')as f:
        return json.load(f)[key]


### data.json
# get mapper from str to emoji
def load_str2emoji(index, key):
    with open(os.getcwd() + '/core/assist/config/data.json', 'r', encoding='utf8')as f:
        json_data = json.load(f)
    return json_data["str_2_emoji"][index][key]

def load_tarrow(index, num):
    with open(os.getcwd() + '/core/assist/config/data.json', 'r', encoding='utf8')as f:
        json_data = json.load(f)
    return json_data["tarrow"][index][str(num)]


### help.txt
# get help
def load_help():
    with open(os.getcwd() + '/core/assist/config/help.txt', 'r', encoding='utf-8')as f:
        data = f.readlines()
    return data

### horse.csv
# get horse data
def load_horse():
    return pd.read_csv(os.getcwd() + '/core/assist/config/horse.csv')
    