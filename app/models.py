from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class User(AbstractUser):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        PRINCIPAL = "PRINCIPAL", 'Principal'
        STUDENT = "STUDENT", 'Student'
        TEACHER = "TEACHER", 'Teacher'

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)

    def save(self, *args, **kwargs):
        if not self.pk:  # If the user is being created
            self.role = self.base_role
        super().save(*args, **kwargs)
    


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.STUDENT)

class Students(User):
    base_role = User.Role.STUDENT

    objects = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "only for students"
    

    def get_attendance_percentage(self):
        total_classes = ClassAttendance.objects.filter(student=self).count()
        attended_classes = ClassAttendance.objects.filter(student=self, present=True).count()
        return (attended_classes / total_classes) * 100 if total_classes > 0 else 0

    

class teachers(User):
    
    base_role=User.Role.TEACHER

    class Meta:
        proxy=True
    
    def Welcome(self):
        return "only for teachers"
    
class Principal(User):
    
    base_role=User.Role.PRINCIPAL

    class Meta:
        proxy=True
    
    def Welcome(self):
        return "only for Principal"
    
class Notice(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    




class StudyMaterial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='study_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    class_assigned = models.IntegerField(choices=[(i, str(i)) for i in range(1, 13)])

    def __str__(self):
        return self.title

class Subject(models.Model):
    subject_name=models.CharField(max_length=200)


    def __str__(self):
        return self.subject_name


class attendance(models.Model):
    subject=models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    status=models.BooleanField(default=False)
    date=models.DateField()


class ClassSubject(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.ForeignKey(teachers, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ClassAttendance(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    present = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Class Attendance"
        verbose_name_plural = "Class Attendances"

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} - {self.date} - {'Present' if self.present else 'Absent'}"






