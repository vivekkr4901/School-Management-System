from django.db import models
from django.contrib.auth.models import AbstractUser

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
