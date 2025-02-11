import logging
import os
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
            print("\n" + "="*50)
            print(self._get_response("date_format_help"))
            date_input = input("\n" + self._get_response("date_input_prompt")).strip()
            is_valid, result = validate_dates(date_input)
            if not is_valid:
                return result
            check_in, check_out = result

            is_available, msg = check_availability(self.db_conn, check_in, check_out)
            print("\n" + msg)
            if not is_available:
                return self._get_response("reserva_rejected")

            print("\n" + self._get_response("apartamentos"))
            apt_type = input("\n" + self._get_response("apartment_choice_prompt")).strip()
            if apt_type not in ["1", "2"]:
                return self._get_response("invalid_option")
            
            apt_name = self._get_response("apartment1_name") if apt_type == "1" else self._get_response("apartment2_name")

            if not is_apartment_available(self.db_conn, apt_name, check_in, check_out):
                return self._get_response("apartment_unavailable").format(apt_type=apt_type)

            nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
            price = 110 * nights
            
            # ========== SECCIÓN CORREGIDA ==========
            confirm_char = self._get_response("confirmation_character").lower()
            user_input = input(f"\n💲 {self._get_response('total_price')} ${price} | {self._get_response('confirmation_prompt')} ").lower()
            
            if user_input != confirm_char:
                return self._get_response("booking_cancelled")
            # ========================================

            client_name = input("\n" + self._get_response("client_name_prompt")).strip()
            client_phone = input("\n" + self._get_response("client_phone_prompt")).strip()

            if not validate_phone(client_phone):
                return self._get_response("invalid_phone")

            client_phone_encrypted = encrypt_data(client_phone)

            booking_id = f"RES-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            cursor = self.db_conn.cursor()
            cursor.execute('''INSERT INTO bookings 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                        (booking_id, check_in, check_out, client_name, 
                        client_phone_encrypted, apt_name, price, "pending"))
            self.db_conn.commit()

            paypal_link = f"https://www.paypal.com/paypalme/CuracaoVacaciones/{booking_id}"
            whatsapp_link = f"https://wa.me/+59995153955?text={self._get_response('whatsapp_message').format(booking_id=booking_id)}"

            print(f"\n{'='*50}")
            print(self._get_response("booking_success").format(
                client_name=client_name,
                paypal_link=paypal_link,
                whatsapp_link=whatsapp_link
            ))

            return self._get_response("reserva_pending").format(
                booking_id=booking_id,
                date=f"{check_in} {self._get_response('to')} {check_out}",
                price=price
            )

        except Exception as e:
            logging.error(f"Error en reserva: {str(e)}")
            return self._get_response("booking_error")

    def show_location(self):
        lat, lon = "12.3665255", "-69.1536117"
        maps_url = f"https://www.google.com/maps?q={lat},{lon}"
        
        print("\n" + self._get_response("location_prompt"))
        choice = input("\n" + self._get_response("location_choice_prompt")).strip()
        
        if choice == "1":
            print(f"\n{self._get_response('location_response').format(maps_url=maps_url)}")

    def contact_advisor(self):
        print("\n" + self._get_response("contact_info"))

    def change_language(self):
        print("\n🌐 Seleccione un idioma / Select a language:")
        print("[1] Español")
        print("[2] English")
        print("[3] Português")
        print("[4] Nederlands")
        choice = input("Seleccione una opción / Select an option: ").strip()
        
        lang_map = {"1": "es", "2": "en", "3": "pt", "4": "nl"}
        if choice in lang_map:
            self.language = lang_map[choice]
            self._load_models()
            print(f"\n✅ {self._get_response('language_changed')}")
        else:
            print("\n❌", self._get_response("invalid_option"))

    def _handle_apartments(self):
        print("\n" + self._get_response("apartamentos"))
        
        while True:
            print("\n" + self._get_response("apartment_images_prompt"))
            print("[1] " + self._get_response("view_apartment1_images"))
            print("[2] " + self._get_response("view_apartment2_images"))
            print("[3] " + self._get_response("return_to_menu"))
            choice = input("\n➡️  " + self._get_response("option_prompt")).strip()

            if choice == "1":
                print("\n🌅 " + self._get_response("view_apartment1_images") + ":")
                print("🔗 Enlace: https://photos.app.goo.gl/rWgd2LptUZJtP6cx9")
            elif choice == "2":
                print("\n🏊 " + self._get_response("view_apartment2_images") + ":")
                print("🔗 Enlace: https://photos.app.goo.gl/LRzbuEXNcDkyHQqTA")
            elif choice == "3":
                break
            else:
                print("\n❌ " + self._get_response("invalid_option"))

    def run(self):
        print("\n" + "="*50)
        print("  🌴 ROBBY APARTMENTS CURACAO - VIRTUAL ASSISTANT  ")
        print("="*50)

        print("\n🌐 " + self._get_response("initial_language_prompt"))
        print("[1] Español")
        print("[2] English")
        print("[3] Português")
        print("[4] Nederlands")
        lang_choice = input("➡️  " + self._get_response("language_input_prompt")).strip()
        
        lang_map = {"1": "es", "2": "en", "3": "pt", "4": "nl"}
        if lang_choice in lang_map:
            self.language = lang_map[lang_choice]
            self._load_models()
            print(f"\n✅ " + self._get_response("language_changed").format(language=self.language))
        else:
            print("\n❌ " + self._get_response("invalid_option"))
            return

        self.user_name = input("\n" + self._get_response("name_prompt")).strip()
        print("\n" + self._get_response("welcome").format(name=self.user_name))

        while True:
            print("\n" + self._get_response("menu"))
            choice = input("\n➡️  " + self._get_response("option_prompt")).strip().lower()

            if choice == "/admin":
                if admin_auth():
                    while True:
                        print("\n🛠️ " + self._get_response("admin_menu"))
                        print("1. Ver reservas")
                        print("2. Calendario")
                        print("3. Agregar reserva")
                        print("4. Cancelar reserva")
                        print("5. Confirmar pago manual")
                        print("6. Salir")
                        admin_choice = input("\n➡️  " + self._get_response("option_prompt")).strip()

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
                            print("\n❌ " + self._get_response("invalid_option"))
                continue

            if choice in ["7", "exit", "salir", "sair", "afsluiten"]:
                print("\n🌞 " + self._get_response("goodbye"))
                break
            elif choice in ["1", "ver apartamentos", "view apartments", "ver apartamentos", "appartementen bekijken"]:
                self._handle_apartments()
            elif choice in ["2", "reservar", "book", "reservar", "boeken"]:
                print("\n" + self._handle_booking())
            elif choice in ["3", "promociones", "promotions", "promoções", "aanbiedingen"]:
                print("\n" + self._get_response("promociones"))
            elif choice in ["4", "contactar asesor", "contact advisor", "contactar consultor", "contact opnemen"]:
                self.contact_advisor()
            elif choice in ["5", "cambiar idioma", "change language", "mudar idioma", "taal wijzigen"]:
                self.change_language()
            elif choice in ["6", "ver ubicación", "view location", "ver localização", "locatie bekijken"]:
                self.show_location()
            else:
                print("\nℹ️ " + self._get_response("invalid_option"))