from django.urls import path

from . import views

urlpatterns = [
    path('', views.PanelView.as_view()),
    path('monitor/add/', views.AddMonitor.as_view()),
    path('monitor/delete/', views.DeleteMonitor.as_view()),
    path('alert/add/', views.AddAlert.as_view()),
    path('alert/delete/', views.DeleteAlert.as_view())
]



import threading
from .checker import get_sites
t1 = threading.Thread(target=get_sites)
t1.start()
