import sqlite3
import os

def init_db():
    if os.path.exists("reservas.db"):
        os.remove("reservas.db")
        
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id TEXT PRIMARY KEY,
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL,
            client_name TEXT NOT NULL,
            client_phone TEXT NOT NULL,
            apartment_type TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    return conn