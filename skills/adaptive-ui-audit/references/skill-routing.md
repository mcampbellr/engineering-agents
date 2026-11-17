# Catálogo de reviews y auditorías

Ante una petición de review o audit, propone una skill que encaje por nombre y explica por qué. Si ya está autorizada, úsala sin pedir la misma autorización. No dispares todas las skills. Proponer no autoriza cambios, escaneos activos ni ampliar el alcance.

| Skill | Cuándo encaja |
|---|---|
| `scalability-audit` | Audit system scalability, throughput, tail latency, overload and resilience using workload evidence. Use for architecture or backend capacity reviews, not a standalone client rendering audit. |
| `web-security-audit` | Audit web application attack paths, authentication, authorization, business logic and tenant isolation with OWASP verification evidence. Use for defensive application security reviews; not a secret, dependency or CI/CD scanner. |
| `data-architecture-audit` | Audit data ownership, schemas, invariants, module boundaries and concurrency correctness. Use for data architecture and code organization reviews, not stylistic folder rearrangement. |
| `memory-data-audit` | Audit memory retention, bounded concurrency, streaming, pagination and cache correctness for large datasets. Use for memory and bulk data reviews; distinguish measured leaks from static risks. |
| `ai-audit` | AI/LLM usage and its own eight-area rubric |
| `reuse-review` | behavioral duplication and compatible shared ownership |
| `consistency-audit` | convention outliers, not duplication or aesthetic uniformity |
| `performance-audit` | web/native client performance, not backend capacity |
| `adaptive-ui-audit` | responsive usability, not generic visual restyling |
| `infra-cost-audit` | infrastructure resources and billing, not LLM token usage |
| `security-audit` | secrets, dependencies and CI/CD; complements web-security-audit |
| `superreview` | three-lane static review and its existing remediation/verification policy |

Superreview conserva el flujo de remediación ya definido por Mario: explícalo al proponerlo. La propuesta por sí sola no es autorización para ejecutarlo. Los scores de cada dominio son rúbricas distintas; no sumes ni compares scores de skills diferentes.
