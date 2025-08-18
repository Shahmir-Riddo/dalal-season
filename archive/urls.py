from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dalal/<id>', views.dalal_detail, name='dalal_detail'),
    path('dalal-ranking', views.dalal_ranking, name='dalal_ranking'),
    path('dalal_shoe_count', views.dalal_shoe_count, name='dalal_shoe_count'),
]
