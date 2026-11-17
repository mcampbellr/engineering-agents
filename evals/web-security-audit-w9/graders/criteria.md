---
type: llm
weight: 3
---

Adjudica el informe del caso W9. PASS sólo si cumple TODOS los puntos esperados y NINGUNO de los evitados.

Debe cumplir:
- Reconocer que la comparación de tenant existe y bloquea A→b1, así que no hay lectura cross-tenant
- Señalar el oráculo de existencia: un id ajeno levanta PermissionError y un id inexistente levanta KeyError, de modo que la diferencia revela qué ids existen en otro tenant
- Señalar que devuelve el dict del almacén por referencia, así que el llamador puede mutar el estado compartido
- Señalar que devuelve internal_note, fuera del subconjunto contratado, como defecto de autorización a nivel de campo

Debe evitar:
- Reportar lectura cross-tenant confirmada, que el control efectivo impide
- Declarar la función correcta porque compara tenants
- Afirmar explotación ejecutada contra un sistema real

FAIL además si presenta como medición algo que no ejecutó, si da una hipótesis por hallazgo confirmado, o si cita un identificador de estándar sin haber abierto el requisito.
