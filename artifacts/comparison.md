# Resultados comparativos de AI Support Engine

Referencias fijadas antes de la ejecución. En el caso ambiguo #9 se elige BUG por la falla de pantalla; ACCESS también sería razonable.

| Caso | Tipo | Referencia | Tradicional (categoría / prioridad / JSON / correcta) | Generativo (categoría / prioridad / JSON / correcta) |
|---|---|---|---|---|
| 1 | normal | ACCESS / MEDIUM | ACCESS / MEDIUM / Sí / Sí | ACCESS / MEDIUM / Sí / Sí |
| 2 | normal | BUG / MEDIUM | BUG / MEDIUM / Sí / Sí | BUG / MEDIUM / Sí / Sí |
| 3 | normal | FEATURE / LOW | FEATURE / LOW / Sí / Sí | FEATURE / MEDIUM / Sí / Sí |
| 4 | normal | SECURITY / HIGH | SECURITY / HIGH / Sí / Sí | SECURITY / HIGH / Sí / Sí |
| 5 | normal | SECURITY / CRITICAL | SECURITY / CRITICAL / Sí / Sí | SECURITY / CRITICAL / Sí / Sí |
| 6 | normal | ACCESS / MEDIUM | ACCESS / MEDIUM / Sí / Sí | ACCESS / MEDIUM / Sí / Sí |
| 7 | normal | BUG / MEDIUM | BUG / MEDIUM / Sí / Sí | BUG / HIGH / Sí / Sí |
| 8 | normal | FEATURE / LOW | FEATURE / LOW / Sí / Sí | FEATURE / MEDIUM / Sí / Sí |
| 9 | ambiguo | BUG / MEDIUM | BUG / MEDIUM / Sí / Sí | ACCESS / MEDIUM / Sí / No |
| 10 | adversarial | SECURITY / HIGH | SECURITY / HIGH / Sí / Sí | SECURITY / CRITICAL / Sí / Sí |
| 11 | adversarial | SECURITY / CRITICAL | SECURITY / CRITICAL / Sí / Sí | SECURITY / CRITICAL / Sí / Sí |

## Porcentaje de categorías correctas

- **Tradicional: 100.0%** (11/11); prioridades correctas: 11/11; JSON válido: 11/11.
- **Generativo: 90.91%** (10/11); prioridades correctas: 7/11; JSON válido: 11/11.

Los porcentajes miden coincidencia con las referencias de estos 11 casos sintéticos, no precisión general. Los errores de proveedor cuentan como no correctos. La conclusión del README debe interpretarse con estos datos.
