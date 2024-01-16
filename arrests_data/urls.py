from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('stats/', views.arrest_records_by_date, name='stats'),
    path('arrests/', views.run_script, name='run_script'),
    path('search', views.search_script, name='search_script'),
]
