"""
URL configuration for proyectoDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from core.views import *
from users.views import *
from common.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),

    # Urls de comunidades
    path('comunidades/', ComunidadListView.as_view(), name='comunidad_list'),
    path('comunidades/<int:pk>/', ComunidadDetailView.as_view(), name='comunidad_detail'),
    path('comunidades/crear/', ComunidadCreateView.as_view(), name='comunidad_create'),
    path('comunidades/<int:pk>/editar/', ComunidadUpdateView.as_view(), name='comunidad_update'),
    path('comunidades/<int:pk>/eliminar/', ComunidadDeleteView.as_view(), name='comunidad_delete'),

    # Urls de inmuebles
    path('inmuebles/', InmuebleListView.as_view(), name='inmueble_list'),
    path('inmuebles/<int:pk>/', InmuebleDetailView.as_view(), name='inmueble_detail'),
    path('inmuebles/crear/', InmuebleCreateView.as_view(), name='inmueble_create'),
    path('inmuebles/<int:pk>/editar/', InmuebleUpdateView.as_view(), name='inmueble_update'),
    path('inmuebles/<int:pk>/eliminar/', InmuebleDeleteView.as_view(), name='inmueble_delete'),

    # Urls de Usuarios
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/<int:pk>/', UsuarioDetailView.as_view(), name='usuario_detail'),
    path('usuarios/nuevo/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='usuario_delete'),

    # Urls de autenticación
    path('login/', login_basico, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', UsuarioRegistrationView.as_view(), name='register'),
  
]
