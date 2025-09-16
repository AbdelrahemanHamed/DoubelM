from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta

from .models import CourseCode
from courses.models import Session


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def activate_code(request):
    code_value = request.data.get("code")
    if not code_value:
        return Response({"error": "الكود مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        code = CourseCode.objects.get(code=code_value)
    except CourseCode.DoesNotExist:
        return Response({"error": "الكود غير صحيح"}, status=status.HTTP_404_NOT_FOUND)

    # Check if student already has an active code for this course that is still valid
    existing_codes = CourseCode.objects.filter(
        course=code.course,
        assigned_to=request.user,
        used=True
    )
    for c in existing_codes:
        if c.is_valid():
            return Response({
                "message": "الكورس مفعل بالفعل ولديك كود صالح له",
                "course": code.course.title,
                "expires_at": c.activated_at + timedelta(days=c.valid_days)
            }, status=status.HTTP_200_OK)

    # Activate the code if it’s unused
    if code.used:
        return Response({"error": "الكود مستخدم بالفعل"}, status=status.HTTP_400_BAD_REQUEST)

    if code.activate(request.user):
        return Response({
            "message": "تم تفعيل الكود بنجاح",
            "course": code.course.title,
            "expires_at": code.activated_at + timedelta(days=code.valid_days),
            "image": request.build_absolute_uri(code.course.image.url) if code.course.image else None
        }, status=status.HTTP_200_OK)

    return Response({"error": "فشل التفعيل"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_courses(request):
    codes = CourseCode.objects.filter(assigned_to=request.user, used=True)
    data = []
    for c in codes:
        data.append({
            "id": c.course.id,
            "course": c.course.title,
            "teacher": c.course.teacher.name if c.course.teacher else None,
            "image": request.build_absolute_uri(c.course.image.url) if c.course.image else None,
            "activated_at": c.activated_at,
            "expires_at": c.activated_at + timedelta(days=c.valid_days) if c.activated_at else None,
            "is_valid": c.is_valid(),
        })
    return Response(data, status=status.HTTP_200_OK)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CourseCode
from courses.models import Course

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def course_details(request, course_id):
    # Get all codes for this course and this student
    codes = CourseCode.objects.filter(course_id=course_id, assigned_to=request.user, used=True)
    
    # Filter only valid codes
    valid_codes = [c for c in codes if c.is_valid()]
    
    if not valid_codes:
        return Response({"error": "الكورس غير مفعل لديك"}, status=400)
    
    # Get the course
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "الكورس غير موجود"}, status=404)

    # Get sessions
    sessions = course.sessions.all().values("id", "title", "link", "created_at")

    return Response({
        "course": {
            "id": course.id,
            "title": course.title,
            "teacher": course.teacher.name if course.teacher else None,
            "image": request.build_absolute_uri(course.image.url) if course.image else None,
            "sessions": list(sessions)
        }
    })
