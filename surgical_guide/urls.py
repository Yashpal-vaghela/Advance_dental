from django.urls import path
from . import views

urlpatterns = [
    path('', views.surgical_guide, name='surgical_guide'),
]