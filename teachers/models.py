from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='teachers/')
    description = models.TextField()

    def __str__(self):
        return self.name
