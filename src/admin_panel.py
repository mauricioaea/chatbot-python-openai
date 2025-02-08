import getpass
import pandas as pd
from datetime import datetime, timedelta

def admin_auth():
    from .config import ADMIN_USERNAME, ADMIN_PASSWORD
    print("\n🔒 Panel de Administración")
    user = input("Usuario: ").strip()
    password = getpass.getpass("Contraseña: ").strip()
    return user == ADMIN_USERNAME and password == ADMIN_PASSWORD

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
        print(f"Check-in: {b[1]} | Check-out: {b[2]}")
        print(f"Tipo: {b[4]} | Precio: ${b[5]}")
        print(f"Estado: {b[6]}")

def show_calendar(conn):
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