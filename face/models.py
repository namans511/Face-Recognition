from django.db import models

# Create your models here.
class Person(models.Model):
    roll_number = models.CharField(max_length=30)
    name = models.CharField(max_length=255)
    encoding = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()   