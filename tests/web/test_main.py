from fastapi.testclient import TestClient

from src.web.main import app

client = TestClient(app)


def test_api_router_included(auth_headers):
    response = client.get("/api", headers=auth_headers("GET", {}))
    assert response.status_code != 404, "API router not included or incorrect prefix"


def test_default_response_class(auth_headers):
    response = client.get("/api", headers=auth_headers("GET", {}))
    assert response.headers["content-type"] == "application/json", (
        "Default response class is not ORJSONResponse"
    )
