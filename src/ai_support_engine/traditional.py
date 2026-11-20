"""Clasificador tradicional determinista, sin conexión a modelos externos."""

import re

from .models import AnalyzeResponse, Category, Mode, Priority


KEYWORDS: dict[Category, tuple[str, ...]] = {
    Category.SECURITY: (
        "phishing", "suplantacion", "robo de cuenta", "acceso no autorizado",
        "actividad sospechosa", "cuenta comprometida", "datos filtrados",
        "filtracion", "malware", "virus", "hackeo", "hackeada",
        "contrasena robada", "brecha de seguridad", "fraude",
    ),
    Category.ACCESS: (
        "iniciar sesion", "inicio de sesion", "no puedo entrar", "no puedo acceder",
        "acceso denegado", "recuperar contrasena", "olvide mi contrasena",
        "restablecer contrasena", "bloqueada", "bloqueado", "login",
        "credenciales", "autenticacion",
    ),
    Category.BUG: (
        "error", "falla", "fallo", "no funciona", "se cierra", "se congela",
        "pantalla blanca", "no carga", "crash", "bug", "problema tecnico",
    ),
    Category.FEATURE: (
        "nueva funcion", "funcionalidad", "mejora", "sugerencia",
        "agregar", "anadir", "implementar", "seria util", "solicito",
    ),
}

CRITICAL_TERMS = (
    "datos filtrados", "filtracion", "cuenta comprometida",
    "contrasena robada", "brecha de seguridad", "robo de cuenta",
)
HIGH_TERMS = (
    "urgente", "inmediato", "critico", "critica", "produccion",
    "todos los usuarios", "no podemos trabajar", "servicio caido",
)

RESPONSES: dict[Category, str] = {
    Category.ACCESS: (
        "Comprueba tus datos de acceso y utiliza la opción de recuperación "
        "de contraseña. Si continúa el problema, contacta con soporte."
    ),
    Category.BUG: (
        "Anota los pasos para reproducir el error y comparte el mensaje "
        "que aparece, sin incluir contraseñas ni datos sensibles."
    ),
    Category.FEATURE: (
        "Gracias por la sugerencia. Describe la mejora y cómo ayudaría "
        "a los usuarios para que el equipo pueda evaluarla."
    ),
    Category.SECURITY: (
        "Este reporte necesita revisión humana. No compartas claves ni "
        "datos sensibles; informa al equipo de seguridad por el canal oficial."
    ),
}

UNCLEAR_RESPONSE = (
    "Necesitamos más información para clasificar tu solicitud. "
    "Describe qué ocurrió y qué resultado esperabas, sin compartir datos sensibles."
)


def _normalize(message: str) -> str:
    import unicodedata

    normalized = unicodedata.normalize("NFKD", message.casefold())
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", normalized).strip()


def _contains(text: str, phrase: str) -> bool:
    return re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text) is not None


def classify_traditional(message: str) -> AnalyzeResponse:
    """Clasifica por reglas explícitas y devuelve el contrato común.

    Las señales de seguridad tienen precedencia sobre las demás categorías.
    Ante mensajes ambiguos o desconocidos, solicita revisión humana.
    """
    if not isinstance(message, str) or not message.strip():
        raise ValueError("El mensaje no puede estar vacío.")
    if len(message) > 2000:
        raise ValueError("El mensaje supera los 2000 caracteres.")

    text = _normalize(message)
    matches = {
        category: any(_contains(text, word) for word in words)
        for category, words in KEYWORDS.items()
    }

    if matches[Category.SECURITY]:
        category = Category.SECURITY
    elif sum(matches.values()) != 1:
        return AnalyzeResponse(
            category=Category.BUG,
            priority=Priority.MEDIUM,
            response=UNCLEAR_RESPONSE,
            requiresHumanReview=True,
            mode=Mode.traditional,
        )
    else:
        category = next(key for key, matched in matches.items() if matched)

    if category == Category.SECURITY:
        priority = (
            Priority.CRITICAL
            if any(_contains(text, term) for term in CRITICAL_TERMS)
            else Priority.HIGH
        )
    elif any(_contains(text, term) for term in HIGH_TERMS):
        priority = Priority.HIGH
    elif category == Category.FEATURE:
        priority = Priority.LOW
    else:
        priority = Priority.MEDIUM

    return AnalyzeResponse(
        category=category,
        priority=priority,
        response=RESPONSES[category],
        requiresHumanReview=category == Category.SECURITY,
        mode=Mode.traditional,
    )
