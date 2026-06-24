from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('docente/login/', views.login_docente_view, name='login_docente'),
    path('upload/', views.upload_view, name='upload'),
    path('resultado/<int:informe_id>/', views.resultado_view, name='resultado'),
    path('historial/', views.historial_view, name='historial'),
    path('exportar/<int:informe_id>/', views.exportar_excel, name='exportar_excel'),
    path('panel-docente/', views.panel_docente_view, name='panel_docente'),
    path('docente/revisar/<int:informe_id>/', views.revisar_informe_view, name='revisar_informe'),
]
