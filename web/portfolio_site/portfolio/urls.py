"""The setting of URLs.
"""
from django.urls import path

from . import views

app_name = 'portfolio'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('works/', views.WorksView.as_view(), name='works'),
    path('work/<int:pk>/', views.WorkView.as_view(), name='work'),
]
