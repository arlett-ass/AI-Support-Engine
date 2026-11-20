# Motor generativo con Google Gemini

## Objetivo

Este módulo consulta realmente un modelo de Google Gemini mediante el SDK
`google-genai`. No contiene respuestas falsas ni un reemplazo silencioso por
el motor tradicional. Si Gemini falla, devuelve un error explícito.

## Configuración local

1. Instala el proyecto y las dependencias con `python -m pip install -e .`
   y `python -m pip install -r requirements-dev.txt`.
2. Consigue una clave de Gemini en Google AI Studio y comprueba las condiciones
   y cuotas de la cuenta. No publiques ni compartas la clave.
3. Configura las variables **en tu terminal**, sin introducirlas en Git:

   ```bash
   export GEMINI_API_KEY='TU_CLAVE_PRIVADA'
   export GEMINI_MODEL='MODELO_DISPONIBLE_EN_TU_CUENTA'
   ```

4. Ejecuta una consulta con datos ficticios:

   ```bash
   python -c "from ai_support_engine.generative import classify_generative; print(classify_generative('No puedo iniciar sesión').model_dump_json(indent=2))"
   ```

El nombre de modelo se deja configurable porque su disponibilidad, precio y
cuotas pueden cambiar. La clave no debe quedar en capturas, commits ni registros.

## Funcionamiento

- Valida el mensaje con el mismo contrato de entrada que el motor tradicional.
- Envía el mensaje como contenido y las reglas de clasificación como
  instrucción de sistema; solicita una salida JSON estructurada.
- Valida el JSON recibido con `AnalyzeResponse`.
- Exige que el modo devuelto sea `generative`.
- Si detecta señales explícitas de seguridad, fuerza categoría `SECURITY`,
  revisión humana y prioridad al menos `HIGH`. Si el modelo ya clasifica como
  `SECURITY`, obliga a revisión humana.
- Si falta configuración, el proveedor falla o la respuesta es inválida, lanza
  un error. **No afirma haber utilizado Gemini cuando no pudo hacerlo.**

## Pruebas y limitaciones

`python -m pytest -v` ejecuta pruebas unitarias con un cliente falso
inyectado. **Estas pruebas no realizan llamadas reales ni prueban acceso a la
cuenta de Google.** La comprobación de integración real requiere una clave
configurada y una llamada controlada como la del ejemplo anterior.

El filtro de seguridad basado en expresiones no detecta todas las amenazas,
negaciones o formas indirectas. No garantiza que el modelo nunca siga una
instrucción maliciosa. No se deben enviar contraseñas, datos personales reales
ni incidentes confidenciales a la API en esta actividad.

La comparación entre motores y el endpoint HTTP se implementarán en ramas
posteriores.
