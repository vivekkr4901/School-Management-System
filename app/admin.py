from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Notice)
admin.site.register(StudyMaterial)
admin.site.register(Subject)
admin.site.register(attendance)
admin.site.register(ClassAttendance)
admin.site.register(ClassSubject)