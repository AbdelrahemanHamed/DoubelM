from django.contrib import admin
from .models import Student
from codes.models import CourseCode

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'phone_number', 'city', 'major', 'active_codes')
    search_fields = ('fullname', 'email', 'phone_number')
    list_filter = ('city', 'major', 'is_active', 'is_staff')

    def active_codes(self, obj):
        codes = CourseCode.objects.filter(assigned_to=obj, used=True)
        active_codes_list = [c.code for c in codes if c.is_valid()]
        return ", ".join(active_codes_list) if active_codes_list else "-"
    active_codes.short_description = "Active Course Codes"
