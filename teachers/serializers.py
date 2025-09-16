from rest_framework import serializers
from .models import Teacher
from courses.models import Course

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'image', 'description']


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)  # Embed teacher info

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'image', 'teacher']
