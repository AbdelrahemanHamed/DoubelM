from django.urls import path
from .views import activate_code, my_courses

urlpatterns = [
    path("activate/", activate_code, name="activate_code"),
    path("my-courses/", my_courses, name="my_courses"),
]
