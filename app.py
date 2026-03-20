from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openpyxl import load_workbook
from datetime import datetime
import base64
from openpyxl.drawing.image import Image as XLImage
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Ruta de tu Excel en OneDrive
ruta_excel = r"C:\Users\JTibaduiza2\OneDrive - SLB\Registro_Visitantes.xlsx"


def guardar_registro(data):
    wb = load_workbook(ruta_excel)
    ws = wb.active

    # Número consecutivo
    siguiente_numero = ws.max_row
    fecha = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M")

    # 🔹 1. Crear fila SIN firma (importante)
    fila = [
        siguiente_numero,
        fecha,
        hora,
        "",
        data["nombre"],
        f"{data['tipoDocumento']} - {data['documento']}",
        data["contacto"],
        data["empresa"],
        data["alcocheck"],
        data["arl"],
        data["eps"],
        data["rh"],
        data["alergias"],
        data["emergencia"],
        data["visita"],
        data["serial"],
        data["laptopIngreso"],
        data["laptopSalida"],
        ""  # <- Firma va como imagen, no texto
    ]

    ws.append(fila)

    # 🔹 2. Procesar firma base64
    firma_base64 = data["firma"].split(",")[1]
    firma_bytes = base64.b64decode(firma_base64)

    imagen_stream = BytesIO(firma_bytes)
    imagen = XLImage(imagen_stream)

    # 🔹 3. Insertar imagen en Excel
    fila_excel = ws.max_row
    celda_firma = f"S{fila_excel}"  # Columna S

    imagen.width = 150
    imagen.height = 60

    ws.add_image(imagen, celda_firma)

    # 🔹 4. Ajustar altura de fila
    ws.row_dimensions[fila_excel].height = 50

    # Guardar archivo
    wb.save(ruta_excel)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/registro", methods=["POST"])
def registro():
    data = request.json

    if not data.get("aceptaDatos"):
        return jsonify({"error": "Debe aceptar los términos"}), 400

    try:
        guardar_registro(data)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)