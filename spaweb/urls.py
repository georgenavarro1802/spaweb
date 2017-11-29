"""rodgal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from web import (views, models)

from spaweb.settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT

urlpatterns = [

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Home
    url(r'^$', views.home, name='home'),

    # Services
    url(r'^servicios', views.servicios, name='servicios'),

    # Products
    url(r'^productos', views.productos, name='productos'),

    # Check Session
    url(r'^checksession$', views.checksession, name='checksession'),

    # Contacto
    url(r'^contactos$', views.contactos, name='contactos'),

    # Suscripciones
    url(r'^suscripciones$', views.suscripciones, name='suscripciones'),

    # Unete a nosotros
    url(r'^unete$', views.unete, name='unete'),

    # Registro o Logins
    url(r'^register$', views.register, name='register'),

    # Lost Password
    url(r'^lost_password$', views.lost_password, name='lost_password'),

    # Reservas
    url(r'^reservas$', views.reservas, name='reservas'),

    # Login
    url(r'^login$', views.entrar, name='entrar'),

    # Logout
    url(r'^salir$', views.salir, name='salir'),

]

# Static
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)

# Media
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)