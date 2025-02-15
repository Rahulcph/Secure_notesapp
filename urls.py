from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_note, name='add_note'),
    path('encrypt/<int:note_id>/', views.encrypt_note, name='encrypt_note'),
    path('decrypt/<int:note_id>/', views.decrypt_note, name='decrypt_note'),
]
