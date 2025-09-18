# quizzes/urls.py
from django.urls import path
from .views import QuizListAPIView, StartQuizAPIView, SubmitQuizAPIView, MyQuizResultsAPIView

urlpatterns = [
    path('quizzes/', QuizListAPIView.as_view(), name='quiz-list'),
    path('quizzes/<int:quiz_id>/start/', StartQuizAPIView.as_view(), name='quiz-start'),
    path('quizzes/<int:quiz_id>/submit/', SubmitQuizAPIView.as_view(), name='quiz-submit'),
    path('quizzes/my-results/', MyQuizResultsAPIView.as_view(), name='quiz-results'),
]
