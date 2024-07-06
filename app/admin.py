from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(Notice)
admin.site.register(StudyMaterial)
admin.site.register(Subject)
admin.site.register(attendance)
admin.site.register(ClassAttendance)
admin.site.register(ClassSubject)

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')

admin.site.register(User, CustomUserAdmin)

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(StudentAnswer)
admin.site.register(Result)
admin.site.register(Option)
admin.site.register(Messages)