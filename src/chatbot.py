import logging
from datetime import datetime
from transformers import pipeline
from .config import LANGUAGE_CONFIG
from .database import init_db, encrypt_data
from .booking_handler import validate_dates, check_availability, is_apartment_available, validate_phone
from .admin_panel import admin_auth, show_all_bookings, show_calendar, add_manual_booking, cancel_booking, confirmar_pago_manual

class Chatbot:
    def __init__(self):
        self.language = "es"
        self.user_name = ""
        self.db_conn = init_db()
        self._load_models()

    def _load_models(self):
        config = LANGUAGE_CONFIG[self.language]
        self.intent_classifier = pipeline(
            "text-classification", 
            model=config["intent_model"]
        )

    def _get_response(self, key):
        return LANGUAGE_CONFIG[self.language]["responses"][key]

    def _handle_booking(self):
        try:
            # Paso 1: Obtener fechas
            print("\n" + "="*50)
            print(self._get_response("date_format_help"))
            date_input = input("\n📅 Fechas (check-in a check-out): ").strip()
            is_valid, result = validate_dates(date_input)
            if not is_valid:
                return result
            check_in, check_out = result
            
            # Paso 2: Verificar disponibilidad
            is_available, msg = check_availability(self.db_conn, check_in, check_out)
            print("\n" + msg)
            if not is_available:
                return self._get_response("reserva_rejected")
            
            # Paso 3: Seleccionar apartamento
            print("\n" + self._get_response("apartamentos"))
            apt_type = input("\n🔍 Elija apartamento (1/2): ").strip()
            if apt_type not in ["1", "2"]:
                return "❌ Opción inválida"
            apt_name = "Frente al Mar" if apt_type == "1" else "Vista Piscina"
            
            if not is_apartment_available(self.db_conn, apt_name, check_in, check_out):
                return f"❌ Apartamento {apt_type} no disponible."
            
            # Paso 4: Confirmar reserva
            nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
            price = 110 * nights
            if input(f"\n💲 Total: ${price} | Confirmar? (s/n): ").lower() != "s":
                return "🚫 Reserva cancelada"
            
            # Paso 5: Obtener datos del cliente
            client_name = input("\n👤 Nombre completo del cliente: ").strip()
            client_phone = input("\n📞 Teléfono de contacto (ej: +584241234567): ").strip()
            
            # Validar teléfono
            if not validate_phone(client_phone):
                return "❌ Teléfono inválido. Use formato internacional: +584241234567"
            
            # Paso 6: Encriptar teléfono
            client_phone_encrypted = encrypt_data(client_phone)
            
            # Registrar en DB
            booking_id = f"RES-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            cursor = self.db_conn.cursor()
            cursor.execute('''INSERT INTO bookings 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                        (booking_id, check_in, check_out, client_name, 
                        client_phone_encrypted, apt_name, price, "pending"))
            self.db_conn.commit()
            
            # Paso 7: Mostrar opciones de pago
            paypal_link = f"https://www.paypal.com/paypalme/CuracaoVacaciones/{booking_id}"
            whatsapp_link = f"https://wa.me/+59995153955?text=¡Hola!%20👋%20Acabo%20de%20reservar%20{booking_id}%20y%20quiero%20enviar%20mi%20comprobante%20de%20pago"
            
            print(f"\n{'='*50}")
            print(f'''
🎉 *¡Reserva registrada exitosamente, {client_name}!*

👇 *Opciones para completar tu pago:*
[1️⃣] Pagar con PayPal: {paypal_link}
[2️⃣] Enviar comprobante de transferencia: {whatsapp_link}

📌 *Instrucciones importantes:*
• Si pagas con PayPal: La confirmación es automática
• Si pagas por otro medio: 
  1. Envía tu comprobante usando el botón [2️⃣]
  2. Validaremos tu pago en <24h
  3. Recibirás confirmación por WhatsApp

⏳ *Reserva activa por 48h*''')
            
            return self._get_response("reserva_pending").format(
                booking_id=booking_id,
                date=f"{check_in} a {check_out}",
                price=price
            )
            
        except Exception as e:
            logging.error(f"Error en reserva: {str(e)}")
            return "❌ Error en el proceso"

    def run(self):
        print("\n" + "="*50)
        print("  🌴 CUACAO VACACIONES - ASISTENTE VIRTUAL  ")
        print("="*50)
        
        # Configurar idioma
        lang = input("\n🌐 Idioma (1=ES/2=EN): ").strip()
        self.language = "es" if lang == "1" else "en"
        self._load_models()
        
        # Obtener nombre
        self.user_name = input("\n👤 Ingrese su nombre: ").strip()
        print("\n" + self._get_response("welcome").format(name=self.user_name))
        
        # Bucle principal
        while True:
            print("\n" + self._get_response("menu"))
            choice = input("\n➡️  Opción: ").strip().lower()
            
            if choice == "/admin" and admin_auth():
                while True:
                    print("\n🛠️ Menú de Administración")
                    print("1. Ver reservas\n2. Calendario\n3. Agregar reserva\n4. Cancelar reserva\n5. Confirmar pago manual\n6. Salir")
                    admin_choice = input("\n➡️  Opción: ").strip()
                    
                    if admin_choice == "6":
                        break
                    elif admin_choice == "1":
                        show_all_bookings(self.db_conn)
                    elif admin_choice == "2":
                        show_calendar(self.db_conn)
                    elif admin_choice == "3":
                        add_manual_booking(self.db_conn)
                    elif admin_choice == "4":
                        cancel_booking(self.db_conn)
                    elif admin_choice == "5":
                        confirmar_pago_manual(self.db_conn)
                    else:
                        print("❌ Opción inválida")
                continue
                
            if choice in ["6", "salir"]:
                print("\n🌞 ¡Gracias por preferirnos!")
                break
            elif choice in ["1", "ver apartamentos"]:
                print("\n" + self._get_response("apartamentos"))
            elif choice in ["2", "reservar"]:
                print("\n" + self._handle_booking())
            elif choice in ["3", "promociones"]:
                print("\n" + self._get_response("promociones"))
            elif choice in ["4", "contactar asesor"]:
                print("\n" + self._get_response("contact_info"))
            else:
                print("\nℹ️ Opción inválida")