from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import CourseCode


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

    # لو الكود متفعل قبل كده
    if code.used:
        if code.assigned_to == request.user and code.is_valid():
            return Response({"message": "الكود متفعل عندك بالفعل", "course": code.course.title})
        return Response({"error": "الكود مستخدم بالفعل"}, status=status.HTTP_400_BAD_REQUEST)

    # فعل الكود
    if code.activate(request.user):
        return Response({
            "message": "تم تفعيل الكود بنجاح",
            "course": code.course.title,
            "expires_at": code.activated_at + timedelta(days=code.valid_days),
        }, status=status.HTTP_200_OK)

    return Response({"error": "فشل التفعيل"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_courses(request):
    codes = CourseCode.objects.filter(assigned_to=request.user, used=True)

    data = []
    for c in codes:
        data.append({
            "course": c.course.title,
            "activated_at": c.activated_at,
            "expires_at": c.activated_at + timedelta(days=c.valid_days) if c.activated_at else None,
            "is_valid": c.is_valid(),
        })

    return Response(data, status=status.HTTP_200_OK)
