"""API HTTP para los motores de clasificación de soporte."""
from fastapi import FastAPI, HTTPException

from .generative import (
    GenerativeConfigurationError,
    GenerativeUnavailableError,
    classify_generative,
)
from .models import AnalyzeRequest, AnalyzeResponse, Mode
from .traditional import classify_traditional

app = FastAPI(title="AI Support Engine", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    if request.mode == Mode.traditional:
        return classify_traditional(request.message)
    try:
        return classify_generative(request.message)
    except GenerativeConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from None
    except GenerativeUnavailableError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from None
