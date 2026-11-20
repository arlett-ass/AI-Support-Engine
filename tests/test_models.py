import pytest
from pydantic import ValidationError

from ai_support_engine.models import (
    AnalyzeRequest,
    AnalyzeResponse,
    Category,
    Mode,
    Priority,
)


def test_valid_request_trims_whitespace():
    item = AnalyzeRequest(message="  No puedo iniciar sesión  ", mode="traditional")
    assert item.message == "No puedo iniciar sesión"
    assert item.mode == Mode.traditional


@pytest.mark.parametrize("message", ["", "  ", "\n\t"])
def test_empty_request_is_rejected(message):
    with pytest.raises(ValidationError):
        AnalyzeRequest(message=message, mode="traditional")


def test_unknown_mode_is_rejected():
    with pytest.raises(ValidationError):
        AnalyzeRequest(message="Problema de acceso", mode="unknown")


def test_extra_fields_are_rejected():
    with pytest.raises(ValidationError):
        AnalyzeRequest(message="Error", mode="traditional", token="secret")


def test_valid_response_has_agreed_categories_and_priorities():
    result = AnalyzeResponse(
        category=Category.SECURITY,
        priority=Priority.CRITICAL,
        response="El incidente requiere revisión.",
        requiresHumanReview=True,
        mode=Mode.generative,
    )
    assert result.category == Category.SECURITY
    assert result.requiresHumanReview is True


def test_invalid_response_is_rejected():
    with pytest.raises(ValidationError):
        AnalyzeResponse(
            category="OTHER",
            priority="URGENT",
            response=" ",
            requiresHumanReview=False,
            mode="generative",
        )


def test_message_length_limit():
    with pytest.raises(ValidationError):
        AnalyzeRequest(message="x" * 2001, mode="traditional")
