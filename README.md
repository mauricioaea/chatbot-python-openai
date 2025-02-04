# Transcripción de Audio con Google Cloud Speech-to-Text

Este proyecto permite transcribir archivos de audio a texto utilizando la API de **Google Cloud Speech-to-Text**. A continuación, se describen los pasos necesarios para configurar y ejecutar el script de transcripción.

---

## Requisitos Previos

1. **Cuenta de Google Cloud**:
   - Crear un proyecto en [Google Cloud Console](https://console.cloud.google.com/).
   - Habilitar la API de **Cloud Speech-to-Text**.

2. **Credenciales de Google Cloud**:
   - Crear una cuenta de servicio y descargar el archivo JSON de credenciales.
   - Guardar el archivo JSON en una ubicación segura (por ejemplo, `C:\credenciales\chatbot-ia-449403-201808443630.json`).

3. **Instalación de Dependencias**:
   - Instalar las librerías necesarias usando `pip`:
     ```bash
     pip install google-cloud-speech
     ```

4. **FFmpeg**:
   - Descargar e instalar FFmpeg desde [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
   - Agregar FFmpeg al PATH del sistema.

   **Pasos para agregar FFmpeg al Path**
   1. Verificar la Instalación de FFmpeg
Primero, asegúrate de que FFmpeg esté correctamente instalado y que la carpeta bin de FFmpeg esté en el PATH del sistema.

Pasos para Verificar:
Abre una nueva ventana de Símbolo del sistema o PowerShell (no la terminal de Visual Studio Code).

Ejecuta el siguiente comando:

bash
ffmpeg -version
Si FFmpeg está correctamente instalado y agregado al PATH, verás información sobre la versión de FFmpeg.

Si no ves la información, significa que FFmpeg no está en el PATH.

2. Agregar FFmpeg al PATH (Si No Está Agregado)
Si FFmpeg no está en el PATH, sigue estos pasos para agregarlo:

En Windows:
Encuentra la Carpeta de FFmpeg:

La carpeta de FFmpeg debe contener un archivo ejecutable llamado ffmpeg.exe. Normalmente, está en una ruta como:


C:\ffmpeg-7.1-full_build\ffmpeg-7.1-full_build\bin
Agregar al PATH:

Haz clic derecho en "Este equipo" o "Mi PC" y selecciona "Propiedades".

Haz clic en "Configuración avanzada del sistema".

En la ventana que aparece, haz clic en "Variables de entorno".

En la sección "Variables del sistema", busca la variable Path y haz clic en "Editar".

Haz clic en "Nuevo" y agrega la ruta de la carpeta bin de FFmpeg (por ejemplo, C:\ffmpeg-7.1-full_build\ffmpeg-7.1-full_build\bin).

Haz clic en "Aceptar" para guardar los cambios.

Verificar:

Abre una nueva ventana de Símbolo del sistema o PowerShell.

Ejecuta el siguiente comando para verificar que FFmpeg esté instalado correctamente:

bash
ffmpeg -version
Si la instalación fue exitosa, verás información sobre la versión de FFmpeg.

3. Usar FFmpeg en la Terminal de Visual Studio Code
Una vez que hayas verificado que FFmpeg está en el PATH, puedes usarlo en la terminal de Visual Studio Code. Sigue estos pasos:

Cierra y Reabre Visual Studio Code:

Esto asegura que Visual Studio Code reconozca los cambios en el PATH.

Ejecuta el Comando de Conversión:

En la terminal de Visual Studio Code, ejecuta el siguiente comando:

bash
ffmpeg -i audio1.opus -c:a libopus audio1_ogg.opus

4. Si el Problema Persiste
Si después de agregar FFmpeg al PATH sigues viendo el error, prueba lo siguiente:

Especificar la Ruta Completa de FFmpeg:
En lugar de usar solo ffmpeg, especifica la ruta completa del ejecutable. Por ejemplo:

bash

    **C:\ffmpeg-7.1-full_build\ffmpeg-7.1-full_build\bin\ffmpeg -i audio1.opus -c:a libopus audio1_ogg.opus
Verificar la Terminal de Visual Studio Code**

---

## Configuración del Proyecto

1. **Estructura del Proyecto**:
   - Crear una carpeta para el proyecto (por ejemplo, `chatbot_api`).
   - Guardar el archivo JSON de credenciales y los archivos de audio en esta carpeta.

2. **Archivo de Código**:
   - Crear un archivo `prueba.py` con el siguiente contenido:
     ```python
     import os
     from google.cloud import speech_v1p1beta1 as speech
     import logging

     def transcribe_audio(audio_file):
         """Transcribe un archivo de audio a texto."""

         credentials_path = r"C:\credenciales\chatbot-ia-449403-201808443630.json"

         try:
             # Verifica si el archivo de audio existe
             if not os.path.exists(audio_file):
                 raise FileNotFoundError(f"El archivo de audio no existe: {audio_file}")

             # Verifica si el archivo de credenciales existe
             if not os.path.exists(credentials_path):
                 raise FileNotFoundError(f"El archivo de credenciales no existe: {credentials_path}")

             # Configura el cliente de Google Cloud Speech
             client = speech.SpeechClient.from_service_account_json(credentials_path)

             # Lee el archivo de audio
             with open(audio_file, "rb") as audio_content:
                 audio = speech.RecognitionAudio(content=audio_content.read())

             # Configura el reconocimiento de audio
             config = speech.RecognitionConfig(
                 encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,  # Formato OGG_OPUS
                 sample_rate_hertz=48000,  # Tasa de muestreo
                 language_code="es-ES",    # Idioma del audio
                 enable_automatic_punctuation=True,  # Puntuación automática
                 use_enhanced=True,        # Modelo mejorado
                 model="latest_long",      # Ideal para audios cortos
                 audio_channel_count=1,    # Cambia a 2 si el audio es estéreo
             )

             # Realiza la transcripción
             response = client.recognize(config=config, audio=audio)

             # Muestra los resultados
             if not response.results:
                 print("No se detectó ninguna palabra en el audio.")
             else:
                 for result in response.results:
                     for alternative in result.alternatives:
                         print(f"Transcripción: {alternative.transcript}")
                 print("Transcripción completada exitosamente")

         except FileNotFoundError as e:
             print(f"Error: {str(e)}")
         except Exception as e:
             logging.error(f"Error durante la transcripción: {str(e)}")
             print("Ocurrió un error al transcribir el audio. Verifica el archivo de log para más detalles.")

     if __name__ == "__main__":
         audio_file = r"D:\copy\ORIGINAL\PROGRAMAR\VISION POR COMPUTADOR\2025\chatbot_api\audio1

## si tu audio no es reconocido o esta en formato .opus, debes convertirlo al formato OGG_OPUS, aqui te dejo las indicaciones como debes de hacerlo

**Convertir audio2.opus a OGG_OPUS**
Abre la Terminal de Visual Studio Code.

Navega a la carpeta donde está el archivo audio2.opus (si no estás allí):

bash

cd D:\copy\ORIGINAL\PROGRAMAR\VISION POR COMPUTADOR\2025\chatbot_api
Ejecuta el siguiente comando para convertir el archivo:

bash

C:\ffmpeg-7.1-full_build\ffmpeg-7.1-full_build\bin\ffmpeg -i audio2.opus -c:a libopus audio2_ogg.opus
Esto creará un nuevo archivo llamado audio2_ogg.opus en la misma carpeta.

Paso 2: Actualizar el Código
Abre tu archivo prueba.py en Visual Studio Code.

Actualiza la ruta del archivo de audio para que apunte al archivo convertido (audio2_ogg.opus):

python
Copy
if __name__ == "__main__":
    audio_file = r"D:\copy\ORIGINAL\PROGRAMAR\VISION POR COMPUTADOR\2025\chatbot_api\audio2_ogg.opus"  # Archivo convertido
    transcribe_audio(audio_file)
Paso 3: Ejecutar el Script

En la terminal de Visual Studio Code, ejecuta el script:

bash
python prueba.py
