import datetime
import json
import redis
import time
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import *
from .forms import *

@login_required
def loggout(request):
    logout(request)
    return HttpResponseRedirect("/")

def login_user(request):
    if request.method == "POST":
        email = request.POST['email_auth']
        password = request.POST['password']
        username = User.objects.get(email=email)
        user = authenticate(username=username.username, password=password)
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



def send_request_view(request):
    if request.method == "POST":
        user = User()
        user.username = get_random_string(length=16)
        name = request.POST.get('name')
        FIO = list(name.split())
        user.first_name = FIO[0]
        user.last_name = FIO[1]
        user.email = request.POST.get('email')
        password = User.objects.make_random_password()
        user.password = make_password(password)
        if len(User.objects.filter(email=request.POST.get('email'))) > 0:
            messages.error(request, 'Пользователь с такой почтой уже существует.')
        else:
            user.save()
            req = Request()
            phone_number = request.POST.get('phone')
            req.user = user
            req.phone_number = phone_number
            req.save()
            html_message = render_to_string('request_mail.html', {'email': user.email,
                                                                  'password': password
                                                                  })

            message = strip_tags(html_message)
            send_mail(
                'Команда EnglishTalk приветствует Вас!', message, 'noreply.englishtalk@gmail.com', [
                user.email], fail_silently=False, html_message=html_message)
            help_message = "Новая заявка на обучение от " +user.first_name+" "+user.last_name+ "!\n" \
                            "Телефон клиента: "+ phone_number + ",\n"\
                            "Почта клиента: "+ user.email + "."
            send_mail(
                'Ура! У нас новая зявка на обучение!', help_message, 'noreply.englishtalk@gmail.com', [
                    "maksrubinov@mail.ru"], fail_silently=False)
            messages.info(request, "Вы успешно подали заявку. Проверьте почтовый ящик "+str(user.email))
    return HttpResponseRedirect('/')

def send_request_view_teach(request):
    if request.method == "POST":
        user = User()
        user.username = get_random_string(length=16)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('surname')
        user.email = request.POST.get('email')
        password = User.objects.make_random_password()
        user.password = make_password(password)
        if len(User.objects.filter(email=request.POST.get('email'))) > 0:
            messages.error(request, 'Пользователь с такой почтой уже существует.')
        else:
            user.save()
            req = Request()
            phone_number = request.POST.get('phone')
            req.user = user
            req.phone_number = phone_number
            req.save()
            message = "Здраствуйте," +user.first_name+" "+user.last_name+ "!\n" \
                    " Вы успешно подали заявку на преподавание урок. \nВ скором времени вам " \
                    "перезвонят.\n\n\n" \
                    "Данные для входа в личный кабинет:\n" \
                    "Логин: "+ user.email +"\n"\
                    "Пароль: "+ password
            send_mail(
                'Заявка на курс EnglishTalk', message, 'noreply.englishtalk@gmail.com', [
                user.email], fail_silently=False)
            help_message = user.first_name + " " + user.last_name + " хочет начать преподавать.\n" \
                           "Телефон: " + phone_number + ",\n" \
                           "Почта: " + user.email + "."
            send_mail(
                'Новая заявка от преподавателя!', help_message, 'noreply.englishtalk@gmail.com', [
                    "maksrubinov@mail.ru"], fail_silently=False)
            messages.info(request, "Вы успешно подали заявку. Проверьте почтовый ящик "+str(user.email))
    return HttpResponseRedirect('/')

def ask_question(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('surname')
        phone_number = request.POST.get('phone')
        message = "Как зовут клиента: "+first_name+" "+last_name+ ".\n" \
                    "Телефон клиента: " + phone_number
        send_mail(
            'Нужна консультация!', message, 'noreply.englishtalk@gmail.com', [
                'maksrubinov@mail.ru'], fail_silently=False)
        messages.info(request, "Вы успешно подали заявку. Проверьте почтовый ящик")
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
    if is_teacher:
        crs = Course.objects.filter(teacher=Teacher.objects.get(user=request.user))
    else:
        crs = Course.objects.filter(student=request.user)
    lessons = Lesson.objects.filter(course__in=crs)
    if len(lessons) == 0:
        context["lsn"] = 0
        context['next_lsn'] = "У вас нет занятий"
        context['course'] = "Нет"
    else:
        lessons.order_by('date')
        i = 0
        context['next_lsn'] = lessons[i].date
        if lessons[i].course.lesson_time:
            context['lsn_time'] = "60"
        else:
            context['lsn_time'] = "45"
        context['course'] = lessons[i].course.name
        context["lsn"] = lessons
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

def blog(request):
    context = {}
    blog = Blog.objects.get(id=1)
    context["blog"] = blog
    return render(request,'blog-single.html', context)

def video(request):
    return render(request,'video.html')
