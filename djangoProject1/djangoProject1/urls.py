"""djangoProject1 URL Configuration

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
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, re_path

import Top250.views
import Top250.CBRecommend

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Top250.views.Login),
    path('register/', Top250.views.Register),
    path('index/', Top250.views.movies),
    re_path(r'detail/(?P<id>[0-9]+)/$', Top250.views.detail),
    re_path(r'type/(?P<id>[0-9]+)/$', Top250.views.type),
]
