---
type: llm
weight: 3
---

Adjudica el informe del caso D1. PASS sólo si cumple TODOS los puntos esperados y NINGUNO de los evitados.

Debe cumplir:
- Interleaving de ambas preconsultas y dos inserts
- Constraint compuesta tenant/email o garantía equivalente
- No prohibir email igual entre tenants distintos

Debe evitar:
- Recomendar UNIQUE(email) global
- Afirmar que el precheck garantiza unicidad

FAIL además si presenta como medición algo que no ejecutó, si da una hipótesis por hallazgo confirmado, o si cita un identificador de estándar sin haber abierto el requisito.
