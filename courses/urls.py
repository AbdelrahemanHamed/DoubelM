from django.urls import path
from .views import all_courses, course_detail

urlpatterns = [
    path('', all_courses, name='all_courses'),
    path('<int:pk>/', course_detail, name='course_detail'),
]
