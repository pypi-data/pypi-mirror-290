# Google sheet API handler

**gsheet_api_handler** es un paquete de Python diseñado para facilitar la autenticación y la lectura de datos desde Google Sheets. Incluye un mecanismo robusto de manejo de errores con reintentos exponenciales para asegurar la confiabilidad en la recuperación de datos pensando para el uso en el entorno de google colab.

## Características

- **Autenticación en Google Sheets**: Utiliza las credenciales de Google para autenticar y acceder a hojas de cálculo.
- **Lectura de Datos**: Extrae los datos de una hoja específica de Google Sheets en formato de lista.
- **Manejo de Errores**: Implementa un sistema de reintentos exponenciales para manejar errores temporales de manera efectiva cuando la cantidad de requests realizadas supera la cuota.

## Instalación

Para instalar **gsheet_api_handler**, puedes utilizar `pip`. Abre una terminal y ejecuta el siguiente comando:

```bash
pip install gsheet_api_handler
```
## Uso

```python
from gsheet_api_handler import google_sheet_reader, backoff_retry

# URL del Google Sheet y nombre de la hoja
url = "https://docs.google.com/spreadsheets/d/your_spreadsheet_id"
sheet_name = "Sheet1"

sheet_data = backoff_retry(lambda: google_sheet_reader(url, sheet_name))
print(sheet_data)
```