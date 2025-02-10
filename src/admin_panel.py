import getpass
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import bcrypt
import os

# Cargar variables de entorno
load_dotenv()

def admin_auth():
    """Autentica al administrador usando credenciales almacenadas en .env."""
    print("\n🔒 Panel de Administración")
    user = input("Usuario: ").strip()
    password = getpass.getpass("Contraseña: ").strip().encode()  # Convertimos la contraseña ingresada a bytes
    
    # Obtener hash desde .env y asegurarnos de que se convierta correctamente a bytes
    stored_hash = os.getenv("ADMIN_PASSWORD_HASH")
    
    if stored_hash is None:
        print("❌ Error: ADMIN_PASSWORD_HASH no está definido en .env")
        return False
    
    stored_hash = stored_hash.encode()  # Convertimos el hash almacenado a bytes
    
    # Verificar usuario y contraseña
    if user == os.getenv("ADMIN_USER") and bcrypt.checkpw(password, stored_hash):
        print("✅ Acceso concedido")
        return True
    else:
        print("❌ Acceso denegado")
        return False

def show_all_bookings(conn):
    """Muestra todas las reservas en la base de datos."""
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bookings ORDER BY check_in''')
    bookings = cursor.fetchall()
    
    if not bookings:
        print("\n📭 No hay reservas registradas")
        return
        
    print("\n📋 *Todas las Reservas:*")
    for b in bookings:
        print(f"\nID: {b[0]}")
        print(f"📅 Fechas: {b[1]} a {b[2]}")
        print(f"👤 Cliente: {b[3]} | 📞 Teléfono: {b[4]}")
        print(f"🏠 Tipo: {b[5]} | 💲 Precio: ${b[6]}")
        print(f"🔄 Estado: {b[7]}")

def show_calendar(conn):
    """Muestra un calendario de disponibilidad."""
    try:
        month_year = input("\n📅 Mes a consultar (MM/AAAA): ").strip()
        target = datetime.strptime(month_year, "%m/%Y")
        start = target.replace(day=1)
        end = (start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        
        dates = pd.date_range(start, end)
        calendar = pd.DataFrame(index=dates, columns=["Frente al Mar", "Vista Piscina"])
        calendar.fillna("🟢 Libre", inplace=True)
        
        cursor = conn.cursor()
        cursor.execute('''SELECT check_in, check_out, apartment_type 
                        FROM bookings WHERE status = "confirmed"''')
        for check_in, check_out, apt_type in cursor.fetchall():
            col = 0 if apt_type == "Frente al Mar" else 1
            for date in pd.date_range(check_in, check_out):
                if date in calendar.index:
                    calendar.iloc[calendar.index.get_loc(date), col] = "🔴 Ocupado"
        
        print("\n📅 Calendario de Disponibilidad:")
        print(calendar.to_markdown(tablefmt="grid", headers="keys"))
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def add_manual_booking(conn):
    """Permite al administrador agregar una reserva manualmente."""
    try:
        print("\n📝 *Agregar Reserva Manual*")
        booking_id = input("ID de la reserva: ").strip()
        check_in = input("Check-in (YYYY-MM-DD): ").strip()
        check_out = input("Check-out (YYYY-MM-DD): ").strip()
        apt_type = input("Tipo (1=Frente al Mar, 2=Vista Piscina): ").strip()
        apt_name = "Frente al Mar" if apt_type == "1" else "Vista Piscina"
        price = float(input("Precio total: $").strip())
        client_name = input("Nombre del cliente: ").strip()
        client_phone = input("Teléfono del cliente: ").strip()
        
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO bookings 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (booking_id, check_in, check_out, client_name, 
                        client_phone, apt_name, price, "confirmed"))
        conn.commit()
        print("✅ Reserva agregada!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def cancel_booking(conn):
    """Permite al administrador cancelar una reserva."""
    try:
        print("\n🗑️ *Cancelar Reserva*")
        booking_id = input("ID de la reserva: ").strip()
        
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM bookings WHERE id = ?''', (booking_id,))
        if cursor.rowcount == 0:
            print("❌ Reserva no encontrada.")
        else:
            conn.commit()
            print("✅ Reserva cancelada!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def confirmar_pago_manual(conn):
    """Permite al administrador confirmar un pago manualmente."""
    try:
        print("\n" + "="*50)
        print("✅ *CONFIRMAR PAGO MANUAL*")
        booking_id = input("🔍 Ingrese el ID de reserva: ").strip()
        
        cursor = conn.cursor()
        cursor.execute('''SELECT client_name, client_phone, check_in, check_out, apartment_type, price 
                        FROM bookings WHERE id = ? AND status = "pending"''', (booking_id,))
        reserva = cursor.fetchone()
        
        if not reserva:
            print("\n❌ Reserva no encontrada o ya confirmada")
            return
            
        cursor.execute('''UPDATE bookings SET status = "confirmed" WHERE id = ?''', (booking_id,))
        conn.commit()
        
        client_name, client_phone, check_in, check_out, apt_type, price = reserva
        
        mensaje = f'''
🎉 *¡PAGO CONFIRMADO!*  

Hola {client_name},  
Tu reserva *{booking_id}* está oficialmente activa.  

📅 *Fechas:* {check_in} a {check_out}  
🏠 *Apartamento:* {apt_type}  
💸 *Total pagado:* ${price}  

📲 *Próximos pasos:*  
1. Recibirás un mensaje de WhatsApp 48h antes del check-in  
2. Presenta tu DNI/pasaporte al llegar  
3. ¡Disfruta de tu estadía! 🌴✨

*¿Preguntas?* Responde a este mensaje.  
'''
        print("\n" + "="*50)
        print(f"📤 Notificación para {client_name} ({client_phone}):")
        print(mensaje)
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
def show_all_bookings(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bookings ORDER BY check_in''')
    bookings = cursor.fetchall()
    
    if not bookings:
        print("\n📭 No hay reservas registradas")
        return
        
    print("\n📋 *Todas las Reservas:*")
    for b in bookings:
        print(f"\nID: {b[0]}")
        print(f"📅 Fechas: {b[1]} a {b[2]}")
        print(f"👤 Cliente: {b[3]} | 📞 Teléfono: {b[4]}")
        print(f"🏠 Tipo: {b[5]} | 💲 Precio: ${b[6]}")
        print(f"🔄 Estado: {b[7]}")