"""
URL configuration for spectate project.

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
from rest_framework.routers import DefaultRouter
from django.urls import path, re_path, include
from .views import event_view, selection_view, sport_view
# from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="888Spectate",
        default_version='v1',
        description="Description",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [

    path('sports/', sport_view.SportsView.as_view(), name='sports-list'),
    path('sports/<int:id>/', sport_view.SportsView.UsingIdPath.as_view(),
         name='sports-detail'),

    path('events/', event_view.EventView.as_view(),
         name='events-list'),
    path('events/<int:id>/', event_view.EventView.UsingIdPath.as_view(),
         name='events-detail'),

    path('selection/', selection_view.SelectionView.as_view(),
         name='selections-list'),
    path('selection/<int:id>/', selection_view.SelectionView.UsingIdPath.as_view(),
         name='selections-detail'),


    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),


]
