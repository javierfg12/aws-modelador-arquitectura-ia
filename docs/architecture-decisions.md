# Decisiones de arquitectura — Modelador AWS para IA

## ADR-001 — Separar reglas de recomendación de Streamlit

**Decisión:** mantener las reglas en `recommendations.py` y la interfaz en `app.py`.

**Motivo:** permite probar la lógica de decisión sin arrancar la interfaz y reduce el acoplamiento entre widgets y recomendaciones.

**Consecuencia:** las funciones reciben parámetros explícitos y devuelven recomendaciones textuales; no crean recursos AWS.

## ADR-002 — Inferencia gestionada como opción por defecto del caso base

**Decisión:** el caso inicial prioriza un servicio de inferencia gestionado cuando el usuario selecciona esa estrategia.

**Motivo:** reduce carga operativa y acelera un piloto.

**Trade-off:** se renuncia a parte del control fino sobre el modelo y su operación. Una selección de SageMaker u otra alternativa requiere evaluar necesidades reales, experiencia del equipo y costes.

## ADR-003 — PII como restricción transversal

**Decisión:** cuando hay datos personales, las recomendaciones elevan la importancia de minimización, cifrado, control de acceso y auditoría.

**Motivo:** la privacidad no debe tratarse como una capa opcional añadida al final.

**Consecuencia:** el flujo conceptual incluye controles antes y después de la inferencia, además de revisión humana para casos sensibles.

## ADR-004 — RTO/RPO como parámetros de entrada

**Decisión:** exponer RTO y RPO para que la recomendación de aplicación y continuidad no utilice valores implícitos.

**Motivo:** los objetivos de recuperación dependen del impacto de negocio y deben ser acordados con sus responsables.

**Limitación:** el prototipo no ejecuta backups ni pruebas de restauración; solo registra objetivos propuestos.

## Validación antes de producción

1. Confirmar clasificación de datos y base jurídica del tratamiento.
2. Diseñar IAM, red, cifrado, secretos y auditoría.
3. Estimar costes con precios y región reales.
4. Ejecutar pruebas de carga, calidad y seguridad.
5. Ensayar recuperación y comprobar RTO/RPO.
6. Obtener aprobación de arquitectura, seguridad, operaciones y negocio.
