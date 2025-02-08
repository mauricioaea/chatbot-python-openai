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

# ================= CONFIGURACIÓN ADMIN =================
ADMIN_USERNAME = "admin_curacao"
ADMIN_PASSWORD = "clave_secreta_123"

# ================= CONFIGURACIÓN INICIAL =================
LANGUAGE_CONFIG = {
    "es": {
        "intent_model": "dccuchile/bert-base-spanish-wwm-cased",
        "responses": {
            "welcome": "¡Hola {name}! Soy tu asistente de Curacao Vacaciones. 🌴",
            "menu": (
                "¿En qué puedo ayudarte hoy?\n\n"
                "1. 🏠 Ver apartamentos\n2. 📅 Hacer reserva\n"
                "3. 🎉 Promociones\n4. 📞 Contactar asesor\n"
                "5. 🌐 Cambiar idioma\n6. ❌ Salir"
            ),
            "apartamentos": (
                "🏠 *Tipos de Apartamentos Disponibles:*\n\n"
                "1. **🌊 Cerca a las mejores playas de la isla**\n"
                "   - 🛌 Capacidad: 4 huéspedes\n"
                "   - 💲 Precio: $110/noche\n"
                "   - 📍 Ubicación: Bandabou-Curacao\n\n"
                "2. **🌟 Vista Piscina**\n"
                "   - 🛌 Capacidad: 4 huéspedes\n"
                "   - 💲 Precio: $110/noche\n"
                "   - 📍 Ubicación: Zona VIP\n\n"
                "**🏡 Servicios Incluidos:** WiFi • Piscina • Estacionamiento • Netflix"
            ),
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
            "promociones": "🎉 VERANO24: 20% OFF en estancias >7 noches",
            "contact_info": "📞 Contacto directo: +5999-765-4321 (WhatsApp)",
            "date_format_help": "🗓️ Formato: YYYY-MM-DD a YYYY-MM-DD\nEj: 2024-12-01 a 2024-12-10"
        }
    }
}