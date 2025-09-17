# quizzes/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Quiz, QuizAttempt, UserAnswer, Answer
from .serializers import QuizSerializer, QuizAttemptSerializer, SubmitAnswerSerializer
from codes.models import CourseCode


# 🔹 List only quizzes for courses the student has access to
class QuizListAPIView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get all valid codes for this student
        valid_codes = CourseCode.objects.filter(
            assigned_to=user,
            used=True,
        )

        # Filter only valid ones
        valid_courses = [c.course for c in valid_codes if c.is_valid()]
        return Quiz.objects.filter(course__in=valid_courses)


# 🔹 Start quiz attempt
class StartQuizAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=kwargs['quiz_id'])
        user = request.user

        # Check course access
        has_access = CourseCode.objects.filter(
            course=quiz.course, assigned_to=user, used=True
        )
        has_access = [c for c in has_access if c.is_valid()]
        if not has_access:
            return Response({"detail": "You are not enrolled in this course."}, status=403)

        attempt, created = QuizAttempt.objects.get_or_create(
            user=user, quiz=quiz, completed=False
        )
        return Response(QuizAttemptSerializer(attempt).data, status=200)


# 🔹 Submit answers
class SubmitQuizAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=kwargs['quiz_id'])
        user = request.user
        attempt = get_object_or_404(QuizAttempt, user=user, quiz=quiz, completed=False)

        serializer = SubmitAnswerSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        score = 0
        total = quiz.questions.count()

        for ans in serializer.validated_data:
            question_id = ans['question_id']
            selected_answer_id = ans['selected_answer_id']
            answer = get_object_or_404(Answer, id=selected_answer_id, question_id=question_id)

            UserAnswer.objects.create(
                attempt=attempt,
                question_id=question_id,
                selected_answer=answer,
            )

            if answer.is_correct:
                score += 1

        attempt.score = score
        attempt.total = total
        attempt.completed = True
        attempt.save()

        return Response({
            "quiz": quiz.title,
            "score": score,
            "total": total,
            "result": f"{score}/{total}"
        })


# 🔹 View my past results
class MyQuizResultsAPIView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user, completed=True).order_by('-created_at')
