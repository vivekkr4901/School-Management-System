from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm
from .models import User

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

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

from django.contrib.auth.decorators import login_required
from .models import Notice
from .forms import NoticeForm

@login_required   #decorators : property of a oops
def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'notices/notice_list.html', {'notices': notices})   #to sort the order in which the notices are given to the students

@login_required
def add_notice(request):     #to create notice for the students
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
