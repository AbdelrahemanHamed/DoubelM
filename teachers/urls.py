from django.urls import path
from .views import get_all_teachers, add_teacher

urlpatterns = [
    path('teachers/', get_all_teachers, name='get_all_teachers'),
    path('add-teacher/', add_teacher, name='add_teacher'),
]
