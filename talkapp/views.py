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
from django.core.mail import EmailMessage

from .models import *
from .forms import *

@login_required
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


def password_reset_done(request):
    messages.success(
        request, "Мы отправили инструкцию по восстановлению пароля на вашу почту. "
                 "Если в течение нескольких минут ничего не пришло, проверьте спам.")
    return HttpResponseRedirect("/")

def password_reset_complete(request):
    messages.success(
        request, "Пароль успешно изменён!")
    return HttpResponseRedirect("/")

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.data['email']
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
        if request.user.is_authenticated:
            req = Request()
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('surname')
            phone_number = request.POST.get('phone')
            req.user = request.user
            req.first_name = first_name
            req.last_name = last_name
            req.phone_number = phone_number
            req.save()
            message = "Hello! " +first_name+" "+last_name+ "\nПоздравляем!" \
                " Вы подали заявку на пробный урок. \nВ скором времени вам " \
                "перезвонят.\n\n\n" \
                "С уважением, команда EnglishTalk  "
            send_mail(
                'Заявка на курс EnglishTalk', message, 'noreply.englishtalk@gmail.com', [
                request.user.email], fail_silently=False)
            messages.success(request, "Вы успешно подали заявку. Проверьте почтовый ящик "+str(request.user.email))
        else:
            messages.warning(request, "Для подачи заявки необходима авторизация")
        return HttpResponseRedirect('/')


def index(request):
    return render(request,'index.html')

@login_required
def dashboard(request):
    context = {}
    is_teacher = False
    if len(Teacher.objects.filter(user=request.user)) > 0:
        is_teacher = True
    context["is_teacher"] = is_teacher
    try:
        context["req"] = Request.objects.get(user=request.user).first_name
    except:
        context["req"] = request.user.username

    if is_teacher:
        lsn = User_Lesson.objects.filter(teacher=Teacher.objects.get(user=request.user))
    else:
        lsn = User_Lesson.objects.filter(student=request.user)
    if len(lsn) == 0:
        context["lsn"] = 0
        context['next_lsn'] = "У вас нет занятий"
        context['course'] = "Нет"
    else:
        lsn.order_by('date')
        context['next_lsn'] = lsn[0].date
        if lsn[0].lesson_time:
            context['lsn_time'] = "60"
        else:
            context['lsn_time'] = "45"
        context['course'] = lsn[0].lesson.course.name
        context["lsn"] = lsn
    return render(request,'dashboard.html', context)

@login_required
def change_email(request):
    if request.method == "POST":
        email = request.POST.get("change_email")
        user = request.user
        user.email = email
        if len(User.objects.filter(email=email)) > 0:
                messages.error(
                    request, "Пользователь с такой почтой уже существует.")
                return HttpResponseRedirect("../")
        else:
            user.save()
            messages.success(
                    request, "Почта успешно изменена.")
        return HttpResponseRedirect('/dashboard')

def ajax_load_lessons(request, number):
    lsn = []
    lsn.append(User_Lesson.objects.get(id=number).json())
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

@login_required
def price(request):
    return render(request,'price.html')

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
    context = {}
    blog = Blog.objects.get(id=1)
    context["blog"] = blog
    return render(request,'blog-single.html', context)

def video(request):
    return render(request,'video.html')
