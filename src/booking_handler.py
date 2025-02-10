import phonenumbers
from datetime import datetime
import logging

def validate_phone(phone, country_code="VE"):
    """Valida números de teléfono internacionales."""
    try:
        parsed = phonenumbers.parse(phone, country_code)
        return phonenumbers.is_valid_number(parsed)
    except:
        return False

def validate_dates(date_str):
    """Valida el formato y lógica de las fechas."""
    try:
        check_in, check_out = date_str.split(" a ")
        start = datetime.strptime(check_in, "%Y-%m-%d")
        end = datetime.strptime(check_out, "%Y-%m-%d")
        
        if start >= end:
            return False, "❌ La fecha de salida debe ser posterior"
        if start < datetime.now():
            return False, "❌ No se permiten fechas pasadas"
            
        return True, (check_in, check_out)
    except:
        return False, "❌ Formato de fecha inválido"

def check_availability(conn, check_in, check_out):
    """Verifica la disponibilidad de los apartamentos."""
    cursor = conn.cursor()
    
    # Verificar ambos apartamentos
    apt1 = is_apartment_available(conn, "Frente al Mar", check_in, check_out)
    apt2 = is_apartment_available(conn, "Vista Piscina", check_in, check_out)
    
    if apt1 and apt2:
        return True, "Ambos apartamentos están disponibles."
    elif apt1:
        return True, "El apartamento 1 (Frente al Mar) está disponible."
    elif apt2:
        return True, "El apartamento 2 (Vista Piscina) está disponible."
    else:
        return False, "❌ No hay disponibilidad."

def is_apartment_available(conn, apartment_type, check_in, check_out):
    """Verifica si un apartamento está disponible en las fechas indicadas."""
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bookings 
                      WHERE apartment_type = ? 
                      AND status = "confirmed"
                      AND ((check_in <= ? AND check_out >= ?)
                      OR (check_in <= ? AND check_out >= ?))''',
                  (apartment_type, check_out, check_in, check_in, check_out))
    return len(cursor.fetchall()) == 0