from starlette.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    """
    Test the /health endpoint returns the expected status and service name.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "transcription-service"}
