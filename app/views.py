from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, NoticeForm, StudyMaterialForm
from .models import User, Notice, StudyMaterial

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.base_role = form.cleaned_data['role']
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

@login_required
def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'notices/notice_list.html', {'notices': notices})

@login_required
def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            return redirect('notice_list')
    else:
        form = NoticeForm()
    return render(request, 'notices/add_notice.html', {'form': form})

@login_required
def upload_materials(request):
    if request.user.role != 'TEACHER':
        return redirect('home')
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            return redirect('materials_list')
    else:
        form = StudyMaterialForm()
    return render(request, 'upload_materials.html', {'form': form})

@login_required
def materials_list(request):
    Class= request.POST.get('Standard')
    materials = StudyMaterial.objects.all().filter(class_assigned=Class)
    return render(request, 'materials_list.html', {'materials': materials})



from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from urllib.parse import quote


@login_required
def download_material(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk)
    response = HttpResponse(material.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{quote(material.file.name)}"'
    return response
