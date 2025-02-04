import os
from google.cloud import speech_v1p1beta1 as speech
import logging

def transcribe_audio(audio_file):
    """Transcribe un archivo de audio a texto."""

    credentials_path = r"C:\credenciales\chatbot-ia-449403-cf712009d139.json"

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
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000,
            language_code="es-ES",
            enable_automatic_punctuation=True,  # Puntuación automática
            use_enhanced=True,  # Modelo mejorado
            model="latest_long",  # Ideal para audios cortos
            audio_channel_count=1,  # Mono (1 canal)
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
    audio_file = r"D:\copy\ORIGINAL\PROGRAMAR\VISION POR COMPUTADOR\2025\chatbot_api\audio2_ogg.opus" # Archivo convertido
    transcribe_audio(audio_file)