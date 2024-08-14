import pytest
from status_checker_api import check_status

def test_check_status():
    url = "https://example.com"
    result = check_status(url)
    assert "✅" in result  # Verifica que el mensaje de éxito esté presente en el resultado
    assert "200" in result  # Verifica que el código de estado esté presente en el resultado
