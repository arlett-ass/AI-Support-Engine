"""Contrato compartido por ambos motores; todavía no implementa una API."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Category(str, Enum):
    ACCESS = "ACCESS"
    BUG = "BUG"
    FEATURE = "FEATURE"
    SECURITY = "SECURITY"


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Mode(str, Enum):
    traditional = "traditional"
    generative = "generative"


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str = Field(min_length=1, max_length=2000)
    mode: Mode

    @field_validator("message")
    @classmethod
    def reject_blank_message(cls, value: str) -> str:
        clean = value.strip()
        if not clean:
            raise ValueError("El mensaje no puede estar vacío.")
        return clean


class AnalyzeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Category
    priority: Priority
    response: str = Field(min_length=1)
    requiresHumanReview: bool
    mode: Mode

    @field_validator("response")
    @classmethod
    def reject_blank_response(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("La respuesta no puede estar vacía.")
        return value.strip()
