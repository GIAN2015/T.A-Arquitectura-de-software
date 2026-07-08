"""
Servicio de validación de informes con IA
Capa de Servicios - Lógica de negocio para validación automática
"""
import json
import re
import requests
from django.conf import settings
from .models import BancoObservaciones


def obtener_observaciones() -> str:
    """Obtiene el banco de observaciones formateado"""
    obs = BancoObservaciones.objects.all()
    if not obs:
        return "No hay observaciones en el banco."
    lineas = [f"- [{o.seccion}]: {o.descripcion}" for o in obs]
    return '\n'.join(lineas)


def validar_informe(contenido_informe: str, reglamento: str, observaciones: str) -> list:
    """
    Valida un informe usando IA (GROQ API).
    Si la API no está disponible, usa validación local basada en heurísticas.
    """
    api_key = settings.GROQ_API_KEY
    
    # Si no hay API key o es el valor por defecto, usar validación local
    if not api_key or api_key in ['your_groq_api_key_here', '']:
        print("⚠️ GROQ_API_KEY no configurada. Usando validación local (modo demo).")
        return validar_informe_local(contenido_informe)
    
    try:
        return validar_con_groq(contenido_informe, reglamento, observaciones, api_key)
    except Exception as e:
        print(f"⚠️ Error con GROQ API: {e}. Usando validación local como fallback.")
        return validar_informe_local(contenido_informe)


def validar_con_groq(contenido_informe: str, reglamento: str, observaciones: str, api_key: str) -> list:
    """
    Validación usando API de IA (Groq o xAI Grok)
    Detecta automáticamente el tipo de API por el formato de la key
    """
    import time
    
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
    "ubicacion": "lugar donde se encuentra el error",
    "severidad": "critica|importante|menor|sugerencia"
  }}
]

