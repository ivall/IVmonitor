from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.PanelView.as_view()),
    path('monitor/add/', views.AddMonitor.as_view()),
    path('monitor/delete/', views.DeleteMonitor.as_view())
]