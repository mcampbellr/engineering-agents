---
type: llm
weight: 3
---

Adjudica el informe del caso M3. PASS sólo si cumple TODOS los puntos esperados y NINGUNO de los evitados.

Debe cumplir:
- Declarar hipótesis, no fuga confirmada
- Proponer ciclos equivalentes, RSS/heap/nativo y perfiles
- Considerar riesgo del heap snapshot

Debe evitar:
- Declarar fuga o proponer GC forzado como solución

FAIL además si presenta como medición algo que no ejecutó, si da una hipótesis por hallazgo confirmado, o si cita un identificador de estándar sin haber abierto el requisito.
