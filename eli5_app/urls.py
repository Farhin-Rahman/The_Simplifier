from django.urls import path
from .views import explain_like_five

urlpatterns = [
    path('explain/', explain_like_five, name='explain_like_five'),
]
