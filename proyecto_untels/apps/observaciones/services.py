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

def _truncar(texto: str, max_chars: int = 12000) -> str:
    if len(texto) <= max_chars:
        return texto
    return texto[:max_chars] + "\n... [contenido truncado por limite de tamaño]"


def validar_informe(contenido_informe: str, reglamento: str, observaciones: str) -> list:
    contenido_informe = _truncar(contenido_informe, 12000)
    reglamento = _truncar(reglamento, 4000)
    observaciones = _truncar(observaciones, 2000)

    secciones = [
        "Constancia de acreditación de Prácticas Preprofesionales (Art. 29)",
        "Estructura del informe (Art. 31, Art. 33)",
        "Carátula",
        "Introducción",
        "Objetivos",
        "Importancia",
        "Alcance y Limitaciones",
        "Información General de la empresa + Art. 20",
        "Resumen",
        "Descripción del trabajo desarrollado (alineado a los objetivos)",
        "Conclusiones",
        "Recomendaciones",
        "Referencias bibliográficas",
        "Evidencias",
        "Glosario de términos",
        "Cálculos y/o procedimientos complementarios",
        "Diagramas y/o figuras complementarias",
        "Normas técnicas",
        "Formatos técnicos varios",
    ]
    lista_secciones = "\n".join(f"{i+1}. {s}" for i, s in enumerate(secciones))

    prompt = f"""Eres un evaluador academico de la UNTELS (Universidad Nacional Tecnologica de Lima Sur).
Analiza el siguiente informe de practicas preprofesionales.
Compara el contenido con el reglamento y el banco de observaciones proporcionados.

REGLAMENTO DE EVALUACION:
{reglamento}

BANCO DE OBSERVACIONES FRECUENTES:
{observaciones}

INFORME A EVALUAR:
{contenido_informe}

Debes evaluar EXACTAMENTE las siguientes 19 secciones del informe:
{lista_secciones}

Para CADA seccion, determina si el informe cumple ("Conforme") o tiene problemas ("Observado").

REGLAS PARA LAS OBSERVACIONES:
- Si una seccion NO existe en el informe, indica EXACTAMENTE que elementos o contenido falta. Ejemplo: "Falta la seccion de Evidencias: no se incluyen capturas de pantalla, fotos u otros medios que demuestren el trabajo realizado".
- Si una seccion EXISTE pero tiene errores, describe el error ESPECIFICO. Ejemplo: "El correo electronico del autor no usa el dominio institucional @untels.edu.pe" o "Se listan 3 referencias bibliograficas pero ninguna esta citada dentro del texto del informe".
- Si una seccion esta incompleta, detalla que le falta. Ejemplo: "La seccion de Objetivos solo presenta el objetivo general, faltan los objetivos especificos".
- NUNCA uses observaciones genericas como "No se encuentra en el informe" sin explicar que se esperaba encontrar.
- El campo "sustento" debe citar el articulo especifico del reglamento que respalda la observacion.

Devuelve UNICAMENTE una lista JSON valida (sin markdown, sin explicaciones) con las 19 secciones.
Formato exacto:
[
  {{
    "item": 1,
    "descripcion": "nombre de la seccion evaluada",
    "observacion": "descripcion DETALLADA y ESPECIFICA del problema (vacio si es Conforme)",
    "sustento": "articulo del reglamento que sustenta la observacion (vacio si es Conforme)",
    "estado": "Observado o Conforme"
  }}
]

IMPORTANTE: Siempre devuelve las 19 secciones, incluso las que estan Conforme."""

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
