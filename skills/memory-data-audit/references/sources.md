# Fuentes primarias

- `node-streams` — [Node.js — Backpressuring in Streams](https://nodejs.org/learn/modules/backpressuring-in-streams). Consulta: 2026-10-26. Respeto de backpressure para controlar acumulación.
- `node-heap` — [Node.js — Using Heap Snapshot](https://nodejs.org/learn/diagnostics/memory/using-heap-snapshot). Consulta: 2026-10-26. Diagnóstico con riesgo de pausa y memoria adicional.
- `python-memory` — [Python — tracemalloc](https://docs.python.org/3/library/tracemalloc.html). Consulta: 2026-10-27. Asignaciones rastreadas y comparación de snapshots; comprobar versión instalada.
- `go-diagnostics` — [Go — Diagnostics](https://go.dev/doc/diagnostics). Consulta: 2026-10-26. Perfiles CPU, memoria, bloqueo y trazas según síntoma.
- `redis-eviction` — [Redis — Key eviction](https://redis.io/docs/latest/develop/reference/eviction/). Consulta: 2026-10-27. Límite de memoria y políticas de eviction; comprobar versión/despliegue.
- `pg-pagination` — [PostgreSQL 18 — LIMIT and OFFSET](https://www.postgresql.org/docs/18/queries-limit.html). Consulta: 2026-10-26. Orden predecible y costo de filas omitidas.
- `pg-isolation` — [PostgreSQL 18 — Transaction Isolation](https://www.postgresql.org/docs/18/transaction-iso.html). Consulta: 2026-10-26. Anomalías, snapshots y serialización; adaptar a motor/versión reales.
- `cgroup-v2` — [Linux kernel — Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html). Consulta: 2026-10-26. memory.max, memory.peak, memory.events/oom_kill y a quién se carga el page cache.
