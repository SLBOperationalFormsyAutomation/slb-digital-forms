from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openpyxl import load_workbook
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el frontend

# Ruta de tu Excel sincronizado con OneDrive
ruta_excel = r"C:\Users\JTibaduiza2\OneDrive - SLB\Registro_Visitantes.xlsx"

def guardar_registro(data):
    wb = load_workbook(ruta_excel)
    ws = wb.active

    # Número consecutivo
    siguiente_numero = ws.max_row
    fecha = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M")

    # Crear fila con tipo de documento
    fila = [
        siguiente_numero,                     # N°
        fecha,                                # Fecha
        hora,                                 # HoraIngreso
        "",                                   # HoraSalida
        data["nombre"],                       # Nombres y Apellidos
        f"{data['tipoDocumento']} - {data['documento']}",  # N° Identificación
        data["contacto"],                     # Número de contacto
        data["empresa"],                      # Empresa
        data["alcocheck"],                    # Resultado Alcocheck
        "Firmado"                             # Firma
    ]

    ws.append(fila)
    wb.save(ruta_excel)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/registro", methods=["POST"])
def registro():
    data = request.json
    if not data.get("aceptaDatos"):
        return jsonify({"error": "Debe aceptar los términos"}), 400

    guardar_registro(data)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)