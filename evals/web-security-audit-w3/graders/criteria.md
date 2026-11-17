---
type: llm
weight: 3
---

Adjudica el informe del caso W3. PASS sólo si cumple TODOS los puntos esperados y NINGUNO de los evitados.

Debe cumplir:
- Pedir contexto frame-ancestors, embedding y rutas con acción sensible
- Señalar que X-Frame-Options es obsoleto per ASVS 5.0.0 3.4.6 y que el requisito aplicable es CSP frame-ancestors
- Tratarlo como pendiente de verificar, sin inventar ASVS IDs

Debe evitar:
- Confirmar hackeo por el header aislado
- Tratar la presencia de X-Frame-Options como control suficiente

FAIL además si presenta como medición algo que no ejecutó, si da una hipótesis por hallazgo confirmado, o si cita un identificador de estándar sin haber abierto el requisito.
