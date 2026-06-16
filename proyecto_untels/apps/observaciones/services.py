import json
import re
import anthropic
from django.conf import settings
from .models import BancoObservaciones

def obtener_observaciones() -> str:
    obs = BancoObservaciones.objects.all()
    if not obs:
        return "No hay observaciones en el banco."
    lineas = [f"- [{o.seccion}]: {o.descripcion}" for o in obs]
    return '\n'.join(lineas)

def validar_informe(contenido_informe: str, reglamento: str, observaciones: str) -> list:
    prompt = f"""Eres un evaluador académico de la UNTELS (Universidad Nacional Tecnológica de Lima Sur).
Analiza el siguiente informe de prácticas preprofesionales.
Compara el contenido con el reglamento y el banco de observaciones proporcionados.

REGLAMENTO DE EVALUACIÓN:
{reglamento}

BANCO DE OBSERVACIONES FRECUENTES:
{observaciones}

INFORME A EVALUAR:
{contenido_informe}

Devuelve ÚNICAMENTE una lista JSON válida (sin markdown, sin explicaciones) con las observaciones encontradas.
Formato exacto:
[
  {{
    "id": 1,
    "seccion": "nombre de la sección",
    "observacion": "descripción del problema encontrado",
    "ubicacion": "lugar donde se encuentra el error"
  }}
]

Si el informe cumple con todo, devuelve una lista vacía: []"""

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    texto = response.content[0].text.strip()
    texto = re.sub(r'```(?:json)?\s*', '', texto).strip('`').strip()

    return json.loads(texto)
