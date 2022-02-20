import time
import requests
import json


def filtr(fields_list):
    temp_data = {}
    for i in range(len(fields_list)):
        field= fields_list[i]
        with open('content_filtr.json', 'r') as f:
            data = json.load(f)
            temp_data[f'{field}'] = data[f'{field}']
    print(f'{temp_data}' + "\n")
    data_j = json.dumps(temp_data)
    return data_j

while True:
    with open('config.json', 'r') as f:
        config = json.load(f)

    address_get = config['ad_1']
    f_n = config['f_n']
    address_post = config['ad_2']
    fields_list = f_n.split(',')
    data = (requests.get(f'{address_get}')).json()
    with open('content_filtr.json', 'w') as f:
        json.dump(data, f)
    filtred_data = filtr(fields_list)
    requests.post(f'{address_post}', filtred_data )
    time.sleep(1)

