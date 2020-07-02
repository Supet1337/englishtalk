from django.shortcuts import render, redirect

def index(request):
    return render(request,'index.html')

def dashboard(request):
    return render(request,'dashboard.html')

def courses(request):
    return render(request,'courses.html')

def ielts(request):
    return render(request,'courses/ielts.html')

def interview(request):
    return render(request,'courses/interview.html')

def freespeaking(request):
    return render(request,'courses/freespeaking.html')

def it(request):
    return render(request,'courses/it.html')

def travel(request):
    return render(request,'courses/travel.html')

def business(request):
    return render(request,'courses/business.html')

def exam(request):
    return render(request,'courses/exam.html')

def engineer(request):
    return render(request,'courses/engineer.html')

def teen(request):
    return render(request,'courses/teen.html')

def child(request):
    return render(request,'courses/child.html')

def personally(request):
    return render(request,'courses/personally.html')

def anylevel(request):
    return render(request,'courses/anylevel.html')

def grammar(request):
    return render(request,'courses/grammar.html')

def blog(request):
    return render(request,'blog-single.html')

def video(request):
    return render(request,'video.html')
