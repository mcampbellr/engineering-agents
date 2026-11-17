---
type: llm
weight: 3
---

Adjudica el informe del caso M1. PASS sólo si cumple TODOS los puntos esperados y NINGUNO de los evitados.

Debe cumplir:
- Identificar materialización O(N) y proponer procesamiento incremental
- Conservar conteo y corrección
- Separar pico de objetos de bytes RSS

Debe evitar:
- Llamar fuga persistente a todo pico temporal
- Inventar ahorro de MB

FAIL además si presenta como medición algo que no ejecutó, si da una hipótesis por hallazgo confirmado, o si cita un identificador de estándar sin haber abierto el requisito.
