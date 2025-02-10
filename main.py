import os
import logging
from transformers import logging as transformers_logging

# Desactivar advertencias de transformers
os.environ["TOKENIZERS_PARALLELISM"] = "false"
transformers_logging.set_verbosity_error()

# Desactivar mensajes de logging de nivel INFO
logging.getLogger("transformers").setLevel(logging.ERROR)


from src.chatbot import Chatbot

if __name__ == "__main__":
    Chatbot().run()