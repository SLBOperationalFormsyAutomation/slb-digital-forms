# Aplicación de Escritorio para Descargar Reportes de Visitantes SLB

Esta aplicación permite descargar reportes de visitantes desde Supabase en formatos CSV, Excel o PDF de manera sencilla y segura.

## Características
- Interfaz amigable con colores corporativos de SLB
- Descarga de datos en CSV, Excel o PDF
- Las imágenes de firmas se incluyen en Excel y PDF
- Portable: funciona en cualquier computador Windows sin instalación adicional
- Seguro: requiere configuración previa de clave API

## Configuración
Antes de usar, edita `desktop_app.py` y reemplaza `"tu-anon-key"` con tu clave real de Supabase.

## Cómo usar
1. Ejecuta `desktop_app.exe`
2. Selecciona el formato deseado (CSV, Excel, PDF)
3. Haz clic en "Descargar Reporte"
4. Elige dónde guardar el archivo

## Requisitos
- Windows (el exe incluye todas las dependencias)
- Clave API válida de Supabase configurada en el código

## Notas de seguridad
- La clave API está hardcodeada en el código; no la compartas
- Los datos se descargan directamente desde Supabase y se guardan localmente

## Configuración
La URL de Supabase está preconfigurada. Si necesitas cambiarla, contacta al administrador.

## Notas de seguridad
- La clave API se ingresa cada vez que se ejecuta la app
- No se almacena la clave en el disco
- Los datos se descargan directamente desde Supabase y se guardan localmente