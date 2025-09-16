# codes/utils.py
import random
import string
from .models import CourseCode  # استدعاء الموديل

def generate_code(length=12):
    """Generate a random alphanumeric code."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

def check_course_access(user, course):
    """
    Check if a user has a valid code for the given course.
    """
    codes = CourseCode.objects.filter(assigned_to=user, course=course, used=True)
    for code in codes:
        if code.is_valid():  # الـ method دي موجودة جوه الموديل CourseCode
            return True
    return False
