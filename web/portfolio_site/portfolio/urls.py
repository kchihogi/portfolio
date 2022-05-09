from django.urls import path

from . import views

app_name = 'portfolio'
urlpatterns = [
    path('', views.IndexView.index, name='index'),
    path('work/<int:pk>/', views.WorkView.get_work, name='work'),
]