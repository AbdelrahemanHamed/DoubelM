from django.contrib import admin
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
import openpyxl
from .models import CourseCode
from courses.models import Course
from .utils import generate_code

# Form to input number of codes
class GenerateCodesForm(forms.Form):
    count = forms.IntegerField(min_value=1, label="Number of codes to generate")


class CourseCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'course', 'used', 'assigned_to', 'activated_at')

    # Custom URL for generating Excel
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('generate-excel/', self.admin_site.admin_view(self.generate_excel_view), name='generate_excel'),
        ]
        return custom_urls + urls

    # View for Excel generation
    def generate_excel_view(self, request):
        if request.method == "POST":
            form = GenerateCodesForm(request.POST)
            if form.is_valid():
                count = form.cleaned_data['count']
                course_id = int(request.POST.get("course_id"))
                course = Course.objects.get(id=course_id)

                wb = openpyxl.Workbook()
                ws = wb.active
                ws.append(['Code', 'Course'])

                for _ in range(count):
                    code = generate_code()
                    CourseCode.objects.create(code=code, course=course)
                    ws.append([code, course.title])

                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename=codes.xlsx'
                wb.save(response)
                return response
        else:
            form = GenerateCodesForm()

        courses = Course.objects.all()
        return render(request, "admin/codes/generate_excel.html", {"form": form, "courses": courses})


# Register safely to avoid AlreadyRegistered error
try:
    admin.site.register(CourseCode, CourseCodeAdmin)
except admin.sites.AlreadyRegistered:
    pass
