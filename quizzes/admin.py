import nested_admin
from django.contrib import admin
from .models import Quiz, Question, Answer

class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 4
    fields = ('text', 'is_correct')


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]


@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'course', 'time_limit')
    inlines = [QuestionInline]
