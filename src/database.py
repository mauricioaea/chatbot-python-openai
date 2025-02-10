import sqlite3
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la clave de encriptación desde .env
key = os.getenv("ENCRYPTION_KEY")

# Verificar si la clave está definida
if not key:
    raise ValueError("ERROR: ENCRYPTION_KEY no está definida en las variables de entorno.")

# Verificar si la clave tiene el formato correcto
try:
    key = key.encode()
    cipher = Fernet(key)
except Exception as e:
    raise ValueError(f"ERROR: La clave Fernet no es válida. Verifica que tenga 32 bytes codificados en Base64. Detalle: {e}")

def init_db():
    """Inicializa la base de datos SQLite y crea la tabla bookings si no existe."""
    if os.path.exists("reservas.db"):
        os.remove("reservas.db")  # Eliminar la base de datos existente (solo para pruebas)
        
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id TEXT PRIMARY KEY,
                    check_in TEXT NOT NULL,
                    check_out TEXT NOT NULL,
                    client_name TEXT NOT NULL,
                    client_phone TEXT NOT NULL,
                    apartment_type TEXT NOT NULL,
                    price REAL NOT NULL,
                    status TEXT NOT NULL)''')
    conn.commit()
    return conn

def encrypt_data(data):
    """Encripta datos sensibles (ej: teléfonos)."""
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    """Desencripta datos previamente encriptados."""
    return cipher.decrypt(encrypted_data.encode()).decode()