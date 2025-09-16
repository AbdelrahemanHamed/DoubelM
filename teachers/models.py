from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='teachers/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
