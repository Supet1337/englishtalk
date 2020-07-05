import json
import redis
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail

from .models import *
from .forms import *


def loggout(request):
    logout(request)
    return HttpResponseRedirect("/")

def login_user(request):

    if request.method == "POST":
        email = request.POST['email_auth']
        password = request.POST['password']
        usernm = User.objects.get(email=email)
        user = authenticate(username=usernm.username, password=password)
        if user is not None:
            login(request, user)
            messages.error(request, 'Вы успешно авторизировались.')
            return HttpResponseRedirect("/")
        else:
            messages.error(request, 'Введены неверные данные.')
            return HttpResponseRedirect("/")




def register_user(request):


    if request.method == "POST":
        user = User()
        user.username = get_random_string(length=16)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('surname')
        user.email = request.POST.get('email')
        password = User.objects.make_random_password()
        user.password = make_password(password)
        user_add = UserAdditionals()
        user_add.user = user
        user_add.phone_number = request.POST.get('phone')
        if len(User.objects.filter(email=user.email)) > 0:
            messages.error(
                request, "Пользователь с такой почтой уже существует.")
        else:
            user.save()
            user_add.save()
            login(request, user)
            message = "Hello!" +user.first_name+" "+user.last_name+ "\nПоздравляем!" \
                " Вы успешно зарегестрировали аккаунт EnglishTalk.\nВперёд к " \
                "новым знаниям!\n" \
                      "Ваш пароль:\n"+str(password)+"\n" \
                " С уважением, команда EnglishTalk  "
            send_mail(
                'Регистрация аккаунта EnglishTalk', message, 'noreply.englishtalk@gmail.com', [
                user.email], fail_silently=False)
            messages.success(request, "Вы успешно зарегистрировались. Ваш пароль отправлен на "+str(user.email))
    return HttpResponseRedirect('../')


def index(request):
    return render(request,'index.html')

def dashboard(request):
    context = {}
    lsn = Lesson.objects.all()
    context["lsn"] = lsn
    return render(request,'dashboard.html', context)



def ajax_load_lessons(request, number):
    lsn = []
    lsn.append(Lesson.objects.get(id=number).json())
    return HttpResponse(json.dumps(lsn))

def ajax_load_lessons_videos(request, number):
    vid = []
    for i in Lesson.objects.get(id=number).get_lesson_videos():
        vid.append(i.json())
    return HttpResponse(json.dumps(vid))

def ajax_load_lessons_audios(request, number):
    aud = []
    for i in Lesson.objects.get(id=number).get_lesson_audios():
        aud.append(i.json())
    return HttpResponse(json.dumps(aud))



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
