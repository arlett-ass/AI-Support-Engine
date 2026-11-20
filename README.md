# AI Support Engine

## Integrantes

- Angelica Arlett Santiago Serrano
- Nicolás David Juarez Mendoza
- Victor Manual Jimenez Suarez


Prototipo académico de clasificación de tickets de soporte con dos modos: **traditional** (reglas deterministas) y **generative** (modelo de lenguaje por API). No necesita base de datos, GPU ni interfaz web.

## Instalación en Linux

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

## Proveedor generativo

Se recomienda Groq (modelo inicial `openai/gpt-oss-20b`). Crear una clave personal en https://console.groq.com/keys y comprobar los límites del plan gratuito. **Nunca subir ni compartir la clave.**

```bash
export GENERATIVE_PROVIDER=groq
export GROQ_MODEL=openai/gpt-oss-20b
read -rsp "Clave de Groq: " GROQ_API_KEY; echo
export GROQ_API_KEY
```

También se conserva Gemini: `GENERATIVE_PROVIDER=gemini`, `GEMINI_API_KEY` y `GEMINI_MODEL`. El acceso gratuito depende del proyecto.

## API REST

```bash
uvicorn ai_support_engine.api:app --reload
```

Documentación interactiva: http://127.0.0.1:8000/docs

Ejemplo de solicitud:

```bash
curl -sS -X POST http://127.0.0.1:8000/api/analyze \
  -H 'Content-Type: application/json' \
  -d '{"message":"No puedo iniciar sesión","mode":"traditional"}'
```

Cambiar `mode` a `generative` para usar Groq. El resultado incluye `category`, `priority`, `response`, `requiresHumanReview` y `mode`. Errores: 422 para entrada inválida; 503 para configuración faltante; 502 si el proveedor falla.

## Comparación y evidencias

```bash
python scripts/compare_engines.py
```

Se genera `artifacts/comparison.json` con **11 casos sintéticos**, incluidos ambigüedad y dos intentos de inyección. La comparación registra resultados y errores reales sin simular llamadas exitosas. Se recomienda capturar la salida de `pytest`, una consulta de cada modo y el archivo JSON. No ejecutar con mensajes privados o secretos.

## Límites

El motor tradicional depende de palabras clave. El generativo depende de la disponibilidad, cuotas y comportamiento del proveedor. La protección contra inyección y la detección de seguridad son parciales: los incidentes explícitos requieren revisión humana, pero no hay garantía de identificar todos los riesgos.

## Conclusión

El motor tradicional permite clasificar solicitudes frecuentes de manera rápida, consistente y sin depender de internet. El generativo ofrece respuestas más flexibles y puede interpretar mensajes variados, pero depende de un proveedor externo y de sus límites de acceso. La comparación utiliza casos sintéticos reproducibles para observar diferencias, sin presentar esas observaciones como una medición definitiva de precisión. Los incidentes de seguridad y los mensajes ambiguos requieren especial cuidado y revisión humana. La validación de entrada, el formato JSON y las pruebas automatizadas ayudan a mantener el contrato de la API; aun así, el prototipo no sustituye a un sistema de soporte supervisado.

## Evidencia final de pruebas

En la ejecución reportada por el equipo: **55 pruebas aprobadas**, **1 advertencia de deprecación de Starlette** y **11 casos de comparación ejecutados**. La advertencia no representa una prueba fallida. En la comparación, los dos motores coincidieron en la categoría de 10 de los 11 mensajes; el mensaje «No puedo entrar y la pantalla falla» fue clasificado como BUG por las reglas y ACCESS por el modelo, mostrando una ambigüedad real. Estos resultados son observaciones de la ejecución, no garantías de exactitud. La salida JSON se genera localmente en `artifacts/comparison.json` y debe adjuntarse o conservarse como evidencia.
