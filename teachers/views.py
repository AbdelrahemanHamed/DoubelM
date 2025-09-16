from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Teacher
from .serializers import TeacherSerializer

# -----------------------------
# Public: Get all teachers
# -----------------------------
@api_view(['GET'])
def get_all_teachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True, context={'request': request})
    return Response(serializer.data)

# -----------------------------
# Admin-only: Add teacher
# -----------------------------
@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_teacher(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Teacher added successfully", "teacher": serializer.data})
    return Response(serializer.errors, status=400)
