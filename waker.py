from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests

app = Flask(__name__)
 
CLE = os.environ.get('CLE_ULTRA')
URL = os.environ.get('URL')
resp = requests.post(URL, json={"cle": CLE}, timeout=5 )
resp.raise_for_status()
j = resp.json()
wake = j.get("awake_url")
resp = requests.post(wake, json={"cle": CLE}, timeout=5 )
