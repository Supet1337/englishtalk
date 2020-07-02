import json
import redis
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail

from .models import *
from .forms import *

def register_user(request, backend='django.contrib.auth.backends.ModelBackend'):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.data['email']
            user.first_name = request.POST.get('name')
            user.password = "User.objects.make_random_password()"
            user_add = UserAdditionals()
            user_add.user = user
            user_add.phone_number = request.POST.get('phone')
            #if len(User.objects.filter(email=form.data['email'])) > 0:
                #messages.error(
                   # request, "Пользователь с такой почтой уже существует.")
                #return HttpResponseRedirect("../")
            #elif len(User.objects.filter(username=form.data['username'])) > 0:
              #  messages.error(
               #     request, "Пользователь с таким ником уже существует.")
              #  return HttpResponseRedirect("/")
            #elif check_password(request.POST.get('password1'), request.POST.get('password2')):
                #messages.error(request, 'Пароли не совпадают.')
                #return HttpResponseRedirect("/")
            #else:
            user.save()
            user_add.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                #message = "Здравствуйте! {}\nПоздравляем!" \
                      #    " Вы успешно зарегестрировали аккаунт Geochat.\nВперёд к " \
                     #     "новым приключениям!\n\n\n" \
                     #     " С уважением, команда Geochat  ".format(user.username)
                #send_mail(
                   # 'Регистрация аккаунта Geochat', message, 'shp.geochat@yandex.ru', [
                     #   user.email], fail_silently=False)
        return HttpResponseRedirect('../')



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
