# Aplicación de Escritorio para Descargar Reportes de Visitantes SLB

Esta aplicación permite descargar reportes de visitantes desde Supabase en formato CSV de manera sencilla y segura.

## Características
- Interfaz amigable con colores corporativos de SLB
- Descarga de datos en CSV
- Portable: funciona en cualquier computador Windows sin instalación adicional
- Seguro: requiere clave API para acceder a los datos

## Cómo usar
1. Ejecuta `desktop_app.exe`
2. Ingresa tu clave API de Supabase (anon key)
3. Haz clic en "Descargar Reporte"
4. Elige dónde guardar el archivo CSV

## Requisitos
- Windows (el exe incluye todas las dependencias)
- Clave API válida de Supabase

## Configuración
La URL de Supabase está preconfigurada. Si necesitas cambiarla, contacta al administrador.

## Notas de seguridad
- La clave API se ingresa cada vez que se ejecuta la app
- No se almacena la clave en el disco
- Los datos se descargan directamente desde Supabase y se guardan localmente