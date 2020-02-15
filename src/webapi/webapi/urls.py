"""webapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path
from convert import views


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^convert/amount=(?P<amount>([0-9]*\.[0-9]+|[0-9]+))/src_currency=(?P<src_currency>[A-Z]{3})/dest_currency=(?P<dest_currency>[A-Z]{3})/reference_date=(?P<reference_date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})$', views.convert, name="convert")
]
