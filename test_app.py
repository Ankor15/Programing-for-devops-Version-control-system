from app import app
import pytest

def test_hello_world():
    client = app.test_client()
    response = client.get('/')
    assert response.data == b'Hello, World! Aplikasi dengan database PostgreSQL dan Redis.'
