from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, NoticeForm, StudyMaterialForm
from .models import User, Notice, StudyMaterial
from django.utils import timezone
from datetime import timedelta
from .models import *
from .forms import *
from django.urls import reverse
from urllib.parse import quote
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('waiting_page')  # Redirect to a waiting page
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def waiting_page(request):
    if request.user.role !='WAITING':
        return redirect('login')
    
    else:

        return render(request, 'waiting.html')





def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
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

@login_required(redirect_field_name="{% url 'login' %}")
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

@login_required(redirect_field_name="{% url 'login' %}")


def notice_list(request):
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    notices = Notice.objects.filter(created_at__gte=seven_days_ago).order_by('-created_at')

    return render(request, 'notices/notice_list.html', {'notices': notices})

@login_required(redirect_field_name="{% url 'login' %}")
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

@login_required(redirect_field_name="{% url 'login' %}")
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

@login_required(redirect_field_name="{% url 'login' %}")
def materials_list(request):
    Class= request.POST.get('Standard')
    materials = StudyMaterial.objects.all().filter(class_assigned=Class)
    return render(request, 'materials_list.html', {'materials': materials})



@login_required(redirect_field_name="{% url 'login' %}")
def download_material(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk)
    response = HttpResponse(material.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{quote(material.file.name)}"'
    return response


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name="{% url 'login' %}")
def profile(request):
    if request.user.role != User.Role.STUDENT:
        # For non-student users, render the general profile page
        return render(request, 'profile.html')
    else:
        # For students, redirect to their specific student profile page
        try:
            student = Students.objects.get(id=request.user.id)
            return redirect(reverse('student_profile', args=[student.id]))  # Replace with your student profile URL name
        except Students.DoesNotExist:
            # Handle case where student profile does not exist
            return render(request, 'profile.html')

@login_required
def student_profile(request, student_id):
    student = Students.objects.get(pk=student_id)
    attendance_percentage = student.get_attendance_percentage()
    return render(request, 'student_profile.html', {
        'student': student,
        'attendance_percentage': attendance_percentage,
    })


def attendancetrack(request):
    if request.method == 'POST':
        form = attendanceform(request.POST)
        if form.is_valid():
            attendancestatus=form.save(commit=False)
            attendancestatus.save()  # Save the form data directly
            return redirect('attendancelist')  # Redirect to the attendancerecord URL
    else:
        form = attendanceform()
    return render(request, 'markattendance.html', {'form': form})

from .models import Subject, attendance
from django.shortcuts import render

