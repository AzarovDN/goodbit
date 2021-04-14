from django.urls import path

from . import views

app_name = 'promocode'
urlpatterns = [
    path('', views.GeneratorCodeView.as_view(), name='index'),
]