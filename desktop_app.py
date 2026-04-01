import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests
import csv
import os
from datetime import datetime
from PIL import Image, ImageTk

# Configuración de Supabase
SUPABASE_URL = "https://jfhsgobubmmedsbtenay.supabase.co"  # URL fija
SUPABASE_ANON_KEY = ""  # Se ingresa en la app

def descargar_reporte(api_key):
    if not api_key:
        messagebox.showerror("Error", "Por favor ingrese la clave API de Supabase.")
        return

    try:
        # URL para obtener todos los registros
        url = f"{SUPABASE_URL}/rest/v1/registros"
        headers = {
            "apikey": api_key,
            "Authorization": f"Bearer {api_key}",
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
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Guardar Reporte",
            initialfile=f"reporte_visitantes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        if not file_path:
            return

        # Escribir a CSV
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            if data:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

        messagebox.showinfo("Éxito", f"Reporte descargado exitosamente en {file_path}")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            messagebox.showerror("Error", "Clave API incorrecta. Verifique la clave de Supabase.")
        else:
            messagebox.showerror("Error", f"Error HTTP: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error al conectar con Supabase: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {str(e)}")

# Crear ventana principal
root = tk.Tk()
root.title("Descargador de Reportes - Registro de Visitantes SLB")
root.geometry("500x400")
root.configure(bg="#003366")  # Azul SLB

# Estilo
style = ttk.Style()
style.configure("TLabel", background="#003366", foreground="white", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10, "bold"))
style.configure("TEntry", font=("Arial", 10))

# Frame principal
main_frame = tk.Frame(root, bg="#003366")
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Logo (texto por ahora, puedes reemplazar con imagen)
logo_label = tk.Label(main_frame, text="SLB", font=("Arial", 24, "bold"), fg="white", bg="#003366")
logo_label.pack(pady=10)

subtitle_label = tk.Label(main_frame, text="Sistema de Registro de Visitantes", font=("Arial", 12), fg="white", bg="#003366")
subtitle_label.pack(pady=5)

# Campo para API Key
api_frame = tk.Frame(main_frame, bg="#003366")
api_frame.pack(pady=10)
api_label = tk.Label(api_frame, text="Clave API de Supabase:", fg="white", bg="#003366", font=("Arial", 10))
api_label.pack(side="left")
api_entry = tk.Entry(api_frame, width=40, show="*")  # Ocultar clave
api_entry.pack(side="left", padx=10)

# Botón
button = tk.Button(main_frame, text="Descargar Reporte", command=lambda: descargar_reporte(api_entry.get()), 
                   height=2, width=25, bg="white", fg="#003366", font=("Arial", 12, "bold"))
button.pack(pady=20)

# Instrucciones
instructions = tk.Label(main_frame, text="Ingrese la clave API y haga clic para descargar el reporte en CSV.", 
                        fg="white", bg="#003366", font=("Arial", 9), wraplength=400)
instructions.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()