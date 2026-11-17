# Engineering Agents · 0.2.1

Paquete personal de 12 skills de ingeniería para Claude Code y Codex. Una fuente editable por workflow, adaptadores generados, formato compartido de resultados y detalles propios de cada especialidad.

| Skill | Alcance |
|---|---|
| `scalability-audit` | Capacidad, colas, concurrencia, overload, latencia y reintentos de backend |
| `web-security-audit` | Rutas de ataque, authn/authz, lógica de negocio y aislamiento entre tenants |
| `data-architecture-audit` | Propiedad, modelos, invariantes, transacciones, índices y migraciones |
| `memory-data-audit` | Retención, límites de memoria, streaming, batches, cursores y caché |
| `ai-audit` | Integraciones LLM, prompts, tokens, agentes, observabilidad, evals y seguridad de IA |
| `performance-audit` | Rendimiento del cliente web/native: carga, render, bundles y solicitudes |
| `adaptive-ui-audit` | Responsive, overflow, breakpoints, safe areas, teclado y reflow |
| `infra-cost-audit` | Recursos de infraestructura, dimensionamiento y riesgo de gasto operativo |
| `security-audit` | Secretos, archivos sensibles, dependencias, supply chain y CI/CD |
| `reuse-review` | Duplicación semántica y reutilización compatible con ubicaciones de ambos lados |
| `consistency-audit` | Outliers de implementación dentro del mismo contexto semántico |
| `superreview` | Tres lanes estáticos, síntesis y política existente de corrección/verificación |

`SKILLS.md` se genera desde el catálogo e incluye criterios de selección. Ante una review o auditoría, los agentes proponen una skill apropiada por nombre y explican por qué. Una propuesta no inicia todas las auditorías ni autoriza cambios. Si ya elegiste una skill, no vuelven a pedir la misma autorización. La preferencia canónica está en Agent Memory (`mem-propose-matching-skills-for-reviews-audits`) y se despliega en las instrucciones globales Claude/Codex.

## Repositorio público

Este repositorio reúne las 12 skills del paquete, sus 25 agentes, fuentes editables, referencias, validadores y pruebas. Conserva la licencia y las atribuciones originales.

```sh
git clone https://github.com/mcampbellr/engineering-agents.git
cd engineering-agents
```

Para cargar el plugin en una sesión de Claude Code:

```sh
claude --plugin-dir /ruta/absoluta/engineering-agents
```

Para Codex, enlaza las carpetas de `skills/` en tu directorio de skills, conservando el paquete completo para sus herramientas de desarrollo. La sección siguiente documenta la instalación personal original; no es un requisito para usar esta copia.

## Uso permanente

El origen personal está en `~/.dotfiles/plugins/engineering-agents/` en Mac. Claude se instala a nivel de usuario desde el marketplace de dotfiles:

```sh
claude plugin install engineering-agents --marketplace /ruta/absoluta/dotfiles --scope user
```

En Cerebro el mismo paquete se instala desde `mcampbellr/.dotfiles` con el instalador nativo. Tras actualizar el marketplace y el plugin, abre una sesión nueva. No hace falta `--plugin-dir` ni una carpeta de trabajo auxiliar.

Invoca `/engineering-agents:ai-audit`, `/engineering-agents:reuse-review`, etc. En Claude sólo se distribuyen las entradas nuevas del plugin: se retiraron los ocho accesos standalone y los tres reviewers globales duplicados. Usa los nombres engineering-agents:<skill> y sus agentes del paquete. Tras una actualización nativa, `scripts/deploy_local.py --root <origen-permanente>` prepara un plan; aplícalo con `--apply --expected-state <plan.json>` para retirar accesos Claude antiguos y sincronizar los enlaces nuevos de Codex y la instrucción global sin reemplazar ediciones concurrentes. Los directorios anteriores se respaldan en `~/.local/state/engineering-agents/migrations/`. Los subagentes registrados tienen nombres propios; para los workflows migrados, `references/dispatch.md` relaciona recetas con los nombres Claude. Si el host no permite delegación o anidación, el padre conserva el orden del flujo y declara la limitación.

