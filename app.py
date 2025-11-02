from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import logging
import time
import asyncio
import websockets


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

def wbs_security():
    

def check_health(proxy):
    if awake[proxy] == "yes":
        url = j[proxy + "_url"]
        
        if not proxy == "cloudlink":
            resp = requests.post(url, json={"cle": CLE}, timeout=3 )
            j = resp.json()
            if not j["status"] or j["status"] == "ok":
                message = f"Une erreur a été détectée au proxy {proxy}. Voici l'erreur repérée par ton serveur : {resp}."
        
        else:
            async def test_connexion():
                uri = "wss://exemple.com/socket"
                headers = {
                    "cle": CLE,
                    "User-Agent": "Waker"
                }
                try:
                    async with websockets.connect(uri, extra_headers=headers) as ws:
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
        
@app.route("/", methods=["POST"])
def wake():
    depart = int(time.time())
    data = request.get_json(force=True, silent=True) or {}
    cle_received = data.get('cle')
    if cle_received:
        resp = requests.post(f"{URL}cle-ultra", json={"cle": cle_received}, timeout=5 )
        resp.raise_for_status()
        x = resp.json()
        access = x.get("access")
    if access == "false" or not cle_received:
        return jsonify({"status": "error", "message": "clé invalide"})

    wake_server()
    
    while int(time.time) < depart + 15:
        time.sleep(1)
    wake_server()

    while int(time.time) < depart + 30:
        time.sleep(1)
    wake_server()
    
    
    return jsonify({"message": "ok"})
