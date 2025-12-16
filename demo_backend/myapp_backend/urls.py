"""
URL configuration for myapp_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from graphene.validation import DisableIntrospection, depth_limit_validator
from graphene_django.views import GraphQLView


from dotenv import dotenv_values
config = dotenv_values(".env")


class View(GraphQLView):
    validation_rules = [depth_limit_validator(max_depth = 10)]
    if not settings.DEBUG:
        validation_rules.append(DisableIntrospection)
        
    graphiql = settings.DEBUG

urlpatterns = [
     path("__debug__/", include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
       path(
        "graphql",
        csrf_exempt(GraphQLView.as_view(graphiql=True))  
    ),
    path("auth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
