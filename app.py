import os
from datetime import datetime

import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://jfhsgobubmmedsbtenay.supabase.co")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpmaHNnb2J1Ym1tZWRzYnRlbmF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ4OTM2NjgsImV4cCI6MjA5MDQ2OTY2OH0.QGs3_rYsX7e4uzUMJhtLkL47-rcdhMtZWWElsLptmrI")


def guardar_registro(data):
    url = f"{SUPABASE_URL}/rest/v1/registros"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    payload = {
        "nombre": data.get("nombre", ""),
        "tipoDocumento": data.get("tipoDocumento", ""),
        "documento": data.get("documento", ""),
        "contacto": data.get("contacto", ""),
        "empresa": data.get("empresa", ""),
        "alcocheck": data.get("alcocheck", ""),
        "arl": data.get("arl", ""),
        "eps": data.get("eps", ""),
        "rh": data.get("rh", ""),
        "alergias": data.get("alergias", ""),
        "emergencia": data.get("emergencia", ""),
        "visita": data.get("visita", ""),
        "serial": data.get("serial", ""),
        "laptopIngreso": data.get("laptopIngreso", ""),
        "laptopSalida": data.get("laptopSalida", ""),
        "aceptaDatos": data.get("aceptaDatos", False),
        "firma": data.get("firma", ""),
        "fechaRegistro": datetime.utcnow().isoformat()
    }

    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "app": "visitor-registration", "time": datetime.now().isoformat()})


@app.route("/registros", methods=["GET"])
def get_registros():
    url = f"{SUPABASE_URL}/rest/v1/registros"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return jsonify(response.json())


@app.route("/registro", methods=["POST"])
def registro():
    data = request.json

    if not data.get("aceptaDatos"):
        return jsonify({"error": "Debe aceptar los términos"}), 400

    try:
        guardar_registro(data)
        return jsonify({"ok": True})
    except Exception as e:
        app.logger.exception("Error en /registro")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
