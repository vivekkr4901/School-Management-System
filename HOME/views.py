from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse

def home(request):
    return HttpResponse("HELLO WELCOME TO THE SCHOOL-MANAGEMENT-SYSTEM")

