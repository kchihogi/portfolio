"""The setting of URLs.
"""
from django.urls import path

from . import views

app_name = 'portfolio'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('works/', views.WorksView.as_view(), name='works'),
    path('work/<int:primary_key>/', views.WorkView.as_view(), name='work'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.success, name='success'),
]
