import pytest

from ci_server import __version__, app


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Thrust the ci service" in response.data


def test_version():
    assert __version__ == "0.1.0"
