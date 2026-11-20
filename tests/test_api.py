"""Pruebas HTTP sin consumir cuota de proveedores."""
from fastapi.testclient import TestClient
from ai_support_engine.api import app
from ai_support_engine.generative import (
    GenerativeConfigurationError, GenerativeUnavailableError,
)
from ai_support_engine.models import AnalyzeResponse

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_traditional_endpoint():
    response = client.post("/api/analyze", json={
        "message": "Recibí un correo de phishing", "mode": "traditional",
    })
    assert response.status_code == 200
    data = AnalyzeResponse.model_validate(response.json())
    assert data.category.value == "SECURITY"
    assert data.requiresHumanReview is True


def test_generative_endpoint(monkeypatch):
    def fake_classifier(message):
        return AnalyzeResponse(
            category="ACCESS", priority="MEDIUM",
            response="Recupera el acceso.", requiresHumanReview=False,
            mode="generative",
        )
    monkeypatch.setattr("ai_support_engine.api.classify_generative", fake_classifier)
    response = client.post("/api/analyze", json={
        "message": "No puedo iniciar sesión", "mode": "generative",
    })
    assert response.status_code == 200
    assert response.json()["mode"] == "generative"


def test_invalid_request():
    for payload in [
        {"message": "", "mode": "traditional"},
        {"message": "Hola", "mode": "unknown"},
        {"message": "Hola", "mode": "traditional", "extra": 1},
        {"message": " ", "mode": "traditional"},
        {"message": "x" * 2001, "mode": "traditional"},
    ]:
        assert client.post("/api/analyze", json=payload).status_code == 422


def test_missing_body():
    assert client.post("/api/analyze", json={}).status_code == 422


def test_provider_unavailable(monkeypatch):
    def unavailable(message):
        raise GenerativeUnavailableError("Proveedor no disponible")
    monkeypatch.setattr("ai_support_engine.api.classify_generative", unavailable)
    response = client.post("/api/analyze", json={
        "message": "Prueba", "mode": "generative",
    })
    assert response.status_code == 502
    assert "Proveedor no disponible" in response.json()["detail"]


def test_provider_unconfigured(monkeypatch):
    def unconfigured(message):
        raise GenerativeConfigurationError("Falta clave")
    monkeypatch.setattr("ai_support_engine.api.classify_generative", unconfigured)
    response = client.post("/api/analyze", json={
        "message": "Prueba", "mode": "generative",
    })
    assert response.status_code == 503
