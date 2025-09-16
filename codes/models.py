from django.db import models
from django.utils import timezone
from datetime import timedelta
from courses.models import Course
from accounts.models import Student


class CourseCode(models.Model):
    code = models.CharField(max_length=12, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="codes")
    assigned_to = models.ForeignKey(Student, null=True, blank=True, on_delete=models.SET_NULL)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    valid_days = models.PositiveIntegerField(default=30)  # default validity = 30 days

    def activate(self, student):
        """
        فعل الكود لليوزر لأول مرة
        """
        if self.used:   # لو متفعل قبل كده خلاص
            return False

        self.assigned_to = student
        self.used = True
        self.activated_at = timezone.now()
        self.save()
        return True

    def is_valid(self):
        """
        يتأكد إن الكود متفعل ولسه في الصلاحية
        """
        if self.used and self.activated_at:
            expiration = self.activated_at + timedelta(days=self.valid_days)
            return timezone.now() <= expiration
        return False

    def __str__(self):
        return f"{self.code} - {self.course.title} ({'Used' if self.used else 'Unused'})"
