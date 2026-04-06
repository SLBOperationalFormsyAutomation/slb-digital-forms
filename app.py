from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import PatternFill, Font, Alignment
from datetime import datetime
import base64
from io import BytesIO
import os
import requests
from PIL import Image
from datetime import datetime, timedelta, timezone

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
        "nombre": data["nombre"],
        "tipoDocumento": data["tipoDocumento"],
        "documento": data["documento"],
        "contacto": data["contacto"],
        "empresa": data["empresa"],
        "alcocheck": data["alcocheck"],
        "arl": data.get("arl",""),
        "eps": data.get("eps",""),
        "rh": data.get("rh",""),
        "alergias": data.get("alergias",""),
        "emergencia": data.get("emergencia",""),
        "visita": data.get("visita",""),
        "serial": data.get("serial",""),
        "laptopIngreso": data.get("laptopIngreso",""),
        "laptopSalida": data.get("laptopSalida",""),
        "aceptaDatos": data["aceptaDatos"],
        "firma": data["firma"]
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


def formatear_fecha(fecha_str):
    """Convierte fecha ISO a hora Colombia (UTC-5)"""
    try:
        if not fecha_str:
            return ""

        # 🔥 Forzar UTC aunque no venga con Z
        if '.' in fecha_str:
            fecha_str = fecha_str.split('.')[0]

        dt_utc = datetime.fromisoformat(fecha_str)

        # ⚠️ CLAVE: asignar UTC manualmente si no tiene tzinfo
        if dt_utc.tzinfo is None:
            dt_utc = dt_utc.replace(tzinfo=timezone.utc)

        # Convertir a Colombia
        colombia_tz = timezone(timedelta(hours=-5))
        dt_col = dt_utc.astimezone(colombia_tz)

        return dt_col.strftime('%d/%m/%Y %H:%M:%S')

    except Exception as e:
        print("Error formateando fecha:", e)
        return fecha_str


@app.route("/export_excel", methods=["GET"])
def export_excel():
    # Obtener datos de Supabase
    url = f"{SUPABASE_URL}/rest/v1/registros"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    registros = response.json()

    # Crear workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Registros"

    # Headers - Excluir created_at y usar dinámicamente
    all_keys = list(registros[0].keys()) if registros else []
    headers = [h for h in all_keys if h != 'created_at']
    
    # Estilo de encabezados (Azul SLB)
    header_fill = PatternFill(start_color="003366", end_color="003366", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
    
    ws.row_dimensions[1].height = 30

    # Datos
    for row_num, reg in enumerate(registros, 2):
        row_height = 20
        for col_num, key in enumerate(headers, 1):
            if key == "firma" and reg.get(key):
                # Insertar imagen de firma
                try:
                    firma_base64 = reg[key]
                    if isinstance(firma_base64, str) and ',' in firma_base64:
                        firma_data = base64.b64decode(firma_base64.split(',')[1])
                    elif isinstance(firma_base64, str):
                        firma_data = base64.b64decode(firma_base64)
                    else:
                        raise ValueError("Formato de firma inválido")
                    img = Image.open(BytesIO(firma_data))
                    img_resized = img.resize((80, 60))
                    img_temp = BytesIO()
                    img_resized.save(img_temp, format='PNG')
                    img_temp.seek(0)
                    xl_img = XLImage(img_temp)
                    ws.add_image(xl_img, f'{chr(64 + col_num)}{row_num}')
                    row_height = 65
                except Exception as e:
                    ws.cell(row=row_num, column=col_num, value="Error en firma")
            elif key == "fechaRegistro" and reg.get(key):
                ws.cell(row=row_num, column=col_num, value=formatear_fecha(reg[key]))
            else:
                ws.cell(row=row_num, column=col_num, value=reg.get(key, ""))
        
        ws.row_dimensions[row_num].height = row_height
    
    # Ajustar ancho de columnas
    for col_num, key in enumerate(headers, 1):
        if key == "firma":
            ws.column_dimensions[chr(64 + col_num)].width = 15
        else:
            ws.column_dimensions[chr(64 + col_num)].width = 18

    # Guardar en memoria
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="registros_visitantes.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


if __name__ == "__main__":
    app.run(debug=True)