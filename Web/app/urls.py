from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('api/predict-price/', views.predict_price, name='predict_price')
]