import logging
from datetime import datetime

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
        "language_name": "Español",
        "intent_model": "dccuchile/bert-base-spanish-wwm-cased",
        "responses": {
            "welcome": "¡Hola {name}! Soy tu asistente de Robby Apartments Curacao. 🌴",
            "menu": (
                "¿En qué puedo ayudarte hoy?\n\n"
                "1. 🏠 Ver apartamentos\n"
                "2. 📅 Hacer reserva\n"
                "3. 🎉 Promociones\n"
                "4. 📞 Contactar asesor\n"
                "5. 🌐 Cambiar idioma\n"
                "6. 📍 Ver ubicación\n"
                "7. ❌ Salir"
            ),
            "apartamentos": (
                "🏠 *Tipos de Apartamentos Disponibles:*\n\n"
                "1. **🌊 Vista al Mar**\n"
                "   - 🛌 Capacidad: 4 huéspedes\n"
                "   - 💲 Precio: $110/noche\n"
                "   - 📍 Ubicación: Westpunt-Curacao\n\n"
                "2. **🌟 Vista Piscina**\n"
                "   - 🛌 Capacidad: 4 huéspedes\n"
                "   - 💲 Precio: $110/noche\n"
                "   - 📍 Ubicación: Zona VIP\n\n"
                "**🏡 Servicios Incluidos:** WiFi • Piscina • Estacionamiento • Netflix • Amazon Prime • Recojida en Aereopuerto Gratis"
            ),
            "apartment_images_prompt": "¿Qué te gustaría hacer?",
            "view_apartment1_images": "Ver imágenes del Apartamento 1 (Vista al Mar)",
            "view_apartment2_images": "Ver imágenes del Apartamento 2 (Vista Piscina)",
            "return_to_menu": "Volver al menú principal",
            "reserva_pending": (
                "⏳ *Reserva en Proceso* 🚀\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Fechas: {date}\n"
                "💲 Total: ${price}\n\n"
                "✅ Recibirás una confirmación por WhatsApp cuando todo esté listo."
            ),
            "reserva_confirmed": (
                "✅ *¡Reserva Confirmada!*\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Fechas: {date}\n"
                "💲 Total: ${price}\n\n"
                "📞 Un asesor se contactará para finalizar el pago."
            ),
            "reserva_rejected": "❌ No hay disponibilidad. Intente con otras fechas.",
            "promociones": "🎉 20% OFF en estancias >7 noches",
            "contact_info": "📞 Ayuda HUmana -> Angela esta disponible +5999-5153955 (WhatsApp)",
            "date_format_help": "🗓️ Formato: YYYY-MM-DD a YYYY-MM-DD\nEj: 2024-12-01 a 2024-12-10",
            "date_input_prompt": "📅 Fechas (check-in a check-out): ",
            "apartment_choice_prompt": "🔍 Elija apartamento (1/2): ",
            "total_price": "Total",
            "confirmation_prompt": "Confirmar? (s/n)",
            "confirmation_character": "s",
            "client_name_prompt": "👤 Nombre completo del cliente: ",
            "client_phone_prompt": "📞 Teléfono de contacto (ej: +584241234567): ",
            "invalid_option": "❌ Opción inválida",
            "apartment_unavailable": "❌ Apartamento {apt_type} no disponible.",
            "booking_cancelled": "🚫 Reserva cancelada",
            "invalid_phone": "❌ Teléfono inválido. Use formato internacional: +584241234567",
            "booking_success": (
                "🎉 *¡Reserva registrada exitosamente, {client_name}!*\n\n"
                "👇 *Opciones para completar tu pago:*\n"
                "[1️⃣] Pagar con PayPal: {paypal_link}\n"
                "[2️⃣] Enviar comprobante de transferencia: {whatsapp_link}\n\n"
                "📌 *Instrucciones importantes:*\n"
                "• Si pagas con PayPal: La confirmación es automática\n"
                "• Si pagas por otro medio:\n"
                "  1. Envía tu comprobante usando el botón [2️⃣]\n"
                "  2. Validaremos tu pago en <24h\n"
                "  3. Recibirás confirmación por WhatsApp\n\n"
                "⏳ *Reserva activa por 48h*"
            ),
            "booking_error": "❌ Error en el proceso",
            "location_prompt": "📍 ¿Deseas ver la ubicación en Google Maps?",
            "location_choice_prompt": "[1] Sí, ¡muéstrame!",
            "location_response": "🌍 Aquí está la ubicación: {maps_url}\n⛱️Estamos a 5 minutos de la playa.",
            "language_selection": "🌐 Seleccione un idioma:",
            "language_input_prompt": "Seleccione una opción: ",
            "language_changed": "Idioma cambiado a {language}.",
            "initial_language_prompt": "Por favor elija su idioma:",
            "name_prompt": "👤 Ingrese su nombre: ",
            "option_prompt": "Opción: ",
            "admin_menu": "Menú de Administración",
            "goodbye": "¡Gracias por preferirnos!",
            "apartment1_name": "Frente al Mar",
            "apartment2_name": "Vista Piscina",
            "to": "a",
            "whatsapp_message": "¡Hola! 👋 Acabo de reservar {booking_id} y quiero enviar mi comprobante de pago"
        }
    },
    "en": {
        "language_name": "English",
        "intent_model": "bert-base-uncased",
        "responses": {
            "welcome": "Hello {name}! I'm your assistant from Robby Apartments Curacao. 🌴",
            "menu": (
                "How can I assist you today?\n\n"
                "1. 🏠 View apartments\n"
                "2. 📅 Make a reservation\n"
                "3. 🎉 Promotions\n"
                "4. 📞 Contact advisor\n"
                "5. 🌐 Change language\n"
                "6. 📍 View location\n"
                "7. ❌ Exit"
            ),
            "apartamentos": (
                "🏠 *Available Apartment Types:*\n\n"
                "1. **🌊 Ocean View**\n"
                "   - 🛌 Capacity: 4 guests\n"
                "   - 💲 Price: $110/night\n"
                "   - 📍 Location: Westpunt-Curacao\n\n"
                "2. **🌟 Pool View**\n"
                "   - 🛌 Capacity: 4 guests\n"
                "   - 💲 Price: $110/night\n"
                "   - 📍 Location: VIP Zone\n\n"
                "**🏡 Included Services:** WiFi • Pool • Parking • Netflix"
            ),
            "apartment_images_prompt": "What would you like to do?",
            "view_apartment1_images": "View images of Apartment 1 (Ocean View)",
            "view_apartment2_images": "View images of Apartment 2 (Pool View)",
            "return_to_menu": "Return to main menu",
            "reserva_pending": (
                "⏳ *Reservation in Progress* 🚀\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Dates: {date}\n"
                "💲 Total: ${price}\n\n"
                "✅ You will receive a confirmation via WhatsApp when everything is ready."
            ),
            "reserva_confirmed": (
                "✅ *Reservation Confirmed!*\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Dates: {date}\n"
                "💲 Total: ${price}\n\n"
                "📞 An advisor will contact you to finalize the payment."
            ),
            "reserva_rejected": "❌ No availability. Please try different dates.",
            "promociones": "🎉 20% OFF for stays >7 nights",
            "contact_info": "📞 Human help -> Angela is available +5999-5153955 (WhatsApp)",
            "date_format_help": "🗓️ Format: YYYY-MM-DD to YYYY-MM-DD\nExample: 2024-12-01 to 2024-12-10",
            "date_input_prompt": "📅 Dates (check-in to check-out): ",
            "apartment_choice_prompt": "🔍 Choose apartment (1/2): ",
            "total_price": "Total",
            "confirmation_prompt": "Confirm? (y/n)",
            "confirmation_character": "y",
            "client_name_prompt": "👤 Full name: ",
            "client_phone_prompt": "📞 Contact phone (e.g., +584241234567): ",
            "invalid_option": "❌ Invalid option",
            "apartment_unavailable": "❌ Apartment {apt_type} not available.",
            "booking_cancelled": "🚫 Booking cancelled",
            "invalid_phone": "❌ Invalid phone. Use international format: +584241234567",
            "booking_success": (
                "🎉 *Booking successfully registered, {client_name}!*\n\n"
                "👇 *Payment options:*\n"
                "[1️⃣] Pay with PayPal: {paypal_link}\n"
                "[2️⃣] Send transfer receipt: {whatsapp_link}\n\n"
                "📌 *Important instructions:*\n"
                "• If you pay with PayPal: Confirmation is automatic\n"
                "• If you pay by other means:\n"
                "  1. Send your receipt using button [2️⃣]\n"
                "  2. We will validate your payment within <24h\n"
                "  3. You will receive confirmation via WhatsApp\n\n"
                "⏳ *Booking active for 48h*"
            ),
            "booking_error": "❌ Error in the process",
            "location_prompt": "📍 Would you like to see the location on Google Maps?",
            "location_choice_prompt": "[1] Yes, show me!",
            "location_response": "🌍 Here is the location: {maps_url}\n⛱️We are 5 minutes from the beach.",
            "language_selection": "🌐 Select a language:",
            "language_input_prompt": "Select an option: ",
            "language_changed": "Language changed to {language}.",
            "initial_language_prompt": "Please choose your language:",
            "name_prompt": "👤 Enter your name: ",
            "option_prompt": "Option: ",
            "admin_menu": "Admin Menu",
            "goodbye": "Thank you for choosing us!",
            "apartment1_name": "Ocean View",
            "apartment2_name": "Pool View",
            "to": "to",
            "whatsapp_message": "Hello! 👋 I just booked {booking_id} and want to send my payment receipt"
        }
    },
    "pt": {
        "language_name": "Português",
        "intent_model": "neuralmind/bert-base-portuguese-cased",
        "responses": {
            "welcome": "Olá {name}! Sou seu assistente do Robby Apartments Curacao. 🌴",
            "menu": (
                "Como posso ajudar hoje?\n\n"
                "1. 🏠 Ver apartamentos\n"
                "2. 📅 Fazer reserva\n"
                "3. 🎉 Promoções\n"
                "4. 📞 Contactar consultor\n"
                "5. 🌐 Mudar idioma\n"
                "6. 📍 Ver localização\n"
                "7. ❌ Sair"
            ),
            "apartamentos": (
                "🏠 *Tipos de Apartamentos Disponíveis:*\n\n"
                "1. **🌊 Vista para o Mar**\n"
                "   - 🛌 Capacidade: 4 hóspedes\n"
                "   - 💲 Preço: $110/noite\n"
                "   - 📍 Localização: Westpunt-Curacao\n\n"
                "2. **🌟 Vista para a Piscina**\n"
                "   - 🛌 Capacidade: 4 hóspedes\n"
                "   - 💲 Preço: $110/noite\n"
                "   - 📍 Localização: Zona VIP\n\n"
                "**🏡 Serviços Incluídos:** WiFi • Piscina • Estacionamento • Netflix"
            ),
            "apartment_images_prompt": "O que você gostaria de fazer?",
            "view_apartment1_images": "Ver imagens do Apartamento 1 (Vista para o Mar)",
            "view_apartment2_images": "Ver imagens do Apartamento 2 (Vista para a Piscina)",
            "return_to_menu": "Voltar ao menu principal",
            "reserva_pending": (
                "⏳ *Reserva em Processo* 🚀\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Datas: {date}\n"
                "💲 Total: ${price}\n\n"
                "✅ Você receberá uma confirmação por WhatsApp quando tudo estiver pronto."
            ),
            "reserva_confirmed": (
                "✅ *Reserva Confirmada!*\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Datas: {date}\n"
                "💲 Total: ${price}\n\n"
                "📞 Um consultor entrará em contato para finalizar o pagamento."
            ),
            "reserva_rejected": "❌ Não há disponibilidade. Tente outras datas.",
            "promociones": "🎉 20% OFF para estadias >7 noites",
            "contact_info": "📞 Ajuda humana -> Angela está disponível +5999-5153955 (WhatsApp)",
            "date_format_help": "🗓️ Formato: YYYY-MM-DD a YYYY-MM-DD\nExemplo: 2024-12-01 a 2024-12-10",
            "date_input_prompt": "📅 Datas (check-in a check-out): ",
            "apartment_choice_prompt": "🔍 Escolha apartamento (1/2): ",
            "total_price": "Total",
            "confirmation_prompt": "Confirmar? (s/n)",
            "confirmation_character": "s",
            "client_name_prompt": "👤 Nome completo: ",
            "client_phone_prompt": "📞 Telefone de contato (ex: +584241234567): ",
            "invalid_option": "❌ Opção inválida",
            "apartment_unavailable": "❌ Apartamento {apt_type} não disponível.",
            "booking_cancelled": "🚫 Reserva cancelada",
            "invalid_phone": "❌ Telefone inválido. Use formato internacional: +584241234567",
            "booking_success": (
                "🎉 *Reserva registrada com sucesso, {client_name}!*\n\n"
                "👇 *Opções para completar seu pagamento:*\n"
                "[1️⃣] Pagar com PayPal: {paypal_link}\n"
                "[2️⃣] Enviar comprovante de transferência: {whatsapp_link}\n\n"
                "📌 *Instruções importantes:*\n"
                "• Se pagar com PayPal: A confirmação é automática\n"
                "• Se pagar por outro meio:\n"
                "  1. Envie seu comprovante usando o botão [2️⃣]\n"
                "  2. Validaremos seu pagamento em <24h\n"
                "  3. Você receberá confirmação por WhatsApp\n\n"
                "⏳ *Reserva ativa por 48h*"
            ),
            "booking_error": "❌ Erro no processo",
            "location_prompt": "📍 Deseja ver a localização no Google Maps?",
            "location_choice_prompt": "[1] Sim, mostre-me!",
            "location_response": "🌍 Aqui está a localização: {maps_url}\n⛱️Estamos a 5 minutos da praia.",
            "language_selection": "🌐 Selecione um idioma:",
            "language_input_prompt": "Selecione uma opção: ",
            "language_changed": "Idioma alterado para {language}.",
            "initial_language_prompt": "Por favor, escolha seu idioma:",
            "name_prompt": "👤 Digite seu nome: ",
            "option_prompt": "Opção: ",
            "admin_menu": "Menu de Administração",
            "goodbye": "Obrigado por escolher-nos!",
            "apartment1_name": "Vista para o Mar",
            "apartment2_name": "Vista para a Piscina",
            "to": "a",
            "whatsapp_message": "Olá! 👋 Acabei de reservar {booking_id} e quero enviar meu comprovante de pagamento"
        }
    },
    "nl": {
        "language_name": "Nederlands",
        "intent_model": "wietsedv/bert-base-dutch-cased",
        "responses": {
            "welcome": "Hallo {name}! Ik ben uw assistent van Robby Apartments Curacao. 🌴",
            "menu": (
                "Hoe kan ik u helpen vandaag?\n\n"
                "1. 🏠 Appartementen bekijken\n"
                "2. 📅 Boek een reservering\n"
                "3. 🎉 Aanbiedingen\n"
                "4. 📞 Contact opnemen\n"
                "5. 🌐 Taal wijzigen\n"
                "6. 📍 Locatie bekijken\n"
                "7. ❌ Afsluiten"
            ),
            "apartamentos": (
                "🏠 *Beschikbare Appartementen:*\n\n"
                "1. **🌊 Zeezicht**\n"
                "   - 🛌 Capaciteit: 4 gasten\n"
                "   - 💲 Prijs: $110/nacht\n"
                "   - 📍 Locatie: Westpunt-Curacao\n\n"
                "2. **🌟 Zwembadzicht**\n"
                "   - 🛌 Capaciteit: 4 gasten\n"
                "   - 💲 Prijs: $110/nacht\n"
                "   - 📍 Locatie: VIP Zone\n\n"
                "**🏡 Inbegrepen Diensten:** WiFi • Zwembad • Parkeren • Netflix"
            ),
            "apartment_images_prompt": "Wat wilt u doen?",
            "view_apartment1_images": "Bekijk afbeeldingen van Appartement 1 (Zeezicht)",
            "view_apartment2_images": "Bekijk afbeeldingen van Appartement 2 (Zwembadzicht)",
            "return_to_menu": "Terug naar hoofdmenu",
            "reserva_pending": (
                "⏳ *Reservering in Behandeling* 🚀\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Data: {date}\n"
                "💲 Totaal: ${price}\n\n"
                "✅ U ontvangt een bevestiging via WhatsApp wanneer alles gereed is."
            ),
            "reserva_confirmed": (
                "✅ *Reservering Bevestigd!*\n\n"
                "📋 ID: {booking_id}\n"
                "📅 Data: {date}\n"
                "💲 Totaal: ${price}\n\n"
                "📞 Een adviseur neemt contact met u op om de betaling af te ronden."
            ),
            "reserva_rejected": "❌ Geen beschikbaarheid. Probeer andere data.",
            "promociones": "🎉 20% KORTING voor verblijven >7 nachten",
            "contact_info": "📞 Hulp van mensen -> Angela is beschikbaar +5999-5153955 (WhatsApp)",
            "date_format_help": "🗓️ Formaat: YYYY-MM-DD tot YYYY-MM-DD\nVoorbeeld: 2024-12-01 tot 2024-12-10",
            "date_input_prompt": "📅 Data (check-in tot check-out): ",
            "apartment_choice_prompt": "🔍 Kies appartement (1/2): ",
            "total_price": "Totaal",
            "confirmation_prompt": "Bevestigen? (j/n)",
            "confirmation_character": "j",
            "client_name_prompt": "👤 Volledige naam: ",
            "client_phone_prompt": "📞 Contacttelefoon (bijv. +584241234567): ",
            "invalid_option": "❌ Ongeldige optie",
            "apartment_unavailable": "❌ Appartement {apt_type} niet beschikbaar.",
            "booking_cancelled": "🚫 Boeking geannuleerd",
            "invalid_phone": "❌ Ongeldig telefoonnummer. Gebruik internationaal formaat: +584241234567",
            "booking_success": (
                "🎉 *Boeking succesvol geregistreerd, {client_name}!*\n\n"
                "👇 *Betalingsopties:*\n"
                "[1️⃣] Betaal met PayPal: {paypal_link}\n"
                "[2️⃣] Stuur een overschrijvingsbewijs: {whatsapp_link}\n\n"
                "📌 *Belangrijke instructies:*\n"
                "• Als u met PayPal betaalt: Bevestiging is automatisch\n"
                "• Als u met een ander middel betaalt:\n"
                "  1. Stuur uw bewijs via knop [2️⃣]\n"
                "  2. Wij valideren uw betaling binnen <24h\n"
                "  3. U ontvangt een bevestiging via WhatsApp\n\n"
                "⏳ *Boeking actief voor 48h*"
            ),
            "booking_error": "❌ Fout in het proces",
            "location_prompt": "📍 Wilt u de locatie op Google Maps zien?",
            "location_choice_prompt": "[1] Ja, toon mij!",
            "location_response": "🌍 Hier is de locatie: {maps_url}\n⛱️We zijn 5 minuten van het strand.",
            "language_selection": "🌐 Selecteer een taal:",
            "language_input_prompt": "Selecteer een optie: ",
            "language_changed": "Taal gewijzigd naar {language}.",
            "initial_language_prompt": "Kies alstublieft uw taal:",
            "name_prompt": "👤 Voer uw naam in: ",
            "option_prompt": "Optie: ",
            "admin_menu": "Beheermenu",
            "goodbye": "Bedankt voor het kiezen van ons!",
            "apartment1_name": "Zeezicht",
            "apartment2_name": "Zwembadzicht",
            "to": "tot",
            "whatsapp_message": "Hallo! 👋 Ik heb zojuist {booking_id} geboekt en wil mijn betalingsbewijs sturen"
        }
    }
}