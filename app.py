import os,sys
sys.dont_write_bytecode = True
import requests
import json
from flask import Flask,jsonify,request,send_file
from metrics import *
from prometheus_client import CollectorRegistry

import socket

PROM_PORT = 9090
APP_PORT = 80
worker_name = socket.gethostname()

pool = {}

#Inicializando o app:
app = Flask(__name__)

def token_auth(token):
    # example token
    if token == '77d9-kg73-832k-235j-ji33':
        return '765325312'
    return None

def ingestion(dados):
    global pool
    token = dados['token']
    client_id = token_auth(token)
    if client_id is not None:
        metric_type = dados['type']
        metric_name = dados['name']
        metric_value = dados['value']
        description = dados['description']
        label1 = dados['label1']
        if metric_type == 'counter':
            if metric_name not in pool:
                pool[metric_name] = Counter(metric_name, description, ['worker_name','client_id','label1'])
            pool[metric_name].labels(worker_name, client_id, label1).inc(metric_value)
            return True
        elif metric_type == 'gauge':
            if metric_name not in pool:
                pool[metric_name] = Gauge(metric_name, description, ['worker_name','client_id','label1'])
            pool[metric_name].labels(worker_name, client_id, label1).set(metric_value)
            return True
        return False

@app.route('/', methods=['GET'])
def raiz():
    #redirect to /metrics:
    url = "http://localhost:" + str(PROM_PORT)
    redirect = requests.get(url, stream=True)
    return redirect.raw.read(), redirect.status_code, redirect.headers.items()

@app.route('/api/v1/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        dados = json.loads(request.data.decode('utf-8'))
        if ingestion(dados) == True:
            METRIC_INGESTION_SUCCESS_COUNT.labels(worker_name).inc()
            response = 'ok'
        else:
            response = 'error'
        return response

start_http_server(PROM_PORT, '0.0.0.0')
app.run(debug=False, host='0.0.0.0', port=APP_PORT)
