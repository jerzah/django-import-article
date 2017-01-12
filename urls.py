from django.conf.urls import include, url
from django.contrib import admin


from . import views

app_name = 'myComments'
urlpatterns = [
    url(r'^$', views.index, name='index')
]
