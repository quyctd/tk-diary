from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Class(models.Model):
    name_course = models.CharField(max_length = 255)
    number = models.IntegerField()
    teacher = models.CharField(max_length = 255, blank = True)
    support = models.CharField(max_length = 255, blank = True)
    def __str__(self):
        return self.name_course+" "+str(self.number)
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classrooms'

class Diary(models.Model):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    time = models.DateField(default = datetime.now)
    classroom = models.ForeignKey(Class, on_delete = models.CASCADE, related_name='diary')
    note_summary = RichTextField()

    def __str__(self):
        return self.classroom.name_course +" "+str(self.classroom.number) +" - "+ datetime.strftime(self.time, "%d/%m/%Y")

    class Meta:
        verbose_name = 'Diary'
        verbose_name_plural = 'Diaries'

class NotePrecise(models.Model):
    for_student = models.CharField(max_length = 255)
    diary = models.ForeignKey(Diary, on_delete = models.CASCADE, related_name='note_precise')
    note = RichTextField()

    def __str__(self):
        return self.for_student +" "+ self.diary.classroom.name_course +" "+ str(self.diary.classroom.number)
    class Meta:
        verbose_name = 'Note Precise'
        verbose_name_plural = 'Note for each Student'

class UserProfile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    HEADLINE_CHOICES = (
        ("Teacher", "Teacher"),
        ("Supporter", "Supporter")
    )
    headline = models.CharField(
        max_length=255, choices=HEADLINE_CHOICES, default=HEADLINE_CHOICES[0])

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
