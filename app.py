import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Modelador AWS para IA",
    layout="wide",
    page_icon="🏗️"
)

# ─────────────────────────────────────────────
# CASO BASE
# ─────────────────────────────────────────────
CASO_BASE = {
    "sector": "Asegurador",
    "documentos_diarios": 18000,
    "usuarios_simultaneos": 220,
    "latencia_max_seg": 4,
    "pii": True,
    "presupuesto": "Medio",
    "variabilidad_demanda": "Media",
    "preferencia_estrategica": "Gestionado",
    "disponibilidad_objetivo": "Alta",
    "rto_horas": 4,
    "rpo_horas": 1,
}

# ─────────────────────────────────────────────
# REGLAS DE DECISIÓN
# ─────────────────────────────────────────────

from recommendations import (
    recomendar_inferencia,
    recomendar_seguridad,
    recomendar_datos,
    recomendar_integracion,
    recomendar_observabilidad,
    recomendar_aplicacion,
    recomendar_tradeoff,
)


# ─────────────────────────────────────────────
# GENERADORES DE OUTPUT
# ─────────────────────────────────────────────

def generar_capas(datos):
    return {
        "1. Datos": recomendar_datos(
            datos["documentos_diarios"], datos["pii"], datos["sector"]
        ),
        "2. Integración": recomendar_integracion(
            datos["latencia_max_seg"], datos["usuarios_simultaneos"]
        ),
        "3. Inferencia / Modelo": recomendar_inferencia(
            datos["preferencia_estrategica"]
        ),
        "4. Aplicación": recomendar_aplicacion(
            datos["disponibilidad_objetivo"], datos["rto_horas"], datos["rpo_horas"]
        ),
        "5. Seguridad y Gobierno": recomendar_seguridad(
            datos["pii"], datos["presupuesto"]
        ),
        "6. Observabilidad y FinOps": recomendar_observabilidad(
            datos["variabilidad_demanda"], datos["presupuesto"]
        ),
    }


def generar_riesgos(datos):
    riesgos = [
        {
            "Riesgo": "Exposición de datos personales sensibles (PII)",
            "Mitigación": "Minimización en cada capa, revisión humana, cifrado KMS y auditoría CloudTrail.",
            "Rol responsable": "Compliance + CISO",
            "Acción inmediata": "Validar tratamiento de PII antes del despliegue.",
        },
        {
            "Riesgo": f"Latencia superior al objetivo (>{datos['latencia_max_seg']}s)",
            "Mitigación": "Caché de respuestas frecuentes, optimización de embeddings y pruebas de carga.",
            "Rol responsable": "Arquitecto SI/TI",
            "Acción inmediata": "Definir y ejecutar pruebas de rendimiento en staging.",
        },
        {
            "Riesgo": "Sobrecoste de inferencia por variabilidad de demanda",
            "Mitigación": "AWS Budgets, Cost Anomaly Detection, límites de gasto y revisión periódica del consumo.",
            "Rol responsable": "FinOps / Responsable de Operación",
            "Acción inmediata": "Establecer presupuesto mensual y umbral de alerta.",
        },
    ]
    return pd.DataFrame(riesgos)


def generar_slos(datos):
    # Mapeo de disponibilidad_objetivo a porcentaje SLA orientativo
    disponibilidad_map = {
        "Media": "99,5 %",
        "Alta": "99,9 %",
        "Muy alta": "99,99 %",
    }
    slos = [
        {
            "Indicador": "Latencia de respuesta (p95)",
            "Valor objetivo": f"≤ {datos['latencia_max_seg']} s",
            "Cómo medirlo": "CloudWatch Metric — API Gateway latency p95",
        },
        {
            "Indicador": "Disponibilidad del servicio",
            "Valor objetivo": disponibilidad_map.get(datos["disponibilidad_objetivo"], "—"),
            "Cómo medirlo": "CloudWatch Synthetics (canarios) + health checks",
        },
        {
            "Indicador": "Tasa de escalado a gestor humano",
            "Valor objetivo": "< 15 % de consultas",
            "Cómo medirlo": "Métrica personalizada en CloudWatch desde la lógica de la app",
        },
        {
            "Indicador": "RTO (tiempo máximo de recuperación)",
            "Valor objetivo": f"≤ {datos['rto_horas']} h",
            "Cómo medirlo": "Ejercicios de recuperación y registro de incidentes",
        },
        {
            "Indicador": "RPO (pérdida máxima de datos)",
            "Valor objetivo": f"≤ {datos['rpo_horas']} h",
            "Cómo medirlo": "Pruebas de restauración y validación de backups",
        },
    ]
    return pd.DataFrame(slos)


# ─────────────────────────────────────────────
# SIDEBAR — INPUTS
# ─────────────────────────────────────────────

st.sidebar.header("⚙️ Parámetros del caso")
st.sidebar.caption("Caso base: Aseguradora — área de siniestros")