def attendancerecord(request):
    if request.method == 'POST':
        subject_name = request.POST.get('SUBJECT')
        
        # Retrieve the Subject instance based on the subject_name
        subject = Subject.objects.get(subject_name=subject_name)

        # Get attendance records for the selected subject
        attendance_records = attendance.objects.filter(subject=subject)

        total_classes = attendance_records.count()
        classes_attended = attendance_records.filter(status=True).count()

        # Calculate attendance percentage
        if total_classes > 0:
            attendance_percentage = (classes_attended / total_classes) * 100
        else:
            attendance_percentage = 0

        return render(request, 'attendancelist.html', {'attendance_percentage': attendance_percentage})

    return render(request, 'attendancelist.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ClassAttendanceBulkForm
from .models import ClassAttendance, ClassSubject, Students

@login_required
def take_attendance(request):
    if request.user.role != User.Role.TEACHER:
        return redirect('home')

    if request.method == "POST":
        form = ClassAttendanceBulkForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            subject = form.cleaned_data['subject']
            attendance_data = form.cleaned_data['attendance']

            for student_id in attendance_data:
                student = Students.objects.get(id=student_id)
                ClassAttendance.objects.update_or_create(
                    student=student, 
                    subject=subject, 
                    date=date, 
                    defaults={'present': True}
                )

            messages.success(request, "Attendance successfully taken")
            return redirect('take-attendance')
    else:
        form = ClassAttendanceBulkForm()

    return render(request, 'attendance/take_attendance.html', {'form': form})

@login_required
def view_attendance(request):
    if request.user.role == User.Role.STUDENT:
        attendance_records = ClassAttendance.objects.filter(student=request.user)
        attendance_percentage = request.user.get_attendance_percentage()
    elif request.user.role == User.Role.TEACHER:
        attendance_records = ClassAttendance.objects.filter(subject__teacher=request.user)
        attendance_percentage = None
    else:
        attendance_records = None
        attendance_percentage = None

    return render(request, 'attendance/view_attendance.html', {
        'attendance_records': attendance_records,
        'attendance_percentage': attendance_percentage,
    })




def contact_us(request):
    return render(request,"contact_us.html")



def school_address(request):
    return render(request,"school_address.html")


#this is used just for the admin to use website rather than admin interface for assigning roles 

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import User

@user_passes_test(lambda u: u.is_superuser)
def manage_roles(request):
    users = User.objects.filter(role=User.Role.WAITING)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role = request.POST.get('role')
        user = get_object_or_404(User, id=user_id)
        user.role = role
        user.save()
        return redirect('manage_roles')
    return render(request, 'manage_roles.html', {'users': users})

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import HttpResponseForbidden
@login_required
def delete_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    # Check if the request.user can delete the target_user
    if request.user.role == User.Role.PRINCIPAL:
        if target_user.role not in [User.Role.TEACHER, User.Role.STUDENT]:
            return HttpResponseForbidden("You do not have permission to delete this user.")
    elif request.user.role == User.Role.TEACHER:
        if target_user.role != User.Role.STUDENT:
            return HttpResponseForbidden("You do not have permission to delete this user.")
    else:
        return HttpResponseForbidden("You do not have permission to delete this user.")

    target_user.delete()
    return redirect('success_page')  

@login_required
def success_page(request):
    return render(request, 'success_page.html')

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})






#for test taking system

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Test, Question, Option

@login_required
def create_test(request):
    if request.user.role != User.Role.TEACHER:
        raise PermissionDenied

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        test = Test.objects.create(title=title, description=description, created_by=request.user)
        for i in range(1, 5):
            question_text = request.POST.get(f'question_{i}')
            if question_text:
                question = Question.objects.create(test=test, text=question_text)
                for j in range(1, 6):
                    option_text = request.POST.get(f'option_{i}_{j}')
                    if option_text:
                        is_correct = f'correct_{i}_{j}' in request.POST
                        Option.objects.create(question=question, text=option_text, is_correct=is_correct)

        return redirect('test_list')

    return render(request, 'create_test.html')

User = get_user_model()

@login_required
def take_test(request, test_id):
    if request.user.role != User.Role.STUDENT:
        raise PermissionDenied

    test = get_object_or_404(Test, id=test_id)

    if request.method == 'POST':
        total_questions = 0
        correct_answers = 0

        for question in test.questions.all():
            selected_option_id = request.POST.get(str(question.id))
            selected_option = get_object_or_404(Option, id=selected_option_id)
            StudentAnswer.objects.create(student=request.user, question=question, selected_option=selected_option)

            if selected_option.is_correct:
                correct_answers += 1
            total_questions += 1

        score = (correct_answers / total_questions) * 100
        result = Result.objects.create(student=request.user, test=test, score=score)

        return redirect('result_detail', result_id=result.id)
        

    return render(request, 'take_test.html', {'test': test})


@login_required
def result_detail(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    
    # Initialize the count in the session if it doesn't exist
    if 'count' not in request.session:
        request.session['count'] = 0
    
    # Increment the count
    request.session['count'] += 1
    
    # Retrieve the count from the session
    count = request.session['count']
    
    return render(request, 'result_detail.html', {'result': result, 'count': count})


@login_required
def test_list(request):
    if request.user.role != User.Role.TEACHER:
        raise PermissionDenied

    tests = Test.objects.filter(created_by=request.user)
    return render(request, 'test_list.html', {'tests': tests})

@login_required
def available_tests(request):
    if request.user.role != User.Role.STUDENT:
        raise PermissionDenied

    tests = Test.objects.all()
    return render(request, 'available_tests.html', {'tests': tests})
