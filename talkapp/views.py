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

def register_user(request):

    if request.method == "POST":
        user = User()
        user.username = get_random_string(length=16)
        user.first_name = request.POST.get('first_name')
        user.email = request.POST.get('email')
        user.password = make_password(User.objects.make_random_password())
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
            message = "Здравствуйте! {}\nПоздравляем!" \
                " Вы успешно зарегестрировали аккаунт Geochat.\nВперёд к " \
                "новым приключениям!\n\n\n" \
                " С уважением, команда Geochat  ".format(user.username)
            send_mail(
                'Регистрация аккаунта Geochat', message, 'noreply.englishtalk@gmail.com', [
                user.email], fail_silently=False)
            messages.success(request, "Вы успешно зарегистрировались.")
    return HttpResponseRedirect('../')


def index(request):
    return render(request,'index.html')

def dashboard(request):
    context = {}
    lsn = Lessons.objects.all()
    context["lsn"] = lsn
    return render(request,'dashboard.html', context)



def ajax_load_lessons(request, number):
    lsn = []
    for ls in Lessons.objects.filter(id=number):
        lsn.append(ls.json())
    return HttpResponse(json.dumps(lsn))




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
