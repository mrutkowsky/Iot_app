from flask import Flask, render_template, request, redirect, url_for
import requests
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        with open('D:\Projects\pNo3\s_3\IoT\list_8\status_codes.json', 'r') as f:
            data = json.load(f)
            s_1 = data["s_1"]
            s_2 = data["s_2"]
            s_3 = data["s_3"]
        return render_template('main.html', status1=s_1, status2=s_2, status3=s_3)
    if request.method == 'POST':
        s_1 = request.form['s_1']
        s_2 = request.form['s_2']
        s_3 = request.form['s_3']
        status_codes = {"s_1": s_1, "s_2": s_2, "s_3": s_3}
        json.dump(status_codes, open(f'D:\Projects\pNo3\s_3\IoT\list_8\status_codes.json', 'w'))
        requests.post('http://192.168.100.77:12341/app1/status', json.dumps({"s_1": s_1}))
        requests.post('http://192.168.100.77:12342/app2/status', json.dumps({"s_2": s_2}))
        requests.post('http://192.168.100.77:12343/app3/status', json.dumps({"s_3": s_3}))
        return render_template('main.html', status1=s_1, status2=s_2, status3=s_3)


@app.route('/app<nr>', methods=['POST', 'GET'])
def home_app(nr):
    if request.method == 'GET':
        with open(f"D:\Projects\pNo3\s_3\IoT\list_8\content{nr}.json", 'r') as f:
            cont = f.read()
        return render_template('index.html', cont=cont)
    if request.method == 'POST':
        data = request.get_json(force=True)
        json.dump(data, open(f'D:\Projects\pNo3\s_3\IoT\list_8\content{nr}.json', 'w'))
        return data


@app.route('/data/<app_nr>', methods=['GET'])
def get_data(app_nr):
    nr = str(app_nr[-1])
    if request.method == 'GET':
        with open(f'D:\Projects\pNo3\s_3\IoT\list_8\content{nr}.json', 'r') as f:
            json_data = json.load(f)
        return str(json_data['Air Temperature'])


@app.route('/panel/<app_nr>', methods=['POST', 'GET'])
def panel(app_nr):
    nr = str(app_nr[-1])
    if request.method == 'GET':
        return render_template('panel.html')
    if request.method == "POST":
        if app_nr == 'app1':
            fq = json.dumps({"fq": request.form['fq']})
            requests.post(f'http://192.168.100.77:12341/{app_nr}/frequency', fq)
        elif app_nr == 'app2':
            fq = json.dumps({"fq": request.form['fq']})
            requests.post(f'http://192.168.100.77:12342/{app_nr}/frequency', fq)
        elif app_nr == 'app3':
            fq = json.dumps({"fq": request.form['fq']})
            requests.post(f'http://192.168.100.77:12343/{app_nr}/frequency', fq)
        return redirect(url_for('home_app', nr=nr))


@app.route('/agregator', methods=['POST', 'GET'])
def agregator():
    agregator = 'agregator'
    if request.method == 'GET':
        with open(f"D:\Projects\pNo3\s_3\IoT\list_8\{agregator}.json", 'r') as f:
            cont = f.read()
        return render_template('agregator.html', cont=cont)
    if request.method == 'POST':
        data = request.get_json(force=True)
        json.dump(data, open(f'D:\Projects\pNo3\s_3\IoT\list_8\{agregator}.json', 'w'))
        return str(data)


@app.route('/filtr', methods=['GET', 'POST'])
def filtr():
    if request.method == 'GET':
        return render_template('filtr.html')
    if request.method == 'POST':
        ad_1 = request.form['ad_get']
        fields = request.form['f_n']
        ad_2 = request.form['ad_post']
        data = {'ad_1': ad_1, 'f_n': fields, 'ad_2': ad_2}
        data_j = json.dumps(data)
        requests.post('http://192.168.100.77:12345/config', data_j)
        print('config posted')
    return redirect(url_for('filtr'))


@app.route('/data/filtr/<app_nr>', methods=['GET'])
def get_no_filtr_data(app_nr):
    nr = str(app_nr[-1])
    if request.method == 'GET':
        with open(f'D:\Projects\pNo3\s_3\IoT\list_8\content{nr}.json', 'r') as f:
            json_data = json.load(f)
        return json_data


@app.route('/filtr/show_data', methods=['POST', 'GET'])
def get_filtred_data():
    filtred = 'filtred'
    if request.method == 'GET':
        with open(f"D:\Projects\pNo3\s_3\IoT\list_8\{filtred}_data.json", 'r') as f:
            cont = f.read()
        return render_template('index.html', cont=cont)
    if request.method == 'POST':
        data = request.get_json(force=True)
        json.dump(data, open(f'D:\Projects\pNo3\s_3\IoT\list_8\{filtred}_data.json', 'w'))
    return data


@app.route('/graph')
def graph():
    temp_data = [0,0,0]
    for i in range(1, 4):
        with open(f'content{i}.json', 'r') as f:
            json_data = json.load(f)
        temp = float(json_data['Air Temperature'])
        temp_data[i-1] = temp
    temp_1 = temp_data[0]
    temp_2 = temp_data[1]
    temp_3 = temp_data[2]
    df = pd.DataFrame({
        'Apps': ['App1', 'App2', 'App3'],
        'Temperature': [temp_1, temp_2, temp_3]
    })
    fig = px.bar(df, x='Apps', y='Temperature')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graph.html', graphJSON=graphJSON)

@app.route('/agregator/graph')
def graph_agr():
    temp_data = [0,0,0]
    for i in range(1, 4):
        with open(f'content{i}.json', 'r') as f:
            json_data = json.load(f)
        temp = float(json_data['Air Temperature'])
        temp_data[i-1] = temp
    with open('agregator.json', 'r') as f:
        json_data_agr = json.load(f)
    temp_avg = int(json_data_agr)
    temp_1 = temp_data[0]
    temp_2 = temp_data[1]
    temp_3 = temp_data[2]
    df = pd.DataFrame({
        'Apps': ['App1', 'App2', 'App3', 'Agregator'],
        'Temperature': [temp_1, temp_2, temp_3, temp_avg]
    })

    fig = px.bar(df, x='Apps', y='Temperature')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graph.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
