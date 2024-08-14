import time
import random

from google.colab import auth 
import gspread

auth.authenticate_user()
from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)


# Manejo del error de superación de requests
def backoff_retry(func, max_retries=5, min_wait_time=30, max_wait_time=120):
    """
    Intenta ejecutar una función con retirada exponencial en caso de error.
    
    Parameters:
    - func: La función a ejecutar.
    - max_retries: Número máximo de reintentos.
    - min_wait_time: Tiempo mínimo de espera entre reintentos en segundos.
    - max_wait_time: Tiempo máximo de espera entre reintentos en segundos.
    
    Returns:
    - El resultado de la función si se ejecuta correctamente.
    """
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            return func()
        except Exception as e:
            error_message = f"{str(e)[:20]}..."  # Muestra los primeros 50 caracteres y añade "..."
            wait_time = min_wait_time + (max_wait_time - min_wait_time) * (retry_count / max_retries)
            wait_time += random.randint(0, 1000) / 1000.0  # Añadir un valor aleatorio de hasta 1 segundo
            print(f"Error: {error_message}. Esperando {wait_time:.2f} segundos antes de reintentar...")
            time.sleep(wait_time)
            retry_count += 1
    
    raise Exception(f"Failed after {max_retries} retries")

# Función para lectura
def google_sheet_reader(url: str, sheet_name: str):
    """
    Simplificación de llamada de datos a un google sheet.
    
    Parameters:
    - url: Link de acceso al google sheet.
    - sheet_name: Nombre de la hoja a la que se está accediendo.
    
    Returns:
    - Devuelve los datos del google sheet en el objeto sheet_data.
    """
    wb = gc.open_by_url(url)
    sheet = wb.worksheet(sheet_name)
    sheet_data = sheet.get_all_values()
    return sheet_data