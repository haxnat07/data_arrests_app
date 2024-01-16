from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('arrests/', views.run_script, name='run_script'),
    path('search', views.search_script, name='search_script'),
]
