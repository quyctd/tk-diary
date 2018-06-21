from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime


# Create your models here.

class Class(models.Model):
    name = models.CharField(max_length = 255)
    number = models.IntegerField()

    def __str__(self):
        return self.name+str(self.number)

class Diary(models.Model):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    time = models.TimeField(default = datetime.now)
    classroom = models.ForeignKey(Class, on_delete = models.CASCADE, related_name='diary')
    note_summary = RichTextField()

    def __str__(self):
        return self.classroom + str(self.time)

class NotePrecise(models.Model):
    for_student = models.CharField(max_length = 255)
    diary = models.ForeignKey(Diary, on_delete = models.CASCADE, related_name='note_precise')
    note = RichTextField()

    def __str__(self):
        return self.for_student + self.diary.classroom