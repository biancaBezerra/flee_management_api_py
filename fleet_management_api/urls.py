"""
URL configuration for fleet_management_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path

from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema_view = swagger_get_schema_view(
  openapi.Info(
    title="Fleet Management API",
    default_version='1.0.0',
    description='API PARA CONSULTAR LOCALIZAÇÃO DE VEÍCULOS DE UMA EMPRESA DE TAXI',
    # term_of_service= "https://www.google.com/policies/terms/" , 
    # contact=openapi.Contact(email= "contact@fleetmanagement.com" ), 
    # licence=openapi.License(name= "BSD Licença" ),
  ),
  public=True,
  permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include('fleet_management_app.urls'), name='fleet_management_app.urls'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_schema'),
]
