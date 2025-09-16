from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Quiz
from .serializers import QuizSerializer

class QuizListAPIView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        return Quiz.objects.filter(course_id=course_id)
