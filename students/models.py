from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


def validate_file_size(value):
    limit=5*1024*1024
    if value.size>limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')
    


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    photo = models.FileField(upload_to='photos/', validators=[validate_file_size])

    def __str__(self):
        return self.name