sector = st.sidebar.text_input("Sector", CASO_BASE["sector"])
documentos_diarios = st.sidebar.number_input(
    "Documentos diarios", min_value=0, value=CASO_BASE["documentos_diarios"]
)
usuarios_simultaneos = st.sidebar.number_input(
    "Usuarios simultáneos", min_value=0, value=CASO_BASE["usuarios_simultaneos"]
)
latencia_max_seg = st.sidebar.number_input(
    "Latencia máxima (s)", min_value=1, value=CASO_BASE["latencia_max_seg"]
)
pii = st.sidebar.checkbox(
    "¿Hay datos personales sensibles (PII)?", value=CASO_BASE["pii"]
)
presupuesto = st.sidebar.selectbox(
    "Presupuesto", ["Bajo", "Medio", "Alto"], index=1
)
variabilidad_demanda = st.sidebar.selectbox(
    "Variabilidad de la demanda", ["Baja", "Media", "Alta"], index=1
)
preferencia_estrategica = st.sidebar.selectbox(
    "Preferencia estratégica", ["Gestionado", "Control fino"], index=0
)
disponibilidad_objetivo = st.sidebar.selectbox(
    "Disponibilidad objetivo", ["Media", "Alta", "Muy alta"], index=1
)
rto_horas = st.sidebar.number_input("RTO objetivo (horas)", min_value=0, value=CASO_BASE["rto_horas"], step=1)
rpo_horas = st.sidebar.number_input("RPO objetivo (horas)", min_value=0, value=CASO_BASE["rpo_horas"], step=1)

datos = {
    "sector": sector,
    "documentos_diarios": documentos_diarios,
    "usuarios_simultaneos": usuarios_simultaneos,
    "latencia_max_seg": latencia_max_seg,
    "pii": pii,
    "presupuesto": presupuesto,
    "variabilidad_demanda": variabilidad_demanda,
    "preferencia_estrategica": preferencia_estrategica,
    "disponibilidad_objetivo": disponibilidad_objetivo,
    "rto_horas": rto_horas,
    "rpo_horas": rpo_horas,
}

# ─────────────────────────────────────────────
# MAIN — OUTPUT EJECUTIVO
# ─────────────────────────────────────────────

st.title("🏗️ Modelador de Arquitecturas AWS para IA")

st.divider()

# ── 1. RESUMEN EJECUTIVO ──────────────────────
st.subheader("📋 1. Resumen ejecutivo")

modo = "simplicidad operativa y velocidad de lanzamiento" \
    if datos["preferencia_estrategica"] == "Gestionado" \
    else "control fino del modelo y personalización"

pii_nota = (
    " La presencia de PII eleva el nivel de exigencia en seguridad y cumplimiento normativo."
    if datos["pii"] else ""
)

st.info(
    f"**Sector:** {datos['sector']}  \n"
    f"**Problema operativo:** Asistente interno para búsqueda documental, borradores de respuesta "
    f"y apoyo a gestores del sector {datos['sector'] or 'no especificado'}.  \\n"
    f"**Criterio dominante:** {modo.capitalize()}, con restricciones de latencia "
    f"(≤{datos['latencia_max_seg']} s), presupuesto {datos['presupuesto'].lower()} "
    f"y disponibilidad {datos['disponibilidad_objetivo'].lower()}.{pii_nota}"
)

st.divider()

# ── 2. ARQUITECTURA POR CAPAS ─────────────────
st.subheader("🗂️ 2. Arquitectura propuesta por capas")

capas = generar_capas(datos)
iconos = ["🗄️", "🔗", "🤖", "💻", "🔒", "📊"]
for (capa, descripcion), icono in zip(capas.items(), iconos):
    with st.expander(f"{icono} {capa}", expanded=True):
        st.write(descripcion)

st.divider()

# ── 3. TRADE-OFF PRINCIPAL ────────────────────
st.subheader("⚖️ 3. Trade-off principal")
st.warning(recomendar_tradeoff(
    datos["preferencia_estrategica"],
    datos["pii"],
    datos["presupuesto"]
))

st.divider()

# ── 4. MATRIZ RAGA ────────────────────────────
st.subheader("🚦 4. Matriz RAGA — Riesgos, Alternativas, Gobernanza y Acciones")
st.dataframe(generar_riesgos(datos), use_container_width=True, hide_index=True)

st.divider()

# ── 5. SLO / SLA ──────────────────────────────
st.subheader("📏 5. SLO / SLA propuestos")
st.dataframe(generar_slos(datos), use_container_width=True, hide_index=True)

st.divider()

# ── 6. REFLEXIÓN DEL EQUIPO ───────────────────
st.subheader("💬 6. Reflexión del equipo")
motor_inferencia = "Amazon Bedrock" if datos["preferencia_estrategica"] == "Gestionado" else "Amazon SageMaker"
tradeoff_pii = (
    "La presencia de PII exige controles estrictos y puede aumentar la latencia percibida. "
    "Calibra el escalado a gestor humano con datos del piloto."
    if datos["pii"] else
    "Aunque no se ha indicado PII, deben mantenerse controles de acceso, cifrado y auditoría."
)
variabilidad_texto = datos["variabilidad_demanda"].lower()
st.success(
    f"**Decisión principal:** Se propone {motor_inferencia} según la preferencia "
    f"estratégica seleccionada ({datos['preferencia_estrategica']}).  \\n\\n"
    f"**Trade-off aceptado:** {recomendar_tradeoff(datos['preferencia_estrategica'], datos['pii'], datos['presupuesto'])}  \\n\\n"
    f"**Riesgo y control:** {tradeoff_pii}  \\n\\n"
    f"**Siguiente validación:** Ejecutar pruebas de carga para comprobar que la latencia p95 "
    f"se mantiene ≤{datos['latencia_max_seg']} s con los controles activos y revisar el "
    f"autoescalado según la variabilidad {variabilidad_texto} de la demanda."
)