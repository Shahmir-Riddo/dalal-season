from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.ds_login, name='ds_login'),
    path('dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('add_dalal', views.add_dalal, name='add_dalal'),
    path('dalal_list', views.dalal_list, name='dalal_list'),
    path('edit_dalal/<id>', views.edit_dalal, name='edit_dalal'),
    path('delete_dalal', views.delete_dalal, name='delete_dalal'),
    path('logout', views.logout_view, name='logout_view')

]
