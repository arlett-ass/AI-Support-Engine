# Motor tradicional: decisiones y límites

Este motor **no utiliza inteligencia artificial generativa**. Clasifica mensajes
mediante palabras y expresiones reconocibles, sin conectarse a servicios externos.

## Proceso

1. Comprueba que el mensaje sea texto, no esté vacío y tenga hasta 2000 caracteres.
2. Normaliza mayúsculas, acentos y espacios.
3. Busca expresiones definidas para `ACCESS`, `BUG`, `FEATURE` y `SECURITY`.
4. Da prioridad a `SECURITY` cuando detecta una señal de riesgo.
5. Asigna `CRITICAL` a incidentes de seguridad con señales explícitas de
   filtración, robo de cuenta o compromiso; los demás incidentes de seguridad
   reciben `HIGH`.
6. Para el resto, asigna `HIGH` si hay señales de urgencia, `LOW` a
   solicitudes de funcionalidades y `MEDIUM` a los demás casos.
7. Devuelve una respuesta fija por categoría y marca revisión humana en
   incidentes de seguridad.

## Casos inciertos

Si no coincide ninguna categoría, o si coincide más de una categoría no
relacionada con seguridad, se devuelve provisionalmente `BUG/MEDIUM`,
**con revisión humana obligatoria y una respuesta que pide aclaraciones**.
Esta es una limitación del contrato actual, que exige una de cuatro categorías.

## Límites

- Una regla basada en palabras clave puede fallar con sinónimos, negaciones,
  ironía o redacciones no previstas.
- No se debe usar como única medida para tomar decisiones de seguridad.
- No interpreta instrucciones contenidas en el mensaje como órdenes.
- Las prioridades son reglas del prototipo, no niveles de servicio reales.
- El motor generativo se implementará en otra rama para permitir la comparación.
