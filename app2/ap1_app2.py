import paho.mqtt.client as mqtt
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/app2/status', methods=['POST'])
def status():
    if request.method == 'POST':
        app2 = 'app2'
        data = request.get_json(force=True)
        with open('config2.json', 'r') as f:
            config = json.load(f)
            print(data)
            config['s_2'] = data['s_2']
        json.dump(config, open(f'D:\Projects\pNo3\s_3\IoT\list_8\{app2}\config2.json', 'w'))
    return data


@app.route('/app2/frequency', methods=['POST'])
def frequency():
    if request.method == 'POST':
        app2 = 'app2'
        data = request.get_json(force=True)
        with open('config2.json', 'r') as f:
            config = json.load(f)
            print(data)
            config['fq'] = data['fq']
        json.dump(config, open(f'D:\Projects\pNo3\s_3\IoT\list_8\{app2}\config2.json', 'w'))
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12342, debug=True)
