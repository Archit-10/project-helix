from fastapi.testclient import TestClient


def test_version_endpoint(client: TestClient):
    response = client.get("/api/v1/version")

    assert response.status_code == 200

    data = response.json()

    assert data["project_name"] == "Project Helix"
    assert data["version"] == "0.1.0"