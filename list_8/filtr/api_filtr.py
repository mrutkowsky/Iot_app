from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/config', methods=['POST'])
def main():
    if request.method == 'POST':
        filtr = 'filtr'
        data = request.get_json(force=True)
        json.dump(data, open(f'D:\Projects\pNo3\s_3\IoT\list_8\{filtr}\config.json', 'w'))
        print('config updated')
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=12345, debug=True)
