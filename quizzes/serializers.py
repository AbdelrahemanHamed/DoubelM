# quizzes/serializers.py
from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizAttempt, UserAnswer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'answers']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'time_limit', 'questions']


# 🔹 Lightweight version for listing attempts or starting a quiz
class QuizBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'time_limit']


class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz = QuizBasicSerializer(read_only=True)  # ✅ prevents write errors

    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'score', 'total', 'completed', 'created_at']


class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_answer_id = serializers.IntegerField()
