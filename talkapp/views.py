from django.shortcuts import render, redirect

def index(request):
    return render(request,'index.html')

def profile(request):
    return render(request,'profile.html')

def courses(request):
    return render(request,'courses.html')

def about(request):
    return render(request,'about.html')
