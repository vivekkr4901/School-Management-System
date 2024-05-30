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
    path('study_materials/download_material/<int:pk>/', views.download_material, name='download_material')
]