import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests
import csv
import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from io import BytesIO
from PIL import Image
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image as RLImage

# Configuración de Supabase
SUPABASE_URL = "https://jfhsgobubmmedsbtenay.supabase.co"
SUPABASE_ANON_KEY = "tu-anon-key"  # Reemplaza con tu clave real de Supabase

def descargar_reporte(formato):
    try:
        # URL para obtener todos los registros
        url = f"{SUPABASE_URL}/rest/v1/registros"
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        }
        params = {
            "select": "*"  # Obtener todos los campos
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            messagebox.showinfo("Información", "No hay registros para descargar.")
            return

        # Pedir ubicación para guardar
        if formato == "CSV":
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Guardar Reporte CSV",
                initialfile=f"reporte_visitantes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if not file_path:
                return
            # Escribir CSV
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                if data:
                    writer = csv.DictWriter(file, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)

        elif formato == "Excel":
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Guardar Reporte Excel",
                initialfile=f"reporte_visitantes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            if not file_path:
                return
            # Generar Excel
            wb = Workbook()
            ws = wb.active
            ws.title = "Registros"

            # Headers
            headers = list(data[0].keys())
            for col_num, header in enumerate(headers, 1):
                ws.cell(row=1, column=col_num, value=header)

            # Datos
            for row_num, reg in enumerate(data, 2):
                for col_num, key in enumerate(headers, 1):
                    if key == "firma" and reg.get(key):
                        # Insertar imagen de firma
                        try:
                            firma_base64 = reg[key]
                            if ',' in firma_base64:
                                firma_data = base64.b64decode(firma_base64.split(',')[1])
                            else:
                                firma_data = base64.b64decode(firma_base64)
                            img = Image.open(BytesIO(firma_data))
                            img_path = f"temp_firma_{row_num}.png"
                            img.save(img_path)
                            xl_img = XLImage(img_path)
                            ws.add_image(xl_img, f'{chr(64 + col_num)}{row_num}')
                            os.remove(img_path)  # Limpiar temp
                        except Exception as e:
                            ws.cell(row=row_num, column=col_num, value="Error en firma")
                    else:
                        ws.cell(row=row_num, column=col_num, value=reg.get(key, ""))

            wb.save(file_path)

        elif formato == "PDF":
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Guardar Reporte PDF",
                initialfile=f"reporte_visitantes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            if not file_path:
                return
            # Generar PDF
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []

            # Datos para tabla
            table_data = [list(data[0].keys())]  # Headers
            for reg in data:
                row = []
                for key in data[0].keys():
                    if key == "firma" and reg.get(key):
                        # Para PDF, insertar imagen
                        try:
                            firma_base64 = reg[key]
                            if ',' in firma_base64:
                                firma_data = base64.b64decode(firma_base64.split(',')[1])
                            else:
                                firma_data = base64.b64decode(firma_base64)
                            img = Image.open(BytesIO(firma_data))
                            img_path = f"temp_firma_pdf_{len(table_data)}.png"
                            img.save(img_path)
                            rl_img = RLImage(img_path, width=50, height=30)
                            row.append(rl_img)
                            # Limpiar después
                        except:
                            row.append("Firma no disponible")
                    else:
                        row.append(str(reg.get(key, "")))
                table_data.append(row)

            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
            doc.build(elements)

        messagebox.showinfo("Éxito", f"Reporte descargado exitosamente en {file_path}")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            messagebox.showerror("Error", "Clave API incorrecta. Verifica la configuración.")
        else:
            messagebox.showerror("Error", f"Error HTTP: {e.response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {str(e)}")

# Crear ventana principal
root = tk.Tk()
root.title("Descargador de Reportes - Registro de Visitantes SLB")
root.geometry("500x450")
root.configure(bg="#003366")

# Estilo
style = ttk.Style()
style.configure("TLabel", background="#003366", foreground="white", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10, "bold"))
style.configure("TCombobox", font=("Arial", 10))

# Frame principal
main_frame = tk.Frame(root, bg="#003366")
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Logo
logo_label = tk.Label(main_frame, text="SLB", font=("Arial", 24, "bold"), fg="white", bg="#003366")
logo_label.pack(pady=10)

subtitle_label = tk.Label(main_frame, text="Sistema de Registro de Visitantes", font=("Arial", 12), fg="white", bg="#003366")
subtitle_label.pack(pady=5)

# Selector de formato
format_frame = tk.Frame(main_frame, bg="#003366")
format_frame.pack(pady=10)
format_label = tk.Label(format_frame, text="Formato del reporte:", fg="white", bg="#003366", font=("Arial", 10))
format_label.pack(side="left")
format_combo = ttk.Combobox(format_frame, values=["CSV", "Excel", "PDF"], state="readonly")
format_combo.current(0)  # Default CSV
format_combo.pack(side="left", padx=10)

# Botón
button = tk.Button(main_frame, text="Descargar Reporte", command=lambda: descargar_reporte(format_combo.get()), 
                   height=2, width=25, bg="white", fg="#003366", font=("Arial", 12, "bold"))
button.pack(pady=20)

# Instrucciones
instructions = tk.Label(main_frame, text="Selecciona el formato y haz clic para descargar.\nLos formatos Excel y PDF incluyen imágenes de firmas.", 
                        fg="white", bg="#003366", font=("Arial", 9), wraplength=400, justify="center")
instructions.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()