import os
from google.cloud import speech_v1p1beta1 as speech
import logging
from transformers import pipeline
from datetime import datetime
import sqlite3
import time
import random

# ================= CONFIGURACIÓN DE LOGGING =================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot_errors.log'),
        logging.StreamHandler()
    ]
)

# ================= CONFIGURACIÓN INICIAL =================
LANGUAGE_CONFIG = {
    "es": {
        "intent_model": "dccuchile/bert-base-spanish-wwm-cased",
        "ner_model": "mrm8488/bert-spanish-cased-finetuned-ner",
        "responses": {
            "welcome": "¡Hola {name}! Soy tu asistente de Curacao Vacaciones. 🌴",
            "menu": "¿En qué puedo ayudarte hoy?\n1. 🏠 Ver apartamentos\n2. 📅 Hacer reserva\n3. 🎉 Promociones\n4. 📞 Contactar asesor\n5. 🌐 Cambiar idioma\n6. ❌ Salir",
            "apartamentos": (
               "🏠 *Tipos de Apartamentos Disponibles:*\n\n"
                "1. **🌊 Cerca a las mejores playas de la isla**\n"
                "   - 🛌 Capacidad: 4 huéspedes\n"
                "   - 💲 Precio: $110/noche\n"
                "   - 📍 Ubicación: Bandabou-Curacao\n"
                "   - 🚶 Acceso directo a la playa 🏖️ (5 minutos caminando)\n"
                
                "   - 🛎️ Servicios incluidos:\n"
                "     • Wi-Fi de alta velocidad\n"
                "     • Estacionamiento privado\n"
                "     • Acceso a piscina\n\n"
                
                "2. **🌟 Apartamento 1 **\n"
                "   - 🛌 Capacidad: 4 huéspedes\n"
                "   - 💲 Precio: $110/noche\n"
                "   - 📍 Ubicación: Zona VIP con vista panorámica\n\n"
                
                "  **🌟 Apartamento 2 **\n"
                "   - 🛌 Capacidad: 4 huéspedes\n"
                "   - 💲 Precio: $110/noche\n"
                "   - 📍 Ubicación: Zona VIP con vista Piscina\n\n"
                
                "**🏡 Cada Apartamento Ofrece:**\n\n"
                "🛁 *Baño:*\n"
                "  - Productos de limpieza\n"
                "  - Set de toallas piscina o playa\n"
                
                "  - Ducha interior & exterior\n\n"
                "🛏️ *Dormitorio:*\n"
                
                "  - Sábanas de algodón\n"
                "  - Armario con sistema de organización\n"
                "  - Cortinas blackout\n\n"
                
                "🍳 *Cocina Equipada:*\n"
                "  - Electrodomésticos\n"
                "  - Vajilla completa para 4 personas\n"
                "  - Set de parrilla profesional\n"
                "  - Cafetera, arrocera, microondas, nevera, estufa\n\n"
                
                "🔒 *Seguridad:*\n"
                "  - Sistema de cámaras\n"
                "  - Botiquín de primeros auxilios\n\n"
                
                "🌴 *Áreas Externas:*\n"
                "  - Balcon privado\n"
                "  - Zona de parrilla con asador\n"
                "  - Piscina\n\n"
                
                "💻 *Conectividad:*\n"
                "  - WiFi\n"
                "  - Smart TV con Netflix Premium, Amazon Prime\n\n"
                
                "🚗 *Estacionamiento:*\n"
                "  - 2 plazas cubiertas por apartamento\n\n"
                
                "🎁 *Servicios Adicionales:*\n"
                "  - Recepción personalizada en el Aereopuerto\n"
                "  - Limpieza diaria (opcional+costo adicional)\n\n"
                
                "📸 Ver fotos: https://www.airbnb.com.co/rooms/1329169006531801279?viralityEntryPoint=1&unique_share_id=5BA2AE9E-6929-4556-9DB7-20ED1EFD7840&slcid=6d65e69435364e5dacb58f3ab98da665&s=76&feature=share&adults=1&channel=native&slug=0kokhOSh&_set_bev_on_new_domain=1738712838_EAZDFhYTg2MmJhYT&source_impression_id=p3_1738712838_P3oLmzpLklPLMj-h\n\n"
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
                "❌ *Fechas No Disponibles*\n\n"
                "📅 Fechas solicitadas: {date}\n\n"
                "ℹ️ Por favor, intenta con otras fechas."
            ),
            "promociones": "🎉 Promoción activa: VERANO24 (20% OFF en estancias >7 noches)",
            "contact_info": "📞 Contacto directo: +5999-765-4321 (WhatsApp)",
            "error_audio": "🔇 No pude entender el audio",
            "date_format_help": (
                "🗓️ *Formato Requerido:*\n"
                "**YYYY-MM-DD a YYYY-MM-DD**\n"
                "Ejemplo: 2024-12-01 a 2024-12-10"
            )
        }
    },
    "en": {
        "intent_model": "bert-base-uncased",
        "ner_model": "dslim/bert-base-NER",
        "responses": {
            "welcome": "Hello {name}! I'm your Curacao Vacations assistant. 🌴",
            "menu": "How can I help you?\n1. 🌊 View apartments\n2. 📅 Make booking\n3. 🎉 Promotions\n4. 📞 Contact agent\n5. 🌐 Change language\n6. ❌ Exit",
            "apartamentos": (
                "🏠 *Apartment Types:*\n\n"
                "1. **🌊 Beachfront**\n"
                "   - 💲 Price: $110/night\n\n"
                "2. **🌟 Pool View**\n"
                "   - 💲 Price: $110/night\n\n"
                "🛌 Capacity: 4 guests • 🏊 Pool • 📶 WiFi"
            ),
            "reserva_pending": (
                "⏳ *Pre-Booking Registered*\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Dates: {date}\n"
                "💲 Total: ${price}\n\n"
                "ℹ️ Checking availability on Airbnb/Booking..."
            ),
            "reserva_confirmed": (
                "✅ *Dates Available!*\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Dates: {date}\n"
                "💲 Total: ${price}\n\n"
                "📞 An agent will contact you to finalize payment."
            ),
            "reserva_rejected": (
                "❌ *Dates Not Available*\n\n"
                "📅 Requested dates: {date}\n\n"
                "ℹ️ Please try different dates."
            ),
            "promociones": "🎉 Active promotion: SUMMER24 (20% OFF stays >7 nights)",
            "contact_info": "📞 Direct contact: +5999-765-4321 (WhatsApp)",
            "error_audio": "🔇 Couldn't understand audio",
            "date_format_help": (
                "🗓️ *Required Format:*\n"
                "**YYYY-MM-DD to YYYY-MM-DD**\n"
                "Example: 2024-12-01 to 2024-12-10"
            )
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
                        dates TEXT,
                        name TEXT,
                        apartment_type TEXT,
                        price REAL,
                        status TEXT DEFAULT 'pending')''')
        self.db_conn.commit()

    def _load_models(self):
        config = LANGUAGE_CONFIG[self.language]
        self.intent_classifier = pipeline(
            "text-classification", 
            model=config["intent_model"]
        )
        self.ner_model = pipeline(
            "ner", 
            model=config["ner_model"]
        )

    def _get_response(self, key):
        return LANGUAGE_CONFIG[self.language]["responses"][key]

    def _validate_dates(self, date_str):
        try:
            separator = " a " if self.language == "es" else " to "
            if separator not in date_str:
                return False, self._get_response("date_format_help")
            
            check_in, check_out = date_str.split(separator)
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
            
            if check_in_date >= check_out_date:
                error_msg = "❌ Error: Fecha salida debe ser posterior" if self.language == "es" else "❌ Error: Check-out must be after check-in"
                return False, error_msg
                
            if check_in_date < datetime.now():
                error_msg = "❌ Error: No se permiten fechas pasadas" if self.language == "es" else "❌ Error: Past dates not allowed"
                return False, error_msg
                
            return True, (check_in, check_out)
            
        except ValueError:
            return False, self._get_response("date_format_help")

    def _check_availability(self):
        """Simula verificación en Airbnb/Booking"""
        print("\n🔍 Consultando disponibilidad...")
        time.sleep(3)
        return random.random() < 0.8  # 80% de disponibilidad

    def _handle_booking(self):
        try:
            # Mostrar formato de fechas
            print("\n" + "="*50)
            print(self._get_response("date_format_help"))
            print("="*50 + "\n")
            
            # Obtener fechas
            date_prompt = "📅 Ingrese las fechas (check-in a check-out): " if self.language == "es" else "📅 Enter dates (check-in to check-out): "
            date_input = input(date_prompt).strip()
            
            if not date_input:
                return "❌ Error: Ingrese fechas válidas" if self.language == "es" else "❌ Error: Enter valid dates"
            
            # Validar fechas
            is_valid, result = self._validate_dates(date_input)
            if not is_valid:
                return result
            check_in, check_out = result
            
            # Seleccionar apartamento
            print("\n" + self._get_response("apartamentos"))
            apartment_type = input("\n🔍 Elige el Número de apartamento (1) vista al mar (2) vista a la piscina (1-2): " if self.language == "es" else "\n🔍 Choose Apartment number (1-2): ").strip()
            
            if apartment_type not in ["1", "2"]:
                return "❌ Debes seleccionar 1 ó 2" if self.language == "es" else "❌ Please select 1 or 2"
            
            # Calcular precio
            nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
            price = 110 * nights
            
            # Confirmar
            confirm_msg = f"\n💲 Total: ${price} | ¿Confirmar pre-reserva? (s/n): " if self.language == "es" else f"\n💲 Total: ${price} | Confirm pre-booking? (y/n): "
            if input(confirm_msg).lower() not in ["s", "y"]:
                return "🚫 Operación cancelada" if self.language == "es" else "🚫 Operation canceled"
            
            # Registrar en DB
            booking_id = f"PRE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            cursor = self.db_conn.cursor()
            cursor.execute('''INSERT INTO bookings 
                            (id, dates, name, apartment_type, price) 
                            VALUES (?, ?, ?, ?, ?)''',
                         (booking_id, f"{check_in} a {check_out}", 
                          self.user_name, 
                          "Frente al Mar" if apartment_type == "1" else "Vista Piscina",
                          price))
            self.db_conn.commit()
            
            # Verificar disponibilidad
            is_available = self._check_availability()
            status = "confirmed" if is_available else "rejected"
            cursor.execute('''UPDATE bookings SET status = ? WHERE id = ?''', (status, booking_id))
            self.db_conn.commit()
            
            # Notificar
            if is_available:
                return self._get_response("reserva_confirmed").format(
                    booking_id=booking_id,
                    date=f"{check_in} a {check_out}",
                    price=price
                )
            else:
                return self._get_response("reserva_rejected").format(
                    date=f"{check_in} a {check_out}"
                )
                
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return "❌ Error en el proceso" if self.language == "es" else "❌ Process error"

    def run(self):
        print("\n" + "="*50)
        print("  🌴 CUACAO VACACIONES - ASISTENTE VIRTUAL  " if self.language == "es" else "  🌴 CUACAO VACATIONS - VIRTUAL ASSISTANT  ")
        print("="*50)
        
        # Configurar idioma
        lang_choice = input("\n🌐 Seleccione idioma/Select language (1=ES/2=EN): ")
        self.language = "es" if lang_choice == "1" else "en"
        self._load_models()
        
        # Obtener nombre
        name_prompt = "\n👤 Ingrese su nombre: " if self.language == "es" else "\n👤 Enter your name: "
        self.user_name = input(name_prompt)
        print("\n" + self._get_response("welcome").format(name=self.user_name))
        
        # Bucle principal
        while True:
            print("\n" + self._get_response("menu"))
            choice = input("\n➡️  Seleccione una opción: " if self.language == "es" else "\n➡️  Enter option: ").lower()
            
            if choice in ["6", "salir", "exit"]:
                print("\n🌞 ¡Gracias por preferirnos!" if self.language == "es" else "\n🌞 Thank you for choosing us!")
                break
                
            elif choice in ["5", "cambiar idioma", "change language"]:
                self.language = "en" if self.language == "es" else "es"
                self._load_models()
                print("\n✅ Idioma actualizado!" if self.language == "es" else "\n✅ Language updated!")
                
            elif choice in ["1", "ver apartamentos", "view apartments"]:
                print("\n" + self._get_response("apartamentos"))
                
            elif choice in ["2", "reservar", "book"]:
                print("\n" + self._handle_booking())
                
            elif choice in ["3", "promociones", "promotions"]:
                print("\n" + self._get_response("promociones"))
                
            elif choice in ["4", "contactar asesor", "contact agent"]:
                print("\n" + self._get_response("contact_info"))
                
            else:
                print("\n" + self._get_response("contact_info"))

if __name__ == "__main__":
    Chatbot().run()