# Modelador de Arquitecturas AWS para IA

Aplicación Streamlit didáctica que convierte parámetros de un caso empresarial en una propuesta lógica de arquitectura AWS. El caso inicial es una aseguradora con un asistente documental para el área de siniestros.

## Funcionalidades
- Recomendaciones por capas: datos, integración, inferencia, aplicación, seguridad y observabilidad.
- Adaptación de la clasificación documental según sector, volumen y presencia de PII.
- Matriz RAGA con riesgos y mitigaciones.
- SLO/SLA orientativos, incluyendo latencia, disponibilidad, RTO y RPO.
- Trade-offs explícitos entre velocidad de implantación y control técnico.

## Ejecución
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Parámetros del caso base
| Variable | Valor |
|---|---:|
| Sector | Asegurador |
| Documentos diarios | 18.000 |
| Usuarios simultáneos | 220 |
| Latencia objetivo | ≤ 4 s |
| PII | Sí |
| Presupuesto | Medio |
| Variabilidad de demanda | Media |
| Preferencia estratégica | Gestionado |
| Disponibilidad objetivo | Alta |
| RTO / RPO propuestos | 4 h / 1 h |

## Alcance y limitaciones
- Es un recomendador conceptual; no despliega recursos ni configura una cuenta AWS.
- Las recomendaciones no son un diseño validado ni una cotización.
- No calcula precios reales. Para estimar costes deben concretarse región, servicios, almacenamiento, peticiones, tokens, retención y patrón de uso, y contrastarlos con AWS Pricing Calculator.
- Los objetivos RTO/RPO y SLO son propuestas iniciales; deben aprobarse con negocio y validarse mediante pruebas.
- Amazon Macie y otros servicios de pago deben evaluarse por alcance y coste. Savings Plans solo se consideran para cómputo elegible con consumo estable.
- El selector de sector adapta la clasificación documental, pero no sustituye un análisis regulatorio específico.

## Seguridad
No introduzcas datos personales reales, credenciales ni información confidencial en la aplicación.
