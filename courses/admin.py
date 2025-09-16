from django.contrib import admin
from .models import Course, Session

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at')
    inlines = [SessionInline]

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'link', 'created_at')
