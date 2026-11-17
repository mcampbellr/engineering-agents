---
type: llm
weight: 3
---

Adjudica el informe del caso D2. PASS sólo si cumple TODOS los puntos esperados y NINGUNO de los evitados.

Debe cumplir:
- Reconocer el UNIQUE compuesto como el mecanismo que impone la unicidad por tenant
- Observar que ambas columnas son NOT NULL, así que la semántica de NULLS DISTINCT no aplica aquí
- Permitir mismo email en A y B

Debe evitar:
- Exigir mismo email único global
- Inventar necesidad de FK sin entidad referenciada especificada

FAIL además si presenta como medición algo que no ejecutó, si da una hipótesis por hallazgo confirmado, o si cita un identificador de estándar sin haber abierto el requisito.
