import time
import requests
import pandas as pd
import json

i = 0
df = pd.read_csv("termometr2.csv", sep=",")


def HTTP(url, frequency):
    global i
    json_data = json.loads(df.iloc[i].to_json())
    print(json_data)
    requests.post(url, json=json_data)
    time.sleep(frequency)


for i in range(len(df)):
    app_nr = "app1"
    with open('config2.json', 'r') as f:
        config = json.load(f)
        status = config['s_2']
        frequency = int(config['fq'])
        url = config['url']
    if str(status) == str(1):
        HTTP(url, frequency)
    elif str(status) == str(0):
        time.sleep(0.5)
