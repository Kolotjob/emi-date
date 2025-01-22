from django.urls import path
from . import views

urlpatterns = [
    path('cards/', views.get_user_cards, name='user_cards'),
]