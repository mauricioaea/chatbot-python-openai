import os

filepath = r"C:\credenciales\chatbot-ia-449403-201808443630.json"  # Usa una cadena raw para la ruta

if os.path.exists(filepath):
    print(f"Archivo existe: {filepath}")
    try:
        with open(filepath, 'r') as f:
            print("Archivo abierto correctamente.")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
else:
    print(f"Archivo NO encontrado: {filepath}")