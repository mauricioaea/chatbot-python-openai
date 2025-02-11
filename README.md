# 🌴 Robby Apartments Curacao - Chatbot de Reservas

¡Bienvenido al chatbot de reservas de Robby Apartments Curacao! Este proyecto es un asistente virtual que permite a los usuarios realizar reservas, consultar disponibilidad, ver promociones y más, en múltiples idiomas.

---

## 🚀 Características Principales

- **Reservas en tiempo real:** Los usuarios pueden reservar apartamentos con vista al mar o a la piscina.
- **Multilingüe:** Soporte para español, inglés, portugués y holandés.
- **Autenticación de administrador:** Panel de administración para gestionar reservas.
- **Encriptación de datos:** Protección de información sensible como números de teléfono.
- **Integración con PayPal:** Opciones de pago seguras.

---

## 🛠️ Requisitos del Sistema

- Python 3.8 o superior.
- Librerías listadas en `requirements.txt`.

---

## 🛠️ Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tuusuario/robby-apartments-chatbot.git
   cd robby-apartments-chatbot

2. **Crea un entorno virtual:**
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

3. **Instala las dependencias:**
pip install -r requirements.txt

4. **Configura las variables de entorno:**
Crea un archivo .env en la raíz del proyecto.

Copia las variables de .env.example y ajusta los valores según sea necesario.

5.**Ejecuta el chatbot:**
python main.py

6.**📂 Estructura del Proyecto**
robby-apartments-chatbot/
├── src/                  # Código fuente del chatbot
│   ├── chatbot.py        # Lógica principal del chatbot
│   ├── database.py       # Manejo de la base de datos
│   ├── booking_handler.py# Validación de reservas
│   └── admin_panel.py    # Panel de administración
├── backups/              # Copias de seguridad de la base de datos
├── venv/                 # Entorno virtual
├── .env                  # Variables de entorno
├── main.py               # Punto de entrada del programa
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación del proyecto

7.**🔐 Variables de Entorno**
El archivo .env debe contener las siguientes variables:
# Credenciales de administrador
ADMIN_USER=admin_curacao
ADMIN_PASSWORD_HASH="$2b$12$Vt05hSzuaHhe/eMwLpzVoevXyKCsR/dnbNIE7EPokvTNjyKGEzVoa"

# Clave de encriptación (generada con Fernet)
ENCRYPTION_KEY=G3tmjm7QA629cn90WFlm9pqit27V37CZAAJVJuwyW_U=

# PayPal (si lo integras)
PAYPAL_CLIENT_ID=tu_id
PAYPAL_SECRET=tu_secreto

# Ubicación de los apartamentos
LOCATION_LAT=12.3663374
LOCATION_LON=-69.1533397

8.**🧑‍💻 Uso**
8.1 Iniciar el chatbot:
    python main.py
8.2 **Seleccionar idioma:**

El chatbot te pedirá que elijas un idioma al iniciar.

8.3 **Realizar una reserva:**

Sigue las instrucciones en pantalla para seleccionar fechas, tipo de apartamento y completar el pago.

8.4 **Panel de administración:**

Accede al panel de administración ingresando /admin en el menú principal.

**📝 Dependencias**
Las dependencias del proyecto están listadas en requirements.txt. Para instalarlas, ejecuta:
pip install -r requirements.txt

**📜 Licencia**
Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo LICENSE.

**🤝 Contribuciones**
¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto, sigue estos pasos:

Haz un fork del repositorio.

Crea una rama con tu nueva funcionalidad (git checkout -b feature/nueva-funcionalidad).

Realiza tus cambios y haz commit (git commit -m 'Añadir nueva funcionalidad').

Haz push a la rama (git push origin feature/nueva-funcionalidad).

Abre un Pull Request.

📧 Contacto
Si tienes preguntas o sugerencias, no dudes en contactarme:
📧 mauricioandreserazo@outlook.com
🌐 https://github.com/mauricioaea