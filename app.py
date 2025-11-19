from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import logging
import time
import asyncio
import websockets
import ast
import random

app = Flask(__name__)


TOKEN = os.environ.get('GITHUB_TOKEN')
CLE = os.environ.get('CLE_ULTRA')
URL = os.environ.get('URL')

data_cache = {
    "manager":0, 
    "cloudlink":0, 
    "message":0, 
    "firebase":0
}

resp = requests.post(URL, json={"cle": CLE}, timeout=5)
resp.raise_for_status()
a = resp.json()
wbs = a.get("cloudlink_url")
awake = a.get("awake")
awake = ast.literal_eval(awake)
port = a.get("port_wake")
ntfy_url = a.get("ntfy_url")
manager_url = a.get("manager_url")


def wbs_security():
    resp = requests.post(f"{manager_url}get/rooms", json={"cle": CLE}, timeout=5)
    resp.raise_for_status()
    b = resp.json()
    rooms = b.get("rooms")
    
    users = []
    
    for room in rooms:
        resp = requests.post(f"{manager_url}get/users", json={"cle": CLE, "room": [room]}, timeout=5)
        resp.raise_for_status()
        c = resp.json()
        users_in_room = list(c.get("val", {}).keys())
        for user in users_in_room:
            users.append(user)
            
    users = list(set(users))
    
    requests.post(URL, json={"cle": CLE, "token": random.randint(100000, 999999)}, timeout=5)
    
    
def check_health(proxy):
    message = None
    if awake[proxy] == "yes":
        url = a[proxy + "_url"]
        
        if not proxy == "cloudlink":
            try:
                resp = requests.post(url, json={"cle": CLE}, timeout=3 )
                j = resp.json()
            except ValueError:
                message = f"Une erreur a été détectée au proxy {proxy}. Voici l'erreur repérée par ton serveur : {resp}."
        
        else:
            async def test_connexion():
                headers = {
                    "cle": CLE,
                    "User-Agent": "Waker"
                }
                try:
                    async with websockets.connect(url, extra_headers=headers) as ws:
                        # On se déconnecte immédiatement après la connexion
                        await ws.close()
                except Exception as e:
                    message = "Une erreur a été détectée au serveur Cloudlink. Ton waker a essayé de s'y sonnecter mais n'y est pas parvenu"
            asyncio.run(test_connexion())

        
        if data_cache[proxy] <= 3 and message:
            resp = requests.post(ntfy_url + "-waker", data=message, headers={"Content-Type": "text/plain"}, timeout=3 )
            data_cache[proxy] += 1

def wake_server():
    check_health("manager")
    check_health("firebase")
    check_health("message")
    check_health("cloudlink")
    if awake["wbs_security"] == "yes":
        wbs_security()
        
for i in range(60):
    depart = int(time.time())

    wake_server()
    
    while int(time.time()) < depart + 15:
        time.sleep(1)
    wake_server()

    while int(time.time()) < depart + 30:
        time.sleep(1)
    wake_server()

import os
import requests

owner = "jeux-jeux"
repo = "waker"
workflow_file = "run.yml"

# Récupération du token temporaire fourni par GitHub Actions
github_token = os.environ.get("GITHUB_TOKEN")

url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_file}/dispatches"
data = {"ref": "main"}

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {github_token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

resp = requests.post(url, headers=headers, json=data)
print(resp.status_code, resp.text)