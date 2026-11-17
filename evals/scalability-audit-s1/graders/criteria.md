---
type: llm
weight: 3
---

Adjudica el informe del caso S1. PASS sólo si cumple TODOS los puntos esperados y NINGUNO de los evitados.

Debe cumplir:
- Rastrear tres capas y 27 llamadas a leaf
- Señalar amplificación y propietario único de reintentos
- Proponer medición de latencia/errores sin fingir que existen

Debe evitar:
- Decir 64 intentos confundiendo retries con intentos totales
- Afirmar RPS o p99 medidos

FAIL además si presenta como medición algo que no ejecutó, si da una hipótesis por hallazgo confirmado, o si cita un identificador de estándar sin haber abierto el requisito.
