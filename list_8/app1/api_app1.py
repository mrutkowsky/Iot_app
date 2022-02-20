import paho.mqtt.client as mqtt
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/app1/status', methods=['POST'])
def status():
    if request.method == 'POST':
        app1 = 'app1'
        data = request.get_json(force=True)
        with open('config1.json', 'r') as f:
            config = json.load(f)
            print(data)
            config['s_1'] = data['s_1']
        json.dump(config, open(f'D:\Projects\pNo3\s_3\IoT\list_8\{app1}\config1.json', 'w'))
    return data


@app.route('/app1/frequency', methods=['POST'])
def frequency():
    if request.method == 'POST':
        app1 = 'app1'
        data = request.get_json(force=True)
        with open('config1.json', 'r') as f:
            config = json.load(f)
            print(data)
            config['fq'] = data['fq']
        json.dump(config, open(f'D:\Projects\pNo3\s_3\IoT\list_8\{app1}\config1.json', 'w'))
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12341, debug=True)
