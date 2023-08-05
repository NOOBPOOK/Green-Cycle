from django.contrib import admin
from django.urls import path
from website import views

urlpatterns = [
    path('', views.home, name="home"),
    path('paper', views.paper, name="paper"),
    path('colthes', views.clothes, name="clothes"),
    path('plastic', views.plastic, name="plastic"),
    path('ewaste', views.ewaste, name="ewaste"),
    path('glass', views.glass, name="glass"),
    path('metal', views.metal, name="metal"),
]