from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer, CourseDetailSerializer

@api_view(['GET'])
def all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True, context={"request": request})
    return Response(serializer.data)

@api_view(['GET'])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = CourseDetailSerializer(course, context={"request": request})
    return Response(serializer.data)
