from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    # Autenticación - Estudiantes
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    
    # Autenticación - Docentes
    path('docente/login/', views.login_docente_view, name='login_docente'),
    
    # Usuario normal (Estudiantes/Egresados)
    path('upload/', views.upload_view, name='upload'),
    path('resultado/<int:informe_id>/', views.resultado_view, name='resultado'),
    path('historial/', views.historial_view, name='historial'),
    
    # Panel Docente (ver informes de estudiantes)
    path('panel-docente/', views.panel_docente_view, name='panel_docente'),
    
    # Panel de Administración (gestionar sistema)
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/usuarios/', admin_views.admin_usuarios, name='admin_usuarios'),
    path('admin/usuarios/<int:usuario_id>/', admin_views.admin_usuario_detalle, name='admin_usuario_detalle'),
    path('admin/reglamento/', admin_views.admin_reglamento, name='admin_reglamento'),
    path('admin/observaciones/', admin_views.admin_observaciones, name='admin_observaciones'),
    path('admin/observaciones/eliminar/<int:obs_id>/', admin_views.admin_observacion_eliminar, name='admin_observacion_eliminar'),
    path('admin/reportes/', admin_views.admin_reportes, name='admin_reportes'),
    
    # Revisión Docente de Informes (NUEVO - Flujo Principal)
    path('docente/revisar/<int:informe_id>/', admin_views.admin_revisar_informe, name='docente_revisar_informe'),
]
