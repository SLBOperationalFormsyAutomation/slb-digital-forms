# Visitor Registration (SLB)\n\nSistema de registro de visitantes con firma digital y almacenamiento en Excel.\n\n## Requisitos\n- Python 3.10+\n- Flask\n- flask-cors\n- openpyxl\n- gunicorn (para producción)\n\n## Archivos clave\n- `app.py`: backend Flask (rutas `/`, `/status`, `/registro`).\n- `index.html`: frontend web con formulario y canvas de firma.\n- `templates/index.html`: alternativa templated.\n- `requirements.txt`: dependencias.\n- `Procfile`: despliegue Render.\n\n## Endpoints\n- `GET /`: UI del formulario.\n- `GET /status`: Health check.\n- `GET /registros`: Ver registros en JSON.\n- `POST /registro`: Registrar visita (JSON).
- `GET /export_excel`: Descargar Excel con registros.\n\n## Desarrollo local\n1. Ambiente virtual\n   ```powershell\n   python -m venv venv\n   .\\venv\\Scripts\\activate\n   pip install -r requirements.txt\n   pip install gunicorn\n   ```\n2. Ejecutar local\n   ```powershell\n   python app.py\n   ```\n3. Abrir `http://127.0.0.1:5000` y probar formulario.\n4. Chequear health:\n   - `http://127.0.0.1:5000/status` -> `{"status":"ok"}`\n\n## Deploy en Render\n1. Repo en GitHub con estos archivos.\n2. Crear nuevo servicio Web en Render, conectar repo.\n3. `Build Command`: `pip install -r requirements.txt`\n4. `Start Command`: `gunicorn app:app --bind 0.0.0.0:$PORT`\n5. En `Environment` añadir: `RUTA_EXCEL=/tmp/Registro_Visitantes.xlsx`\n6. Cambiar `index.html`/`templates/index.html`: `const API_BASE = "https://slb-digital-forms.onrender.com"`.\n7. Desplegar y validar: `https://slb-digital-forms.onrender.com/status`.\n\n## Notas de implementación\n- Se guarda internamente `*.tmp` y se hace `os.replace` para evitar el bloqueo si Excel está abierto.\n- Accesible en API: `/registro` (POST JSON); `/status` (GET).\n- `aceptaDatos` obligatorio, firma definida y base64 PNG requerida.\n\n## Ejemplo de payload POST /registro\n```json\n{\n  "nombre": "Juan Pérez",\n  "tipoDocumento": "C.C",\n  "documento": "12345678",\n  "contacto": "3001234567",\n  "empresa": "SLB",\n  "alcocheck": "Negativo",\n  "arl": "ARL",\n  "eps": "EPS",\n  "rh": "O+",\n  "alergias": "Ninguna",\n  "emergencia": "Ana 3110000000",\n  "visita": "Oficina",\n  "serial": "ABC123",\n  "laptopIngreso": "Sí",\n  "laptopSalida": "No",\n  "aceptaDatos": true,\n  "firma": "data:image/png;base64,..."\n}\n```\n\n## Implementación actual (Supabase)\n\nGuarda datos en Supabase (PostgreSQL gratis, persistente).\n\n### Configurar Supabase\n\n1. Crear cuenta en `https://supabase.com` (gratis).\n2. Crear proyecto.\n3. Ir a Table Editor → Crear tabla 'registros' con columnas:\n   - id (uuid, primary)\n   - nombre (text)\n   - tipoDocumento (text)\n   - documento (text)\n   - contacto (text)\n   - empresa (text)\n   - alcocheck (text)\n   - arl (text)\n   - eps (text)\n   - rh (text)\n   - alergias (text)\n   - emergencia (text)\n   - visita (text)\n   - serial (text)\n   - laptopIngreso (text)\n   - laptopSalida (text)\n   - aceptaDatos (boolean)\n   - firma (text)\n   - created_at (timestamptz, default now())\n4. Ir a Settings → API → Copiar Project URL y anon public key.\n\n### Variables Render\n- `SUPABASE_URL = https://tu-project.supabase.co`\n- `SUPABASE_ANON_KEY = tu-anon-key`\n\n### Ver datos\n- `GET /registros` devuelve JSON.\n- En Supabase dashboard → Table → ver filas.\n- Export a CSV/Excel desde dashboard.

## Exportar a Excel en OneDrive

### Endpoint de Exportación
- `GET /export_excel`: Descarga un archivo Excel con todos los registros, incluyendo firmas como imágenes.

### Subir a OneDrive Manualmente
1. Ve a `https://tu-app-render.onrender.com/export_excel`.
2. Descarga el archivo `registros_visitantes.xlsx`.
3. Sube manualmente a OneDrive/SharePoint.

### Automatización con Power Automate (Recomendado)
Para subir automáticamente al Excel en OneDrive:

1. Crear flujo en Power Automate (https://powerautomate.microsoft.com).
2. Trigger: Recurrence (diario/semanal).
3. Acción: HTTP - GET a `https://tu-app-render.onrender.com/export_excel` (descargar archivo).
4. Acción: Create file en OneDrive/SharePoint con el contenido descargado, sobrescribiendo el archivo existente.

Esto actualiza el Excel en OneDrive automáticamente sin intervención manual.
