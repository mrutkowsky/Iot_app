import time
import requests

data_s = [0, 0, 0]
data_t = []


def Average(lst):
    return sum(lst) / len(lst)


while True:
    with open('config_agregator.txt', 'r') as f:
        all_lines = f.readlines()
        t = int(all_lines[0])
    for k in range(t):
        for i in range(1, 4):
            r = requests.get(f'http://127.0.0.1:5000/data/app{i}')
            data_s[i - 1] = float(r.text)
        time.sleep(1)
        data_t.append(Average(data_s))
        av_data_t = str(Average(data_t))
        print(av_data_t)
        requests.post('http://127.0.0.1:5000/agregator', av_data_t)
    data_t = []
