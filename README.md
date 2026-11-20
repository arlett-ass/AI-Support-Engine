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

Se generan **`artifacts/comparison.json` y `artifacts/comparison.md`** con 11 casos sintéticos: 8 normales, 1 ambiguo y 2 adversariales. Cada caso tiene categoría y prioridad de referencia definidas antes de consultar los motores; para ambos se registra categoría, prioridad, si el JSON es válido y si la categoría y la prioridad coinciden con la referencia. Se calcula automáticamente el porcentaje de categorías correctas de cada motor (aciertos/11 × 100), además del porcentaje de prioridades correctas. Un error de proveedor cuenta como respuesta no correcta; nunca se sustituye por una respuesta inventada. La tabla y los porcentajes medidos se encuentran en **`artifacts/comparison.md`**, generado después de la ejecución real. No ejecutar con mensajes privados ni secretos.

**Nota sobre la ambigüedad:** «No puedo entrar y la pantalla falla» tiene referencia BUG porque reporta una falla de pantalla, aunque ACCESS también es razonable. Por eso, la comparación no demuestra precisión general ni un ganador universal.

**Evidencia de ejecución:** guardar captura de `python -m pytest -v`, de `python scripts/compare_engines.py`, de una respuesta HTTP tradicional y otra generativa en `http://127.0.0.1:8000/docs`; conservar `artifacts/comparison.json` y `artifacts/comparison.md`. Las capturas deben corresponder a ejecuciones reales.

## Límites

El motor tradicional depende de palabras clave. El generativo depende de la disponibilidad, cuotas y comportamiento del proveedor. La protección contra inyección y la detección de seguridad son parciales: los incidentes explícitos requieren revisión humana, pero no hay garantía de identificar todos los riesgos.

## Conclusión técnica (menos de 150 palabras)

En los casos observados, ambos motores clasificaron de la misma forma 10 de las 11 solicitudes; la diferencia apareció en un mensaje ambiguo. Esto no significa que los dos tengan el mismo porcentaje de aciertos en todas las situaciones: para decidir cuál funcionó mejor se deben consultar los porcentajes calculados en `artifacts/comparison.md`, usando las categorías de referencia. El motor tradicional es predecible, funciona sin internet y responde rápidamente, pero depende de frases conocidas. El generativo puede comprender mensajes variados y redactar respuestas más contextuales, aunque requiere conexión y depende del proveedor. Con una muestra tan pequeña no se puede afirmar que uno sea mejor en general. En incidentes de seguridad se mantiene la revisión humana.

## Evidencia final de pruebas

En la ejecución reportada por el equipo: **55 pruebas aprobadas**, **1 advertencia de deprecación de Starlette** y **11 casos de comparación ejecutados**. La advertencia no representa una prueba fallida. En la comparación reportada, los dos motores coincidieron en la categoría de 10 de los 11 mensajes; el mensaje «No puedo entrar y la pantalla falla» fue clasificado como BUG por las reglas y ACCESS por el modelo, mostrando una ambigüedad real. Estos resultados son observaciones de la ejecución, no garantías de exactitud. La salida JSON se genera localmente en `artifacts/comparison.json` y debe adjuntarse o conservarse como evidencia.
