from django.urls import path
from . import views

urlpatterns = [
    path('explain/', views.explain_like_five, name='explain_like_five'),
]