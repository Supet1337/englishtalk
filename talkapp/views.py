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
        username = request.POST['username_auth']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.error(request, 'Неправильный логин или пароль.')
            return HttpResponseRedirect("/")





def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.data['email']
            user_add = UserAdditionals()
            user_add.user = user
            if len(User.objects.filter(email=form.data['email'])) > 0:
                messages.error(
                    request, "Пользователь с такой почтой уже существует.")
                return HttpResponseRedirect("../")
            elif len(User.objects.filter(username=form.data['username'])) > 0:
                messages.error(
                    request, "Пользователь с таким ником уже существует.")
                return HttpResponseRedirect("/")
            elif check_password(request.POST.get('password1'), request.POST.get('password2')):
                messages.error(request, 'Пароли не совпадают.')
                return HttpResponseRedirect("/")
            else:
                user.save()
                user_add.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                message = "Hello! {}\nПоздравляем!" \
                          " Вы успешно зарегестрировали аккаунт EnglishTalk.\nВперёд к " \
                          "новым знаниям!\n\n\n" \
                          "С уважением, команда Englishtalk  ".format(user.username)
                send_mail(
                    'Регистрация аккаунта Englishtalk', message, 'noreply.englishtalk@gmail.com', [
                        user.email], fail_silently=False)
        return HttpResponseRedirect('../')


def send_request_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('surname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        message = "Hello! " +first_name+" "+last_name+ "\nПоздравляем!" \
            " Вы подали заявку на пробный урок. \nВ скором времени вам " \
            "перезвонят.\n\n\n" \
            "С уважением, команда EnglishTalk  "
        send_mail(
            'Заявка на курс EnglishTalk', message, 'noreply.englishtalk@gmail.com', [
            email], fail_silently=False)
        messages.success(request, "Вы успешно подали заявку. Проверьте почтовый ящик "+str(email))
        return HttpResponseRedirect('/')


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

def ajax_load_video(request, number):
    vid = []
    vid.append(Lesson_video.objects.get(id=number).json())
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
