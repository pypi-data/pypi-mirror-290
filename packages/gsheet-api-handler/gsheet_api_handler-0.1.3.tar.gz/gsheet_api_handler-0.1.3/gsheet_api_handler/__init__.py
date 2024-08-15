# __init__.py

# Importa las funciones principales del paquete
from .main import google_sheet_reader, backoff_retry

# Define qué elementos estarán disponibles al importar todo el paquete
__all__ = ["google_sheet_reader", "backoff_retry"]

# Información del paquete
__version__ = "0.1.3"
__author__ = "Fabrizzio Rutigliano"
__email__ = "fabrizziorutigliano@gmail.com"
