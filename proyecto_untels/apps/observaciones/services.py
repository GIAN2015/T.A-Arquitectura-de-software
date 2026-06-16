import json
import re
import requests
from django.conf import settings
from .models import BancoObservaciones

def obtener_observaciones() -> str:
    obs = BancoObservaciones.objects.all()
    if not obs:
        return "No hay observaciones en el banco."
    lineas = [f"- [{o.seccion}]: {o.descripcion}" for o in obs]
    return '\n'.join(lineas)

def validar_informe(contenido_informe: str, reglamento: str, observaciones: str) -> list:
    prompt = f"""Eres un evaluador academico de la UNTELS (Universidad Nacional Tecnologica de Lima Sur).
Analiza el siguiente informe de practicas preprofesionales.
Compara el contenido con el reglamento y el banco de observaciones proporcionados.

REGLAMENTO DE EVALUACION:
{reglamento}

BANCO DE OBSERVACIONES FRECUENTES:
{observaciones}

INFORME A EVALUAR:
{contenido_informe}

Devuelve UNICAMENTE una lista JSON valida (sin markdown, sin explicaciones) con las observaciones encontradas.
Formato exacto:
[
  {{
    "id": 1,
    "seccion": "nombre de la seccion",
    "observacion": "descripcion del problema encontrado",
    "ubicacion": "lugar donde se encuentra el error"
  }}
]

Si el informe cumple con todo, devuelve una lista vacia: []"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()

    texto = response.json()["choices"][0]["message"]["content"].strip()
    texto = re.sub(r'```(?:json)?\s*', '', texto).strip('`').strip()

    return json.loads(texto)
