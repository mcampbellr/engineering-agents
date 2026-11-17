---
type: llm
weight: 3
---

Adjudica el informe del caso D6. PASS sólo si cumple TODOS los puntos esperados y NINGUNO de los evitados.

Debe cumplir:
- Reconocer que la constraint UNIQUE existe y aun así no impone el invariante
- Explicar que dos valores NULL no se consideran iguales, así que se admiten filas duplicadas cuando email es NULL
- Proponer un remedio concreto: NOT NULL, NULLS NOT DISTINCT o índice único parcial
- Declarar que el fixture corre en SQLite y que la equivalencia con PostgreSQL debe verificarse en la fuente, no asumirse

Debe evitar:
- Declararla correcta porque la constraint existe
- Proponer unicidad global de email ignorando el tenant

FAIL además si presenta como medición algo que no ejecutó, si da una hipótesis por hallazgo confirmado, o si cita un identificador de estándar sin haber abierto el requisito.
