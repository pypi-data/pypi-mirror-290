import pytest
from status_checker_api import check_status

def test_check_status():
    url = "https://example.com"
    response = check_status(url)
    assert response.status_code == 200