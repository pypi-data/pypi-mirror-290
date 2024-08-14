import requests
from urllib.parse import urlparse

def check_status(url):
    # Asegúrate de que la URL tenga un esquema (http o https)
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'https://' + url
    
    try:
        response = requests.get(url)
        return response  # Devuelve el objeto de respuesta
    except requests.exceptions.RequestException as e:
        return f"❗️ Error: {e}"