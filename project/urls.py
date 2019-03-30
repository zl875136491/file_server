"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from users import views as usersviews
from filesystem import views as fileviews
urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', usersviews.login),
    url(r'^index', usersviews.index),
    url(r'^teacherindex', usersviews.teacherindex),
    url(r'^login/', usersviews.login),
    url(r'^register/', usersviews.register),
    url(r'^logout/', usersviews.logout),
    url(r'^captcha', include('captcha.urls')),
    url(r'^file/', fileviews.upload),
    url(r'^uploadok/', fileviews.uploadok),
    url(r'^filemanage', fileviews.filemanage),
    url(r'^noteediter', fileviews.noteediter),
    url(r'^notereciver', fileviews.notereciver),
    url(r'^404/', usersviews.page404),
]
