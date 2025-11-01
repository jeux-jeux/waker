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

resp = requests.post(f"{URL}cle-ultra", json={"cle": cle_received}, timeout=5 )
resp.raise_for_status()
j = resp.json()
awake = j.get("awake")

def check_health(proxy):
    if awake[proxy] == "yes":
        

@app.route("/", methods=["POST"])
def wake():
    data = request.get_json(force=True, silent=True) or {}
    cle_received = data.get('cle')
    if cle_received:
        resp = requests.post(f"{URL}cle-ultra", json={"cle": cle_received}, timeout=5 )
        resp.raise_for_status()
        j = resp.json()
        access = j.get("access")
    if access == "false" or not cle_received:
        return jsonify({"status": "error", "message": "clé invalide"})

    
