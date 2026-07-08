"""
Filtros de template personalizados para formatear dictámenes
"""
from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter(name='formatear_dictamen')
def formatear_dictamen(texto):
    """
    Convierte el dictamen en texto plano a HTML formateado
    
    Usage:
        {{ informe.comentario_docente|formatear_dictamen }}
    """
    if not texto:
        return '<p class="text-muted fst-italic">Sin dictamen</p>'
    
    # Escapar HTML básico primero
    html_parts = []
    
    # Procesar línea por línea
    lines = texto.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detectar separadores grandes (====)
        if line.startswith('===='):
            i += 1
            continue
        
        # Detectar separadores medianos (----)
        if line.startswith('----'):
            html_parts.append('<hr class="my-3">')
            i += 1
            continue
        
        # Detectar encabezados principales (ALL CAPS)
        if line and line.isupper() and len(line) < 50:
            # Es un encabezado
            color_class = ''
            icon = ''
            
            if 'DICTAMEN' in line:
                color_class = 'text-primary'
                icon = '📋'
            elif 'RECOMENDACIÓN' in line:
                color_class = 'text-warning'
                icon = '⚖️'
            elif 'OBSERVACIONES' in line:
                color_class = 'text-info'
                icon = '📊'
            elif 'FIN' in line:
                color_class = 'text-muted'
                icon = '✓'
            else:
                color_class = 'text-dark'
            
            html_parts.append(f'<h5 class="mt-4 mb-3 fw-bold {color_class}">{icon} {line}</h5>')
            i += 1
            continue
        
        # Detectar subtítulos con emoji (🔴, 🟠, 🟡, 💡)
        if line and any(emoji in line for emoji in ['🔴', '🟠', '🟡', '💡']):
            badge_class = 'danger' if '🔴' in line else 'warning' if '🟠' in line else 'info' if '🟡' in line else 'secondary'
            html_parts.append(f'<div class="alert alert-{badge_class} py-2 px-3 mb-2"><strong>{line}</strong></div>')
            i += 1
            continue
        
        # Detectar checkmarks (✅, ❌)
        if line and ('✅' in line or '❌' in line):
            badge_class = 'success' if '✅' in line else 'danger'
            html_parts.append(f'<div class="alert alert-{badge_class} py-2 px-3"><strong>{line}</strong></div>')
            i += 1
            continue
        
        # Detectar listas numeradas (1., 2., etc)
        if re.match(r'^\d+\.\s+\[', line):
            # Es un ítem de observación
            html_parts.append(f'<div class="card mb-3 border-start border-3 border-primary"><div class="card-body py-2">')
            html_parts.append(f'<h6 class="mb-2 text-primary">{line}</h6>')
            
            # Leer las siguientes líneas con indentación
            i += 1
            while i < len(lines) and lines[i].startswith('   '):
                detail_line = lines[i].strip()
                if detail_line.startswith('Observación:'):
                    html_parts.append(f'<p class="mb-1"><small><strong>Observación:</strong> {detail_line[12:].strip()}</small></p>')
                elif detail_line.startswith('Ubicación:'):
                    html_parts.append(f'<p class="mb-1 text-muted"><small><i class="bi bi-geo-alt-fill me-1"></i>{detail_line[10:].strip()}</small></p>')
                elif detail_line.startswith('Comentario del docente:'):
                    html_parts.append(f'<p class="mb-0 text-info"><small><i class="bi bi-chat-fill me-1"></i>{detail_line[23:].strip()}</small></p>')
                elif detail_line.startswith('Sugerencia:'):
                    html_parts.append(f'<p class="mb-1"><small><strong>Sugerencia:</strong> {detail_line[11:].strip()}</small></p>')
                else:
                    html_parts.append(f'<p class="mb-1"><small>{detail_line}</small></p>')
                i += 1
            
            html_parts.append('</div></div>')
            continue
        
        # Detectar listas con bullet (•)
        if line.startswith('•'):
            html_parts.append(f'<li class="ms-3">{line[1:].strip()}</li>')
            i += 1
            continue
        
        # Detectar texto normal con "Total de observaciones"
        if line.startswith('Total de observaciones'):
            html_parts.append(f'<div class="alert alert-light border py-2 px-3 mb-3"><strong>{line}</strong></div>')
            i += 1
            continue
        
        # Texto normal (párrafos)
        if line:
            html_parts.append(f'<p class="mb-2">{line}</p>')
        
        i += 1
    
    html = ''.join(html_parts)
    return mark_safe(html)
