from django.urls import path
from .views import activate_code, my_courses, course_details

urlpatterns = [
    # Activate a course code
    path("activate/", activate_code, name="activate_code"),

    # List all courses activated by the logged-in user
    path("my-courses/", my_courses, name="my_courses"),

    # Get course details with sessions by course ID (only if the code is activated by user)
    path("courses/<int:course_id>/details/", course_details, name="course-details"),
]
