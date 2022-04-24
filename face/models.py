from django.db import models

# Create your models here.
class Person(models.Model):
    roll_number = models.CharField(max_length=30,unique=True)
    name = models.CharField(max_length=255)
    encoding = models.JSONField()

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()   

class Timings(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField()
    wow = models.CharField(max_length=60)