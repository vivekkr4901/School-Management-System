from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
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




class Students(User):
    
    base_role=User.Role.STUDENT

    class Meta:
        proxy=True
    
    def Welcome(self):
        return "only for students"
    

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
    


