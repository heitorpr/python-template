from fastapi import status
from fastapi.testclient import TestClient

from src.web.main import app


def test_api_router_included(auth_headers):
    with TestClient(app) as client:
        response = client.get("/api", headers=auth_headers("GET", {}))
        assert response.status_code != status.HTTP_404_NOT_FOUND, (
            "API router not included or incorrect prefix"
        )


def test_default_response_class(auth_headers):
    with TestClient(app) as client:
        response = client.get("/api", headers=auth_headers("GET", {}))
        assert response.headers["content-type"] == "application/json", (
            "Default response class is not ORJSONResponse"
        )


def test_excluded_paths():
    with TestClient(app) as client:
        excluded_paths = ["/docs", "/redoc", "/metrics"]
        for path in excluded_paths:
            response = client.get(path)
            assert response.status_code == status.HTTP_200_OK, (
                f"Excluded path {path} did not return expected status"
            )


def test_signature_middleware_http_exception():
    with TestClient(app) as client:
        response = client.get("/api/heroes/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        assert response.json() == {
            "detail": "Missing signature or timestamp",
        }
