from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import time

app = Flask(__name__)
 
CLE = os.getenv('CLE_ULTRA')
URL = os.getenv('URL')
resp = requests.post(URL, json={"cle": CLE}, timeout=5 )
resp.raise_for_status()
j = resp.json()
wake = j.get("awake_url")
for i in range (59):
    now = int(time.time())
    resp = requests.post(wake, json={"cle": CLE}, timeout=5 )
    while int(time.time()) < now+60:
        time.sleep(1)
