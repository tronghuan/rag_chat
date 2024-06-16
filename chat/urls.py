from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('show', views.show, name='show'),
    path('check', views.check, name='check'),
    path('aws_embedding', views.aws_embedding, name='aws_embedding'),
]