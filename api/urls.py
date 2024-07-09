from django.urls import path
from .views import swap_faces

urlpatterns = [
    path('swap_face/', swap_faces, name='swap_face'),
]
