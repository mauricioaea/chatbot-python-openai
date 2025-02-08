import os
import sqlite3
import logging
import getpass
import time
from datetime import datetime, timedelta
from transformers import pipeline
import pandas as pd

# Eliminar la base de datos existente si es necesario
if os.path.exists("reservas.db"):
    os.remove("reservas.db")

# ================= CONFIGURACIÓN DE LOGGING =================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot_errors.log'),
        logging.StreamHandler()
    ]
)

# ================= CONFIGURACIÓN ADMIN =================
ADMIN_USERNAME = "admin_curacao"
ADMIN_PASSWORD = "clave_secreta_123"

# ================= CONFIGURACIÓN INICIAL =================
LANGUAGE_CONFIG = {
    "es": {
        "intent_model": "dccuchile/bert-base-spanish-wwm-cased",
        "ner_model": "mrm8488/bert-spanish-cased-finetuned-ner",
        "responses": {
            "welcome": "¡Hola {name}! Soy tu asistente de Curacao Vacaciones. 🌴",
            "menu": (
                "¿En qué puedo ayudarte hoy?\n\n"
                "1. 🏠 Ver apartamentos\n"
                "2. 📅 Hacer reserva\n"
                "3. 🎉 Promociones\n"
                "4. 📞 Contactar asesor\n"
                "5. 🌐 Cambiar idioma\n"
                "6. ❌ Salir"
            ),
            "apartamentos": (
                "🏠 *Tipos de Apartamentos Disponibles:*\n\n"
                "1. **🌊 Cerca a las mejores playas de la isla**\n"
                "   - 🛌 Capacidad: 4 huéspedes\n"
                "   - 💲 Precio: $110/noche\n"
                "   - 📍 Ubicación: Bandabou-Curacao\n"
                "   - 🚶 Acceso directo a la playa 🏖️ (5 minutos caminando)\n\n"
                "2. **🌟 Vista Piscina**\n"
                "   - 🛌 Capacidad: 4 huéspedes\n"
                "   - 💲 Precio: $110/noche\n"
                "   - 📍 Ubicación: Zona VIP\n\n"
                "**🏡 Servicios Incluidos:** WiFi • Piscina • Estacionamiento • Netflix"
            ),
            "reserva_pending": (
                "⏳ *Pre-Reserva Registrada*\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Fechas: {date}\n"
                "💲 Total: ${price}\n\n"
                "ℹ️ Verificando disponibilidad en Airbnb/Booking..."
            ),
            "reserva_confirmed": (
                "✅ *¡Fechas Disponibles!*\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Fechas: {date}\n"
                "💲 Total: ${price}\n\n"
                "📞 Un asesor se contactará para finalizar el pago."
            ),
            "reserva_rejected": (
                "❌ *No hay disponibilidad en las fechas seleccionadas.*\n\n"
                "ℹ️ Por favor, intente con otras fechas o elija otro apartamento."
            ),
            "promociones": "🎉 VERANO24: 20% OFF en estancias >7 noches",
            "contact_info": "📞 Contacto directo: +5999-765-4321 (WhatsApp)",
            "date_format_help": "🗓️ Formato: YYYY-MM-DD a YYYY-MM-DD\nEj: 2024-12-01 a 2024-12-10"
        }
    }
}

