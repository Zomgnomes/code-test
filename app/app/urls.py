"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from api import views
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("keys/", views.key_list, name="key_list"),
    path("keys/<str:name>", views.key_specific, name="key_specific"),
    path("dogs/load", views.dog_load, name="dog_load"),
    path("dogs/", views.dog_output, name="dog_output"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
