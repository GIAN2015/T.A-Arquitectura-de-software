from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('upload/', views.upload_view, name='upload'),
    path('resultado/<int:informe_id>/', views.resultado_view, name='resultado'),
]
