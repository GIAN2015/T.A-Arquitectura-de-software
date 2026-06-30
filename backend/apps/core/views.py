"""Compatibilidad: las vistas reales viven en apps.presentacion.web."""

from apps.presentacion.web.auth_views import login_docente_view, login_view, logout_view, registro_view
from apps.presentacion.web.docente_views import panel_docente_view
from apps.presentacion.web.estudiante_views import historial_view, resultado_view, upload_view

__all__ = [
    'historial_view',
    'login_docente_view',
    'login_view',
    'logout_view',
    'panel_docente_view',
    'registro_view',
    'resultado_view',
    'upload_view',
]
