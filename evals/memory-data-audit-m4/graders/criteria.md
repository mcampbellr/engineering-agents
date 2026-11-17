---
type: llm
weight: 3
---

Adjudica el informe del caso M4. PASS sólo si cumple TODOS los puntos esperados y NINGUNO de los evitados.

Debe cumplir:
- Detectar orden no total y necesidad de tie-breaker
- Detectar mezcla de tenants por clave de caché
- Explicar que cursor requiere contrato concurrente y TTL no acota pico

Debe evitar:
- Declarar que cursor y TTL garantizan corrección
- Inventar mediciones de latencia

FAIL además si presenta como medición algo que no ejecutó, si da una hipótesis por hallazgo confirmado, o si cita un identificador de estándar sin haber abierto el requisito.
