# Opción B: Groq para clasificación generativa

La integración usa el endpoint oficial `https://api.groq.com/openai/v1/chat/completions` y la dependencia `httpx` ya instalada. No requiere GPU local. Gemini se conserva como proveedor alternativo.

1. Crear cuenta en https://console.groq.com y generar una API Key desde el apartado de claves.
2. Revisar el plan Free y los límites efectivos de la organización en https://console.groq.com/settings/limits. No activar un plan de pago.
3. En la terminal Linux (no escribir claves en archivos versionados):

```bash
export GENERATIVE_PROVIDER=groq
export GROQ_MODEL=openai/gpt-oss-20b
read -rsp "Clave de Groq: " GROQ_API_KEY; echo
export GROQ_API_KEY
python -m pytest -v
python -c "from ai_support_engine.generative import classify_generative; print(classify_generative('No puedo iniciar sesión en mi cuenta de prueba').model_dump_json(indent=2))"
```

El programa utiliza JSON mode y valida el resultado localmente con Pydantic. Si la API rechaza el modelo o la cuota, muestra un error explícito; no inventa una respuesta. Las pruebas con cliente falso no acreditan acceso real. Nunca compartir claves ni utilizar datos sensibles reales.

Para volver a Gemini: `export GENERATIVE_PROVIDER=gemini` y configurar `GEMINI_API_KEY` y `GEMINI_MODEL`.

**Importante:** el modelo gratuito y sus límites pueden cambiar; comprobarlos en el panel antes de la demostración. La implementación conserva el contrato de cuatro categorías y la revisión humana de incidentes de seguridad.
