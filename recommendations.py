"""Reglas puras de recomendación para el modelador de arquitectura AWS.

Estas funciones no dependen de Streamlit ni realizan llamadas a AWS, por lo que
pueden probarse de forma aislada.
"""

def recomendar_inferencia(preferencia_estrategica):
    """Regla 4 y 5: inferencia según preferencia estratégica."""
    if preferencia_estrategica == "Gestionado":
        return "Amazon Bedrock — modelo gestionado, menor overhead operativo."
    return "Amazon SageMaker — control fino del modelo, mayor personalización."


def recomendar_seguridad(pii, presupuesto):
    """
    Regla 6 (reforzada): si hay PII, se añaden controles avanzados.
    Si además el presupuesto es Bajo, se prioriza minimización estricta
    sobre herramientas de terceros para no sobrecostear.
    """
    if pii:
        base = (
            "Controles reforzados: cifrado en tránsito y en reposo (KMS), "
            "minimización de datos en cada capa, revisión humana obligatoria "
            "en casos sensibles, políticas IAM de mínimo privilegio, "
            "auditoría con AWS CloudTrail y conformidad RGPD/LOPD."
        )
        if presupuesto == "Bajo":
            base += (
                " Dado el presupuesto ajustado, se priorizan controles nativos "
                "de AWS (IAM, KMS, CloudTrail) antes de soluciones de terceros."
            )
        return base
    return (
        "Controles estándar: IAM con mínimo privilegio, cifrado en reposo "
        "y monitoreo básico con CloudWatch."
    )


def recomendar_datos(documentos_diarios, pii, sector):
    """Capa de datos adaptada al volumen y sensibilidad."""
    sector_norm = sector.strip().lower()
    categoria = "tipo de siniestro" if any(term in sector_norm for term in ("asegur", "financ", "banca")) else "tipo documental"
    if documentos_diarios > 10000 and pii:
        return (
            "S3 con clasificación de datos sensibles (evaluar Amazon Macie según alcance y coste). "
            f"Particionado por fecha y {categoria}. "
            "Definir política de retención, borrado y acceso por expediente."
        )
    if documentos_diarios > 10000:
        return (
            f"S3 con particionado por fecha y {categoria}. "
            "Ingesta a través de AWS Glue para normalización documental."
        )
    return "S3 estándar con catálogo básico en AWS Glue."


def recomendar_integracion(latencia_max_seg, usuarios_simultaneos):
    """
    Regla 7 (reforzada): si la latencia es baja, se explicita
    preocupación por rendimiento y se añade caché.
    """
    partes = [
        "API Gateway + AWS Lambda para orquestación de flujos documentales."
    ]
    if latencia_max_seg <= 4:
        partes.append(
            f"⚠️ Latencia objetivo ≤{latencia_max_seg}s: se recomienda caché "
            "de respuestas frecuentes (ElastiCache/Redis) y optimización "
            "del pipeline de embeddings."
        )
    if usuarios_simultaneos > 100:
        partes.append(
            f"Con {usuarios_simultaneos} usuarios concurrentes, el diseño debe "
            "contemplar auto-scaling en Lambda y throttling en API Gateway."
        )
    return " ".join(partes)


def recomendar_observabilidad(variabilidad_demanda, presupuesto):
    """
    Regla 8 (reforzada): alta variabilidad → observabilidad + control de costes.
    Regla 10: presupuesto bajo → evitar sobredimensionamiento.
    """
    if variabilidad_demanda == "Alta":
        obs = (
            "CloudWatch con dashboards en tiempo real, alertas automáticas de coste "
            "(AWS Budgets + Cost Anomaly Detection), métricas de inferencia y "
            "rastreo distribuido con AWS X-Ray."
        )
    elif variabilidad_demanda == "Media":
        obs = (
            "Monitoreo continuo con CloudWatch Metrics y revisión semanal de consumo. "
            "Alertas sobre latencia p95 y tasa de error."
        )
    else:
        obs = "Observabilidad básica con CloudWatch Logs y revisión mensual de KPIs."

    if presupuesto == "Bajo":
        obs += (
            " FinOps: AWS Budgets, Cost Anomaly Detection y revisión de rightsizing. "
            "Evaluar Savings Plans solo para cómputo elegible con demanda estable y tras analizar el uso."
        )
    return obs


def recomendar_aplicacion(disponibilidad_objetivo, rto_horas, rpo_horas):
    """Regla 9: alta/muy alta disponibilidad → resiliencia explícita."""
    base = "Interfaz web interna para gestores y analistas (React o Streamlit interno)."
    if disponibilidad_objetivo in ("Alta", "Muy alta"):
        base += (
            f" Dado el objetivo '{disponibilidad_objetivo}', el despliegue debe "
            f"contemplar multi-AZ, health checks y objetivos explícitos: RTO ≤{rto_horas} h y RPO ≤{rpo_horas} h."
        )
    else:
        base += f" Definir y probar objetivos de recuperación: RTO ≤{rto_horas} h y RPO ≤{rpo_horas} h."
    return base


def recomendar_tradeoff(preferencia_estrategica, pii, presupuesto):
    """Trade-off principal explícito y justificado."""
    if preferencia_estrategica == "Gestionado":
        tradeoff = (
            "**Velocidad de lanzamiento vs. control operativo.** "
            "Se elige Amazon Bedrock por su menor overhead de mantenimiento, "
            "asumiendo que la aseguradora prioriza llegar a producción rápido "
            "sobre tener control total del modelo subyacente."
        )
    else:
        tradeoff = (
            "**Control fino vs. velocidad de despliegue.** "
            "Se elige SageMaker para maximizar la personalización del modelo, "
            "asumiendo capacidad interna de MLOps. "
            "El coste operativo y el tiempo de despliegue serán mayores."
        )
    if pii and presupuesto == "Medio":
        tradeoff += (
            " La presencia de PII añade un segundo trade-off: "
            "**seguridad vs. rendimiento** — los controles de anonimización "
            "y revisión humana aumentan la latencia, por lo que el equipo "
            "debe fijar el umbral de escalado a gestor humano con cuidado."
        )
    return tradeoff