Si el informe cumple con todo, devuelve una lista vacia: []"""

    # Detectar tipo de API por el formato de la key
    if api_key.startswith('xai-'):
        # xAI Grok API
        url = "https://api.x.ai/v1/chat/completions"
        model = "grok-beta"
        print(f"⏱️  [00s] 🤖 Usando xAI Grok API")
        print(f"⏱️  [00s] 📊 Prompt size: {len(prompt)} caracteres")
    else:
        # Groq API (default)
        url = "https://api.groq.com/openai/v1/chat/completions"
        model = "llama-3.3-70b-versatile"
        print(f"⏱️  [00s] 🤖 Usando Groq API (Llama 3.3)")
        print(f"⏱️  [00s] 📊 Prompt size: {len(prompt)} caracteres")

    start_time = time.time()
    print(f"⏱️  [00s] 🌐 Enviando request a {url}")
    
    try:
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            },
            timeout=90,  # 90 segundos de timeout
        )
        
        elapsed = time.time() - start_time
        print(f"⏱️  [{int(elapsed)}s] ✅ Response recibido (HTTP {response.status_code})")
        
        response.raise_for_status()
        
        response_json = response.json()
        print(f"⏱️  [{int(elapsed)}s] 📝 Parseando respuesta JSON")
        
        texto = response_json["choices"][0]["message"]["content"].strip()
        print(f"⏱️  [{int(elapsed)}s] 📏 Respuesta: {len(texto)} caracteres")
        
        # Limpiar markdown
        texto = re.sub(r'```(?:json)?\s*', '', texto).strip('`').strip()
        
        # Parsear JSON
        observaciones_list = json.loads(texto)
        print(f"⏱️  [{int(elapsed)}s] ✅ {len(observaciones_list)} observaciones generadas")
        
        return observaciones_list
        
    except requests.Timeout:
        elapsed = time.time() - start_time
        print(f"⏱️  [{int(elapsed)}s] ❌ TIMEOUT: La API tardó más de 90 segundos")
        raise ValueError("La API de IA tardó demasiado tiempo (>90s). Intenta de nuevo.")
    
    except requests.HTTPError as e:
        elapsed = time.time() - start_time
        print(f"⏱️  [{int(elapsed)}s] ❌ HTTP ERROR {response.status_code}: {response.text[:200]}")
        
        # Mensajes más claros según el error
        if response.status_code == 400:
            error_text = response.text
            if "Model not found" in error_text:
                raise ValueError(f"El modelo de IA no está disponible. Verifica tu configuración.")
            elif "credits" in error_text.lower() or "license" in error_text.lower():
                raise ValueError(f"Sin créditos en xAI. Activa créditos en https://console.x.ai o usa Groq API.")
        elif response.status_code == 401:
            raise ValueError(f"API Key inválida. Verifica tu .env")
        elif response.status_code == 429:
            raise ValueError(f"Límite de requests excedido. Espera un momento.")
        
        raise ValueError(f"Error de API (HTTP {response.status_code}): {response.text[:200]}")
    
    except json.JSONDecodeError as e:
        elapsed = time.time() - start_time
        print(f"⏱️  [{int(elapsed)}s] ❌ JSON ERROR: No se pudo parsear la respuesta")
        print(f"Respuesta recibida: {texto[:500]}")
        raise ValueError(f"La IA no devolvió JSON válido: {str(e)}")
    
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"⏱️  [{int(elapsed)}s] ❌ ERROR INESPERADO: {str(e)}")
        raise


def validar_informe_local(contenido: str) -> list:
    """
    Validación local sin IA (modo demo/fallback).
    Analiza el contenido aplicando reglas básicas para simular detección de la IA.
    Esto permite que el sistema funcione sin GROQ API Key configurada.
    """
    observaciones = []
    contenido_lower = contenido.lower()
    palabras = contenido.split()
    num_palabras = len(palabras)
    num_lineas = len(contenido.split('\n'))
    
    # Regla 1: Verificar carátula
    if 'untels' not in contenido_lower and 'universidad nacional tecnologica' not in contenido_lower:
        observaciones.append({
            "seccion": "Carátula",
            "observacion": "No se detecta mención a la UNTELS en el documento. Verificar que la carátula institucional esté completa.",
            "ubicacion": "Página 1 - Carátula",
            "severidad": "critica"
        })
    
    # Regla 2: Verificar índice
    if 'indice' not in contenido_lower and 'índice' not in contenido_lower and 'contenido' not in contenido_lower:
        observaciones.append({
            "seccion": "Índice",
            "observacion": "No se detecta un índice o tabla de contenidos en el documento.",
            "ubicacion": "Inicio del documento",
            "severidad": "importante"
        })
    
    # Regla 3: Verificar introducción
    if 'introduccion' not in contenido_lower and 'introducción' not in contenido_lower:
        observaciones.append({
            "seccion": "Introducción",
            "observacion": "No se detecta una sección de introducción claramente identificada.",
            "ubicacion": "Después del índice",
            "severidad": "importante"
        })
    
    # Regla 4: Verificar conclusiones
    if 'conclusion' not in contenido_lower and 'conclusión' not in contenido_lower:
        observaciones.append({
            "seccion": "Conclusiones",
            "observacion": "No se detecta una sección de conclusiones en el informe.",
            "ubicacion": "Final del documento",
            "severidad": "critica"
        })
    
    # Regla 5: Verificar longitud mínima
    if num_palabras < 500:
        observaciones.append({
            "seccion": "Contenido",
            "observacion": f"El informe es muy corto (solo {num_palabras} palabras). Se requiere un contenido más extenso y detallado.",
            "ubicacion": "Todo el documento",
            "severidad": "critica"
        })
    elif num_palabras < 1500:
        observaciones.append({
            "seccion": "Contenido",
            "observacion": f"El contenido es relativamente breve ({num_palabras} palabras). Se recomienda ampliar las descripciones de actividades.",
            "ubicacion": "Todo el documento",
            "severidad": "importante"
        })
    
    # Regla 6: Verificar mención a empresa/institución
    if 'empresa' not in contenido_lower and 'institucion' not in contenido_lower and 'institución' not in contenido_lower:
        observaciones.append({
            "seccion": "Descripción de Empresa",
            "observacion": "No se detecta una descripción clara de la empresa/institución donde se realizaron las prácticas.",
            "ubicacion": "Sección inicial del informe",
            "severidad": "importante"
        })
    
    # Regla 7: Verificar actividades realizadas
    if 'actividad' not in contenido_lower and 'tarea' not in contenido_lower and 'funcion' not in contenido_lower and 'función' not in contenido_lower:
        observaciones.append({
            "seccion": "Actividades Realizadas",
            "observacion": "No se detecta una sección clara de actividades, tareas o funciones realizadas durante las prácticas.",
            "ubicacion": "Cuerpo principal del informe",
            "severidad": "critica"
        })
    
    # Regla 8: Verificar referencias bibliográficas
    if 'referencia' not in contenido_lower and 'bibliograf' not in contenido_lower:
        observaciones.append({
            "seccion": "Referencias",
            "observacion": "No se detectan referencias bibliográficas. Se recomienda incluir fuentes consultadas en formato APA.",
            "ubicacion": "Final del documento",
            "severidad": "menor"
        })
    
    # Regla 9: Verificar anexos
    if 'anexo' not in contenido_lower:
        observaciones.append({
            "seccion": "Anexos",
            "observacion": "No se detecta una sección de anexos. Considere agregar evidencias fotográficas y documentos de soporte.",
            "ubicacion": "Final del documento",
            "severidad": "menor"
        })
    
    # Regla 10: Verificar objetivos
    if 'objetivo' not in contenido_lower and 'meta' not in contenido_lower:
        observaciones.append({
            "seccion": "Objetivos",
            "observacion": "No se detectan objetivos claramente planteados en la introducción.",
            "ubicacion": "Sección de introducción",
            "severidad": "importante"
        })
    
    return observaciones
