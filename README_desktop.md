# Aplicación de Escritorio para Descargar Reportes de Visitantes SLB

Esta aplicación permite descargar reportes de visitantes desde Supabase en formatos CSV, Excel o PDF de manera sencilla y segura.

## Características
- Interfaz amigable con colores corporativos de SLB
- Descarga de datos en CSV, Excel o PDF
- Las imágenes de firmas se incluyen directamente en Excel y PDF (sin archivos temporales)
- Portable: funciona en cualquier computador Windows sin instalación adicional
- Ícono personalizado con logo SLB
- Seguro: requiere configuración previa de clave API

## Configuración
La clave API ya está configurada en el código. No necesitas editar nada.

## Cómo usar
1. Ejecuta `desktop_app.exe`
2. Selecciona el formato deseado (CSV, Excel, PDF)
3. Haz clic en "Descargar Reporte"
4. Elige dónde guardar el archivo

## Notas
- PDF se genera en orientación horizontal para mostrar todas las columnas
- Excel incluye imágenes de firmas embebidas
- CSV es texto plano sin imágenes

## Requisitos
- Windows (el exe incluye todas las dependencias)
- Clave API válida de Supabase configurada en el código

## Configuración
La URL de Supabase está preconfigurada. Si necesitas cambiarla, contacta al administrador.

## Notas de seguridad
- La clave API se ingresa cada vez que se ejecuta la app
- No se almacena la clave en el disco
- Los datos se descargan directamente desde Supabase y se guardan localmente