"""Pruebas de Groq sin conexión externa ni clave real."""

import json
import pytest
from ai_support_engine.generative import classify_generative, GenerativeUnavailableError
from ai_support_engine.models import Category, Mode, Priority


def test_groq_success(monkeypatch):
    monkeypatch.setenv("GENERATIVE_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "fake-test-key")
    calls = []

    class Response:
        status_code = 200
        def json(self):
            return {"choices": [{"message": {"content": json.dumps({
                "category": "ACCESS", "priority": "MEDIUM",
                "response": "Recupera tu acceso.", "requiresHumanReview": False,
                "mode": "generative"
            })}}]}

    def fake_post(url, **kwargs):
        calls.append((url, kwargs))
        return Response()

    monkeypatch.setattr("ai_support_engine.generative.httpx.post", fake_post)
    result = classify_generative("No puedo iniciar sesión")
    assert result.category == Category.ACCESS
    assert result.mode == Mode.generative
    assert calls[0][1]["json"]["model"] == "openai/gpt-oss-20b"
    assert calls[0][1]["json"]["response_format"] == {"type": "json_object"}
    assert calls[0][1]["json"]["messages"][1]["role"] == "user"


def test_groq_permission_error(monkeypatch):
    monkeypatch.setenv("GENERATIVE_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "fake-test-key")

    class Response:
        status_code = 403

    monkeypatch.setattr("ai_support_engine.generative.httpx.post", lambda *a, **k: Response())
    with pytest.raises(GenerativeUnavailableError, match="HTTP 403"):
        classify_generative("No puedo iniciar sesión")


def test_groq_security_override(monkeypatch):
    monkeypatch.setenv("GENERATIVE_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "fake-test-key")

    class Response:
        status_code = 200
        def json(self):
            return {"choices": [{"message": {"content": json.dumps({
                "category": "FEATURE", "priority": "LOW", "response": "Gracias.",
                "requiresHumanReview": False, "mode": "generative"
            })}}]}

    monkeypatch.setattr("ai_support_engine.generative.httpx.post", lambda *a, **k: Response())
    result = classify_generative("Recibí un correo de phishing")
    assert result.category == Category.SECURITY
    assert result.priority == Priority.HIGH
    assert result.requiresHumanReview