class Chatbot:
    def __init__(self):
        self.language = "es"
        self.user_name = ""
        self.db_conn = sqlite3.connect('reservas.db')
        self._init_db()
        self._load_models()

    def _init_db(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                        id TEXT PRIMARY KEY,
                        check_in DATE,
                        check_out DATE,
                        name TEXT,
                        apartment_type TEXT,
                        price REAL,
                        status TEXT)''')
        self.db_conn.commit()

    def _load_models(self):
        config = LANGUAGE_CONFIG[self.language]
        self.intent_classifier = pipeline(
            "text-classification", 
            model=config["intent_model"]
        )

    def _get_response(self, key):
        return LANGUAGE_CONFIG[self.language]["responses"][key]

    def _validate_dates(self, date_str):
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
            return False, self._get_response("date_format_help")

    def _check_availability(self, check_in, check_out):
        cursor = self.db_conn.cursor()
        
        # Verificar disponibilidad de ambos apartamentos
        apt1_available = self._is_apartment_available("Frente al Mar", check_in, check_out)
        apt2_available = self._is_apartment_available("Vista Piscina", check_in, check_out)
        
        if apt1_available and apt2_available:
            return True, "Ambos apartamentos están disponibles."
        elif apt1_available:
            return True, "El apartamento 1 (Frente al Mar) está disponible."
        elif apt2_available:
            return True, "El apartamento 2 (Vista Piscina) está disponible."
        else:
            return False, "❌ No hay disponibilidad en las fechas seleccionadas. Intente con otras fechas."

    def _is_apartment_available(self, apartment_type, check_in, check_out):
        cursor = self.db_conn.cursor()
        cursor.execute('''SELECT * FROM bookings 
                          WHERE apartment_type = ? 
                          AND status = "confirmed"
                          AND ((check_in <= ? AND check_out >= ?)
                          OR (check_in <= ? AND check_out >= ?))''',
                      (apartment_type, check_out, check_in, check_in, check_out))
        return len(cursor.fetchall()) == 0

    def _handle_booking(self):
        try:
            # Paso 1: Obtener fechas
            print("\n" + "="*50)
            print(self._get_response("date_format_help"))
            print("="*50)
            
            date_input = input("\n📅 Ingrese fechas (check-in a check-out): ").strip()
            is_valid, result = self._validate_dates(date_input)
            if not is_valid:
                return result
            check_in, check_out = result
            
            # Paso 2: Verificar disponibilidad
            is_available, availability_msg = self._check_availability(check_in, check_out)
            print("\n" + availability_msg)
            
            if not is_available:
                return "ℹ️ Por favor, intente con otras fechas."
            
            # Paso 3: Seleccionar apartamento
            print("\n" + self._get_response("apartamentos"))
            apt_type = input("\n🔍 Elija apartamento (1/2): ").strip()
            if apt_type not in ["1", "2"]:
                return "❌ Opción inválida"
            apt_name = "Frente al Mar" if apt_type == "1" else "Vista Piscina"
            
            # Verificar disponibilidad del apartamento seleccionado
            if not self._is_apartment_available(apt_name, check_in, check_out):
                return f"❌ El apartamento {apt_type} no está disponible. Intente con el otro apartamento."
            
            # Paso 4: Confirmación
            nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
            price = 110 * nights
            
            if input(f"\n💲 Total: ${price} | ¿Confirmar? (s/n): ").lower() != "s":
                return "🚫 Reserva cancelada"
            
            # Registrar en DB
            booking_id = f"RES-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            cursor = self.db_conn.cursor()
            cursor.execute('''INSERT INTO bookings 
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                         (booking_id, check_in, check_out, self.user_name, 
                          apt_name, price, "confirmed"))
            self.db_conn.commit()
            
            return self._get_response("reserva_confirmed").format(
                booking_id=booking_id,
                date=f"{check_in} a {check_out}",
                price=price
            )
            
        except Exception as e:
            logging.error(f"Error en reserva: {str(e)}")
            return "❌ Error en el proceso"

    # ================= ADMIN PANEL =================
    def _admin_auth(self):
        print("\n🔒 Panel de Administración")
        user = input("Usuario: ").strip()
        password = getpass.getpass("Contraseña: ").strip()
        return user == ADMIN_USERNAME and password == ADMIN_PASSWORD

    def _admin_menu(self):
        while True:
            print("\n🛠️ Menú de Administración")
            print("1. Ver todas las reservas")
            print("2. Calendario de disponibilidad")
            print("3. Agregar reserva manualmente")
            print("4. Cancelar reserva")
            print("5. Salir")
            choice = input("\n➡️  Opción: ").strip()
            
            if choice == "5":
                break
            elif choice == "1":
                self._show_all_bookings()
            elif choice == "2":
                self._show_calendar()
            elif choice == "3":
                self._add_manual_booking()
            elif choice == "4":
                self._cancel_booking()
            else:
                print("❌ Opción inválida")

    def _show_all_bookings(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''SELECT * FROM bookings ORDER BY check_in''')
        bookings = cursor.fetchall()
        
        if not bookings:
            print("\n📭 No hay reservas registradas")
            return
            
        print("\n📋 *Todas las Reservas:*")
        for b in bookings:
            print(f"\nID: {b[0]}")
            print(f"Check-in: {b[1]} | Check-out: {b[2]}")
            print(f"Tipo: {b[4]}")
            print(f"Precio: ${b[5]} | Estado: {b[6]}")
            print(f"Cliente: {b[3]}")

    def _show_calendar(self):
        try:
            month_year = input("\n📅 Mes a consultar (MM/AAAA): ").strip()
            target = datetime.strptime(month_year, "%m/%Y")
            start = target.replace(day=1)
            end = (start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            
            dates = pd.date_range(start, end)
            calendar = pd.DataFrame(index=dates, columns=["Frente al Mar", "Vista Piscina"])
            calendar.fillna("🟢 Libre", inplace=True)
            
            cursor = self.db_conn.cursor()
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

    def _add_manual_booking(self):
        try:
            print("\n📝 *Agregar Reserva Manual*")
            booking_id = input("ID de la reserva: ").strip()
            check_in = input("Fecha check-in (YYYY-MM-DD): ").strip()
            check_out = input("Fecha check-out (YYYY-MM-DD): ").strip()
            apt_type = input("Tipo de apartamento (1=Frente al Mar, 2=Vista Piscina): ").strip()
            apt_name = "Frente al Mar" if apt_type == "1" else "Vista Piscina"
            price = float(input("Precio total: ").strip())
            status = "confirmed"
            
            cursor = self.db_conn.cursor()
            cursor.execute('''INSERT INTO bookings 
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (booking_id, check_in, check_out, "Administración", 
                            apt_name, price, status))
            self.db_conn.commit()
            print("✅ Reserva agregada exitosamente!")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    def _cancel_booking(self):
        try:
            print("\n🗑️ *Cancelar Reserva*")
            booking_id = input("Ingrese el ID de la reserva a cancelar: ").strip()
            
            cursor = self.db_conn.cursor()
            cursor.execute('''DELETE FROM bookings WHERE id = ?''', (booking_id,))
            if cursor.rowcount == 0:
                print("❌ No se encontró la reserva.")
            else:
                self.db_conn.commit()
                print("✅ Reserva cancelada exitosamente!")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    # ================= MAIN FLOW =================
    def run(self):
        print("\n" + "="*50)
        print("  🌴 CUACAO VACACIONES - ASISTENTE VIRTUAL  ")
        print("="*50)
        
        # Configurar idioma
        lang = input("\n🌐 Idioma/Idioma (1=ES/2=EN): ").strip()
        self.language = "es" if lang == "1" else "en"
        self._load_models()
        
        # Obtener nombre
        self.user_name = input("\n👤 Ingrese su nombre: ").strip()
        print("\n" + self._get_response("welcome").format(name=self.user_name))
        
        # Bucle principal
        while True:
            print("\n" + self._get_response("menu"))
            user_input = input("\n➡️  Seleccione opción: ").strip().lower()
            
            # Comando secreto admin
            if user_input == "/admin" and self._admin_auth():
                self._admin_menu()
                continue
                
            if user_input in ["6", "salir"]:
                print("\n🌞 ¡Gracias por preferirnos!")
                break
                
            elif user_input in ["1", "ver apartamentos"]:
                print("\n" + self._get_response("apartamentos"))
                
            elif user_input in ["2", "reservar"]:
                print("\n" + self._handle_booking())
                
            elif user_input in ["3", "promociones"]:
                print("\n" + self._get_response("promociones"))
                
            elif user_input in ["4", "contactar asesor"]:
                print("\n" + self._get_response("contact_info"))
                
            else:
                print("\nℹ️ Ingrese una opción válida")

if __name__ == "__main__":
    Chatbot().run()