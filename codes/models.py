from django.db import models
from django.utils import timezone
from datetime import timedelta

class CourseCode(models.Model):
    code = models.CharField(max_length=12, unique=True)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="codes")
    assigned_to = models.ForeignKey("accounts.Student", null=True, blank=True, on_delete=models.SET_NULL)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    valid_days = models.PositiveIntegerField(default=30)

    def activate(self, student):
        """
        Activate the code for a student
        """
        if self.used:
            return False
        self.assigned_to = student
        self.used = True
        self.activated_at = timezone.now()
        self.save()
        return True

    def is_valid(self):
        """
        Check if the code is activated and still valid
        """
        if self.used and self.activated_at:
            expiration = self.activated_at + timedelta(days=self.valid_days)
            return timezone.now() <= expiration
        return False

    def course_data(self, request=None):
        """
        Return course info including teacher name and image URL
        """
        return {
            "id": self.course.id,
            "title": self.course.title,
            "teacher": self.course.teacher.name if self.course.teacher else None,
            "image": request.build_absolute_uri(self.course.image.url) if self.course.image and request else None,
        }

    def to_dict(self, request=None):
        return {
            "code": self.code,
            "course": self.course_data(request),
            "activated_at": self.activated_at,
            "expires_at": self.activated_at + timedelta(days=self.valid_days) if self.activated_at else None,
            "is_valid": self.is_valid(),
        }

    def __str__(self):
        return f"{self.code} - {self.course.title} ({'Used' if self.used else 'Unused'})"
