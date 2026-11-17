# Entrega a un auditor externo

Adjunta el ZIP completo o la carpeta del paquete. Para evaluar un especialista, entrega al auditor su SKILL.md y referencias, su perfil canónico y core/contract.md. Para revisar el adaptador Claude, agrega agents/<nombre>.md y scripts/build.py. No entregues esta clave de evaluación al agente que esté resolviendo los casos ciegos.

Prompt para revisar las instrucciones de cada uno de los cuatro agentes:

> Audita este especialista como un artefacto de ingeniería. No asumas que es correcto porque cita documentación. Verifica sus afirmaciones contra fuentes primarias y la versión citada; identifica afirmaciones no sustentadas, instrucciones contradictorias, umbrales arbitrarios, atribuciones incorrectas y huecos de alcance. Comprueba si cada recomendación puede validarse con un experimento y si distingue análisis estático de mediciones. Busca tanto falsos positivos como defectos que podría omitir. Propón un caso positivo, uno negativo y uno de evidencia insuficiente que no estén en sus fixtures publicados. Cita archivo y línea del paquete para cada defecto del agente, y fuente externa cuando aplique. Separa defectos confirmados de preferencias de redacción. Comprueba la equivalencia del adaptador Claude y la skill Codex sin exigir APIs idénticas. Devuelve hallazgos por severidad, contraevidencia, cambio mínimo y prueba que resolvería el desacuerdo. Declara qué no ejecutaste. No modifiques el paquete durante esta revisión.

Ejecuta el prompt por separado sobre:

- scalability-audit: overload, capacidad, tail latency, retry budget, idempotencia y modelo de carga.
- web-security-audit: amenazas alcanzables, autorización por objeto/tenant, trazado hasta sink, controles ASVS y pruebas WSTG.
- data-architecture-audit: propiedad, invariantes, concurrencia, estructuras, contratos y migraciones compatibles.
- memory-data-audit: retención frente a pico, presupuesto de datos en vuelo, streaming, paginación consistente e invalidación de caché.

Luego realiza evaluación conductual ciega según README.md. Una revisión favorable del texto no reemplaza esos runs. Guarda veredictos originales, las fuentes abiertas y la adjudicación de desacuerdos. No hay evidencia todavía de que estos agentes sean superiores a alternativas existentes.
