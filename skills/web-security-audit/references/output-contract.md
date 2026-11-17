# Formato compartido de salida

Separa la envoltura comparable del detalle propio de cada especialidad. Mantén este formato también al integrar una skill legada. El formato no implica que todas las skills tengan la misma cobertura, scoring o permisos.

## Markdown
1. Alcance y veredicto: skill, run-id, repo/revisión, qué se revisó y qué quedó fuera; requires_changes, inconclusive o no_blocking_findings.
2. Hallazgos por impacto: ID, severidad, confianza, estado de evidencia y estado de resolución; ubicación, problema/condición, impacto, controles/contraevidencia, arreglo mínimo y tradeoffs.
3. Detalle de dominio: las secciones y rubricas que correspondan a AI, performance, seguridad, responsive UI, infraestructura o revisión por lanes. Aquí se conservan los breakdowns de scoring y sus formatos originales.
4. Validación y cobertura: controles pass/fail/not_tested/not_applicable; pruebas ejecutadas con evidencia frente a propuestas. Superreview conserva su tabla key/requested_by/kind/scope/command/reason como plan serial, sin ejecutarlo.
5. Limitaciones y siguientes pasos: datos faltantes, decisiones necesarias y remediación autorizada. Si hubo cambios, distingue estado previo, fixed estático y verificación dinámica pendiente.

En chat resume hallazgos y límites con estos mismos conceptos sin forzar archivos o un informe largo. Cada hallazgo tiene evidencia propia; agrupa por causa raíz. Un score de dominio es una heurística de su rúbrica, no una medición de producción ni una certificación. No agregues un score global entre skills.

## JSON
Usa references/report.schema.json y el validador empaquetado scripts/validate_report.py con --repo <repositorio>. Excepción de ejecución: Superreview es estático; entrega el JSON y delega la ejecución del validador al mismo verificador serial que ejecutaría su plan. Declara esa validación como no ejecutada en domain, sin quebrar su frontera estática. Completa los campos comunes: schema_version, package_version, skill, run_id, scope, environment, verdict, findings, controls, metrics, sources, limitations y next_steps. Usa null para desconocidos; metrics contiene sólo mediciones/propuestas con su instrumentación, no scores de una rúbrica.

El campo opcional domain conserva los datos particulares: scores y pesos, postura heurística, observaciones de UI, perfil de costo, verificaciones por lane y plan de remediación. Una salida legacy JSON puede preservarse íntegra dentro de domain; sus findings no sustituyen los findings normalizados de arriba. Si un valor de domain no fue medido, decláralo en ese bloque; el esquema común no valida su rúbrica particular.

Severidades normalizadas: CRITICAL→critical, HIGH→high, MEDIUM→medium, LOW→low; MAJOR de Superreview→high y MINOR→low. Conserva la severidad original en el detalle de dominio si añade contexto. No eleves por estilo. Los hallazgos pueden incluir status=open|fixed|pending_decision|follow_up (omitido significa open). Fixed debe especificar en validación qué se comprobó y qué quedó pendiente, sin fingir ejecución dinámica.

BLOCKED/REQUIRES CHANGES→requires_changes; APPROVED→no_blocking_findings sólo en el alcance verificado; evidencia insuficiente→inconclusive. El veredicto post-fix evalúa los hallazgos abiertos; conserva el veredicto anterior y los cambios en domain. No uses una etiqueta de Production-Ready de una rúbrica legada como garantía del sistema.
