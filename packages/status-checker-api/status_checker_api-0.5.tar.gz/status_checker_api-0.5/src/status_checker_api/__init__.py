import requests
from urllib.parse import urlparse

def check_status(url):
    # Asegúrate de que la URL tenga un esquema (http o https)
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'https://' + url
    
    try:
        response = requests.get(url)
        return f"✅ La URL está activa con código de estado: {response.status_code}"  # Devuelve el mensaje con el código de estado
    except requests.exceptions.RequestException as e:
        return f"❌ Error: {e} 😔"  # Devuelve el mensaje de error con una x