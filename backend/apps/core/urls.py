"""
URLs del sistema
Versión 2.0 - Flujo completo multi-rol
"""
from django.urls import path
from . import views
from . import admin_views
from apps.presentacion.web import auth_views, secretaria_views, presidente_views, docente_views

urlpatterns = [
    # ==================== AUTENTICACIÓN ====================
    
    # Estudiantes/Egresados
    path('', auth_views.login_view, name='login'),
    path('registro/', auth_views.registro_view, name='registro'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Docentes
    path('docente/login/', auth_views.login_docente_view, name='login_docente'),
    
    # Secretaria (NUEVO v2.0)
    path('secretaria/login/', auth_views.login_secretaria_view, name='login_secretaria'),
    
    # Presidente (NUEVO v2.0)
    path('presidente/login/', auth_views.login_presidente_view, name='login_presidente'),
    
    
    # ==================== ESTUDIANTES/EGRESADOS ====================
    
    path('upload/', views.upload_view, name='upload'),
    path('resultado/<int:informe_id>/', views.resultado_view, name='resultado'),
    path('historial/', views.historial_view, name='historial'),
    
    
    # ==================== SECRETARIA (NUEVO v2.0) ====================
    
    path('secretaria/dashboard/', secretaria_views.secretaria_dashboard, name='secretaria_dashboard'),
    path('secretaria/derivar/<int:informe_id>/', secretaria_views.secretaria_derivar, name='secretaria_derivar'),
    path('secretaria/notificar/<int:informe_id>/', secretaria_views.secretaria_notificar_estudiante, name='secretaria_notificar'),
    path('secretaria/ver/<int:informe_id>/', secretaria_views.secretaria_ver_informe, name='secretaria_ver_informe'),
    path('secretaria/notificaciones/', secretaria_views.secretaria_notificaciones, name='secretaria_notificaciones'),
    
    
    # ==================== PRESIDENTE (NUEVO v2.0) ====================
    
    path('presidente/dashboard/', presidente_views.presidente_dashboard, name='presidente_dashboard'),
    path('presidente/designar/<int:informe_id>/', presidente_views.presidente_designar_docente, name='presidente_designar'),
    path('presidente/revisar/<int:informe_id>/', presidente_views.presidente_revisar_dictamen, name='presidente_revisar'),
    path('presidente/ver/<int:informe_id>/', presidente_views.presidente_ver_informe, name='presidente_ver_informe'),
    path('presidente/historial/', presidente_views.presidente_historial, name='presidente_historial'),
    path('presidente/notificaciones/', presidente_views.presidente_notificaciones, name='presidente_notificaciones'),
    
    
    # ==================== DOCENTE (ACTUALIZADO v2.0) ====================
    
    path('panel-docente/', docente_views.panel_docente_view, name='panel_docente'),
    path('docente/banco/', docente_views.docente_banco_observaciones, name='docente_banco_observaciones'),
    path('docente/revisar/<int:informe_id>/', docente_views.docente_revisar_informe, name='docente_revisar_informe'),
    path('docente/ver/<int:informe_id>/', docente_views.docente_ver_informe, name='docente_ver_informe'),
    path('docente/historial/', docente_views.docente_historial, name='docente_historial'),
    path('docente/notificaciones/', docente_views.docente_notificaciones, name='docente_notificaciones'),
    
    
    # ==================== ADMIN (Sistema - Mantener para compatibilidad) ====================
    
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/usuarios/', admin_views.admin_usuarios, name='admin_usuarios'),
    path('admin/usuarios/<int:usuario_id>/', admin_views.admin_usuario_detalle, name='admin_usuario_detalle'),
    path('admin/reglamento/', admin_views.admin_reglamento, name='admin_reglamento'),
    path('admin/observaciones/', admin_views.admin_observaciones, name='admin_observaciones'),
    path('admin/observaciones/eliminar/<int:obs_id>/', admin_views.admin_observacion_eliminar, name='admin_observacion_eliminar'),
    path('admin/reportes/', admin_views.admin_reportes, name='admin_reportes'),
    path('admin/revisar/<int:informe_id>/', admin_views.admin_revisar_informe, name='admin_revisar_informe'),
]
