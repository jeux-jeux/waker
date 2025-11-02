from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import logging
import time

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

CLE = os.environ.get('CLE')
URL = os.environ.get('URL')

data_cache = {
    "manager":0, 
    "cloudlink":0, 
    "message":0, 
    "firebase":0
}

resp = requests.post(URL, json={"cle": CLE}, timeout=5 )
resp.raise_for_status()
j = resp.json()
awake = j.get("awake")

def check_health(proxy):
    if awake[proxy] == "yes":
        url = j[proxy + "_url"]
        resp = requests.post(url, json={"cle": CLE}, timeout=4 )
            if not j["status"] or j["status"] == "ok":
                if data_cache[proxy] < 3:
                    resp = requests.post(j["ntfy_url"], json={"cle": CLE}, timeout=5 )                    
                
@app.route("/", methods=["POST"])
def wake():
    data = request.get_json(force=True, silent=True) or {}
    cle_received = data.get('cle')
    if cle_received:
        resp = requests.post(f"{URL}cle-ultra", json={"cle": cle_received}, timeout=5 )
        resp.raise_for_status()
        x = resp.json()
        access = x.get("access")
    if access == "false" or not cle_received:
        return jsonify({"status": "error", "message": "clé invalide"})

    
