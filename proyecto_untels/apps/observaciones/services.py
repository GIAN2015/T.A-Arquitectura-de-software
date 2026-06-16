import json
import re
import google.generativeai as genai
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

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    texto = response.text.strip()
    texto = re.sub(r'```(?:json)?\s*', '', texto).strip('`').strip()

    return json.loads(texto)
