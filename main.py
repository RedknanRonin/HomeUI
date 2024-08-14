import threading

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
import time
from ruuvitag_sensor.ruuvi import RuuviTagSensor
import asyncio
from pip._vendor import requests

app = Flask(__name__)
CONFIG_FILE = 'data/config.json'


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return []

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)



last_fetch_time = 0
cached_ruuvitag_data = {}
async def ruuvitagData():
    global last_fetch_time, cached_ruuvitag_data
    current_time = time.time()
    refresh_interval = 300  # 5 minutes

    # Check if the data needs to be refreshed
    if current_time - last_fetch_time < refresh_interval:
        return cached_ruuvitag_data

    conf = load_config()
    macs = conf["macs"]
    datas = dict()
    res = {}
    run = True
    while run:
        async for found_data in RuuviTagSensor.get_data_async(macs):
            datas.update({found_data[0]: found_data[1]})
            if len(datas.keys()) == 3:
                run = False
                break

        for each in datas:
            res[each] = datas[each]['temperature']

    # Update the last fetch time and cached data
    last_fetch_time = current_time
    cached_ruuvitag_data = res

    return res

def schedule_ruuvitag_data():
    ruuvitagData()
    threading.Timer(300, schedule_ruuvitag_data).start() # called every 5min

def airthingsAuth():
    config=load_config()
    current_time = time.time()
    token_expiry_time =(config.get("airthingsAuthTokenExpiry", 0))
    if current_time < token_expiry_time:
        return  # Token is still valid, no need to refresh

    url="https://accounts-api.airthings.com/v1/token"
    headers = {
        "grant_type":"client_credentials",
        "client_id":config.get("airthingsClientId"),
        "client_secret":config.get("airthingsClientSecret"),
        "Accept": "application/json"
        }
    response = requests.post(url, data=headers)   #headers should be in data?? and not headers?
    if response.status_code == 200:
        config["airthingsAuthToken"]=response.json().get("access_token")
        config["airthingsAuthTokenExpiry"] = current_time + response.json().get("expires_in")
        save_config(config)
    else:
        print("Failed to authenticate with Airthings API")

def hueAuth():
    config=load_config()
    current_time = time.time()

    if (len(config["hueRefreshToken"])==0) or (config["hueAuthTokenExpiry"] < current_time):
        authrequest=requests.get("https://api.meethue.com/v2/oauth2/authorize?client_id="+config["hueClientId"]+"&response_type=code")

        if authrequest.status_code == 200:
            print("Please visit the following URL to authorize the application:")
            print(authrequest.url)
            auth_code = input("Enter the authorization code: ")

            # Step 2: Exchange authorization code for access token
            token_url = "https://api.meethue.com/v2/oauth2/token"
            token_data = {
                "code": auth_code,
                "grant_type": "authorization_code",
                "client_id": config['hueClientId'],
                "client_secret": config['hueClientSecret']
            }
            token_headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            token_response = requests.post(token_url, data=token_data, headers=token_headers)

            if token_response.status_code == 200:
                token_info = token_response.json()
                config["hueAuthToken"] = token_info.get("access_token")
                config["hueAuthTokenExpiry"] = current_time + token_info.get("expires_in")
                config["hueRefreshToken"] = token_info.get("refresh_token")
                save_config(config)
            else:
                print("Failed to obtain access token")

        else:
            print("Failed to initiate authorization")
    else:
        token_url = "https://api.meethue.com/v2/oauth2/token"
        token_data = {
            "grant_type": "refresh_token",
            "client_id": config['hueClientId'],
            "client_secret": config['hueClientSecret'],
            "refresh_token": config["hueRefreshToken"]
        }
        token_headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        token_response = requests.post(token_url, data=token_data, headers=token_headers)
        if token_response.status_code == 200:
            token_info = token_response.json()
            config["hueAuthToken"] = token_info.get("access_token")
            config["hueAuthTokenExpiry"] = current_time + token_info.get("expires_in")
            config["hueRefreshToken"] = token_info.get("refresh_token")
            save_config(config)
        else:
            print("Failed to obtain refresh token")



@app.route('/')
def home():
    hueAuth()
    threading.Timer(10800, airthingsAuth()).start()
    config=load_config()
    return render_template('index.html',config=config)

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route('/ruuvitag_data', methods=['GET'])
async def get_ruuvitag_data():
    res=await asyncio.create_task(ruuvitagData())
    print(res)
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug="True",host="0.0.0.0", port=5000)
