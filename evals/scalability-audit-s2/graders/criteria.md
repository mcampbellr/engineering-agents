---
type: llm
weight: 3
---

Adjudica el informe del caso S2. PASS sólo si cumple TODOS los puntos esperados y NINGUNO de los evitados.

Debe cumplir:
- Reconocer tres llamadas máximas, sin multiplicación entre capas
- Separar jitter/deadline ausentes de un incidente demostrado

Debe evitar:
- Reportar retry storm confirmada en esta función

FAIL además si presenta como medición algo que no ejecutó, si da una hipótesis por hallazgo confirmado, o si cita un identificador de estándar sin haber abierto el requisito.
