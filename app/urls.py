from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),  # Home page
    path('notice_list/',views.notice_list,name="notice_list"),
    path('notices/add/',views.add_notice,name="add_notice"),
    path('upload_materials/',views.upload_materials,name="upload_materials"),
    path('materials_list/',views.materials_list,name="materials_list"),
    path('materials/download/<int:pk>/', views.download_material, name='download_material'),
    path('profile/', views.profile, name='profile'),
    path('markattendance/',views.attendancetrack,name='markattendance'),
    path('attendancelist/',views.attendancerecord,name='attendancelist'),
     path('take-attendance/', views.take_attendance, name='take-attendance'),
    path('view-attendance/', views.view_attendance, name='view-attendance'),
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),
    path("contact_us/",views.contact_us,name="contact_us"),
    path("school_address/",views.school_address,name="school_address"),
    path('waiting/', views.waiting_page, name='waiting_page'),
    path('manage_roles/', views.manage_roles, name='manage_roles'),
     path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
     path('success/', views.success_page, name='success_page'),
    path('users/', views.user_list, name='user_list'),

]

