from django.urls import path, include
from . import views

urlpatterns = [
    # Public Website URLs
    path('', views.index, name='index'),

]