Codex descubre las 12 skills desde el manifiesto portable `plugin.json`. Puede usarlas como plugin o enlazando las carpetas a su directorio de skills. Descubrir un plugin no significa instalarlo ni haber evaluado la calidad de sus respuestas. El paquete no instala Codex CLI.

## Salida común y detalle de dominio

Los reportes exportados usan `reports/<skill>/<run-id>/report.md` y `report.json`. Las salidas comparten alcance/veredicto, hallazgos con evidencia, severidad, confianza y estado, validación/cobertura, limitaciones y siguientes pasos. `core/output-contract.md` define la forma común; el JSON se valida con `core/report.schema.json` y el validador empaquetado.

El campo `domain` conserva scores, breakdowns, secciones legales orientativas, observaciones de UI, perfiles de costo y verificaciones por lane. No se suman scores de skills diferentes ni se presentan como métricas de producción. Los reportes originales de 13/16 secciones se conservan como detalle de dominio, no como un formato competidor. Las rutas originales de artefactos se remapean por run-id para no mezclar ejecuciones.

Cada workflow conserva sus límites: `consistency-audit` pregunta antes de remediar; `superreview` conserva el flujo de corrección de bloqueantes de Mario y entrega verificación dinámica a un verificador serial. Proponer cualquiera de estas skills no autoriza ese flujo por sí solo. Ningún perfil instala scanners o servicios para completar una auditoría.

## Fuente única

- `profiles/` + `core/` + `sources.json`: los cuatro especialistas originales.
- `source-skills/<skill>/`: fuentes editables de las ocho skills migradas y sus recursos.
- `catalog.json`: nombres, descripciones, alcance y agentes de todas las skills.
- `migration-provenance.json`: inventario y hashes de las fuentes antes de adaptarlas.
- `skills/`, `agents/`, `evals/`, `SKILLS.md`, manifests y `SHA256SUMS`: generados; no editar a mano.

`ai-audit`, performance, responsive UI, consistencia, infra y reuse proceden de la Mac. Security y Superreview proceden de la copia más reciente de Cerebro, incluidas las restricciones estáticas y el policy compartido. Superreview incluye sus tres reviewers y los tres recursos anti-slop que utilizaban; no depende de una skill global anti-slop para leerlos. No se copiaron credenciales, hooks, configuración de proveedores ni modelos fijos.

Las fuentes migradas conservan su atribución y licencia declarada; el paquete no inventa una licencia para archivos que no la declaran. Los modelos simbólicos cheap/mid/frontier se interpretan como etiquetas históricas de complejidad; los agentes heredan el modelo del usuario.

## Verificación

```sh
python3 scripts/build.py
python3 scripts/build.py --check
python3 evaluation/run_fixtures.py
python3 evaluation/schema_invariants.py
python3 evaluation/test_validation.py
python3 evaluation/test_bundle.py
claude plugin validate .
```

El generador usa sólo stdlib. Para validar JSON y ejecutar pruebas del esquema, instala `requirements-validation.txt` en un entorno Python fuera del paquete. Ausencia de `jsonschema` termina con código 2, nunca como éxito. Cada skill lleva el validador, esquema y requisitos para ser autocontenida.

Esta migración comprueba carga, referencias, generación, retirada de entradas antiguas, formato y compatibilidad. No es una nueva evaluación de la profundidad técnica de todas las reglas. El frontmatter de `security-audit` conserva los campos Claude que limitan invocación y herramientas: el validador genérico de skills no reconoce esos tres campos, pero los anfitriones Claude y Codex sí cargan las 12 skills; Codex conserva además su política de invocación explícita en openai.yaml.

La suite de 18 casos existente cubre los cuatro perfiles originales. La investigación W9 y el desacuerdo de adjudicación permanecen en `evaluation/w9-investigation.json`; no se afirman resultados para las ocho migraciones ni mejora frente a un modelo sin skills. No se lanzaron evaluaciones de pago para esta migración. Las referencias técnicas o legales importadas deben verificarse contra fuentes primarias vigentes antes de usarlas en un audit real.
