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

def redirect_login(request):
    return HttpResponseRedirect("/")

def login_user(request):
    if request.method == "POST":
        email = request.POST['email_auth']
        password = request.POST['password']
        try:
            username = User.objects.get(email=email)
            user = authenticate(username=username.username, password=password)
        except:
            user = None
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/dashboard/lk")
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

def confidentiality(request):
    return render(request, "confidentiality.html")

def oferta(request):
    return render(request, "oferta.html")

def send_request_view(request):
    if request.method == "POST":
        user = User()
        user.username = get_random_string(length=32)
        user.first_name = request.POST.get('name')
        user.email = request.POST.get('email')
        password = User.objects.make_random_password()
        user.password = make_password(password)
        if len(User.objects.filter(email=request.POST.get('email'))) > 0:
            messages.error(request, 'Пользователь с такой почтой уже существует.')
        else:
            roomName = get_random_string(length=32)
            user.save()
            req = UserAdditional()
            phone_number = request.POST.get('phone')
            req.user = user
            req.phone_number = phone_number
            req.video_chat = roomName
            req.save()
            room = ChatRoom()
            room.name = roomName
            room.student = user
            room.save()
            html_message = render_to_string('request_mail.html', {'email': user.email,
                                                                  'password': password
                                                                  })

            message = strip_tags(html_message)
            send_mail(
                'Команда EnglishTalk приветствует Вас!', message, 'noreply.englishtalk@gmail.com', [
                user.email], fail_silently=False, html_message=html_message)
            help_message = "Новая заявка на обучение от " +user.first_name+"!\n" \
                            "Телефон клиента: "+ phone_number + ",\n"\
                            "Почта клиента: "+ user.email + "."
            send_mail(
                'Ура! У нас новая зявка на обучение!', help_message, 'noreply.englishtalk@gmail.com', [
                    "help.englishtalk@gmail.com"], fail_silently=False)
            messages.info(request, "Вы успешно подали заявку. Проверьте почтовый ящик "+str(user.email))
    return HttpResponseRedirect('/')

def send_request_view_teach(request):
    if request.method == "POST":
        user = User()
        user.username = get_random_string(length=32)
        user.first_name = request.POST.get('name')
        user.email = request.POST.get('email')
        password = User.objects.make_random_password()
        user.password = make_password(password)
        if len(User.objects.filter(email=request.POST.get('email'))) > 0:
            messages.error(request, 'Пользователь с такой почтой уже существует.')
        else:
            user.save()
            req = UserAdditional()
            phone_number = request.POST.get('phone')
            req.user = user
            req.phone_number = phone_number
            req.save()
            message = "Здраствуйте," +user.first_name+"!\n" \
                    " Вы успешно подали заявку на преподавание уроками. \nВ скором времени вам " \
                    "перезвонят.\n\n\n" \
                    "Данные для входа в личный кабинет:\n" \
                    "Логин: "+ user.email +"\n"\
                    "Пароль: "+ password
            send_mail(
                'Заявка на курс EnglishTalk', message, 'noreply.englishtalk@gmail.com', [
                user.email], fail_silently=False)
            help_message = user.first_name + " хочет начать преподавать.\n" \
                           "Телефон: " + phone_number + ",\n" \
                           "Почта: " + user.email + "."
            send_mail(
                'Новая заявка от преподавателя!', help_message, 'noreply.englishtalk@gmail.com', [
                    "help.englishtalk@gmail.com"], fail_silently=False)
            messages.info(request, "Вы успешно подали заявку. Проверьте почтовый ящик "+str(user.email))
    return HttpResponseRedirect('/')

def ask_question(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        message = "Как зовут клиента: "+name+".\n" \
                    "Телефон клиента: " + phone_number
        send_mail(
            'Нужна консультация!', message, 'noreply.englishtalk@gmail.com', [
                'help.englishtalk@gmail.com'], fail_silently=False)
        messages.info(request, "Вы успешно подали заявку. Проверьте почтовый ящик")
    return HttpResponseRedirect('/')

def index(request):
    context = {}
    blogs = []
    i = 0
    for b in Blog.objects.all():
        if i == 4:
            break
        blogs.append(b)
        i += 1
    context['blog'] = blogs
    return render(request,'index.html', context)

@login_required
def dashboard_lk(request):
    context = {}
    is_teacher = False
    if len(Teacher.objects.filter(user=request.user)) > 0:
        is_teacher = True
    context["is_teacher"] = is_teacher
    context['blog'] = Blog.objects.all()
    context['videos'] = VideoPractise.objects.all()
    context['video_categories'] = VideoCategory.objects.all()
    if is_teacher:
        crs = UserCourse.objects.filter(teacher=Teacher.objects.get(user=request.user))
    else:
        crs = UserCourse.objects.filter(student=request.user)
        context['video_chat'] = UserAdditional.objects.get(user=request.user).video_chat
        chat = ChatRoom.objects.get(student=request.user)
        context["chat"] = chat
    lessons = UserLesson.objects.filter(user_course__in=crs)
    if len(lessons) == 0:
        context["lsn"] = 0
    else:
        student_additional = UserAdditional.objects.get(user=request.user)
        lessons.order_by('date')
        flag = False
        past_lessons = []
        future_lessons = []
        for l in lessons:
            end = l.date
            if student_additional.lesson_time:
                end += datetime.timedelta(minutes=60)
            else:
                end += datetime.timedelta(minutes=45)
            l.date_end = end
            l.save()
            if l.date <= datetime.datetime.now() <= end and not flag:
                context['cur_lsn'] = l
                if is_teacher:
                    context['video_chat'] = UserAdditional.objects.get(user=l.user_course.student).video_chat
                    chat = ChatRoom.objects.get(student=l.user_course.student)
                    context["chat"] = chat
                context['now_lsn'] = True
                flag = True
            elif end < datetime.datetime.now():
                if not l.is_completed:
                    student_additional.paid_lessons -= 1
                    student_additional.save()
                    l.is_completed = True
                    l.save()
                past_lessons.append(l)
            elif not l.is_completed:
                if len(future_lessons) < student_additional.paid_lessons:
                    if not flag:
                        flag = True
                        context['next_lsn'] = l.date
                    future_lessons.append(l)
        context['past_lsn'] = past_lessons
        context['future_lsn'] = future_lessons
        calendar = []
        day = []
        for i in range(len(lessons)):
            if i == 0:
                day.append(lessons[i])
            elif lessons[i].date.day == lessons[i-1].date.day:
                day.append(lessons[i])
            else:
                calendar.append(day)
                day = []
                day.append(lessons[i])
        calendar.append(day)
        context['calendar'] = calendar
        i = 0
        if student_additional.lesson_time:
            context['lsn_time'] = "60"
        else:
            context['lsn_time'] = "45"
        context['course'] = lessons[i].user_course.course_type
        context['teacher'] = lessons[i].user_course.teacher.user.first_name
        context["lsn"] = lessons
        try:
            context["ava"] = lessons[i].user_course.teacher.image.url
        except:
            context["ava"] = "Аватар"
        context["paid_lessons"] = student_additional.paid_lessons


    return render(request,'dashboard/dashboard-lk.html', context)


@login_required
def dashboard_courses(request):
    context = {}
    is_teacher = False
    if len(Teacher.objects.filter(user=request.user)) > 0:
        is_teacher = True
    context["is_teacher"] = is_teacher
    context['blog'] = Blog.objects.all()
    context['videos'] = VideoPractise.objects.all()
    context['video_categories'] = VideoCategory.objects.all()
    if is_teacher:
        crs = UserCourse.objects.filter(teacher=Teacher.objects.get(user=request.user))
    else:
        crs = UserCourse.objects.filter(student=request.user)
        context['video_chat'] = UserAdditional.objects.get(user=request.user).video_chat
        chat = ChatRoom.objects.get(student=request.user)
        context["chat"] = chat
    lessons = UserLesson.objects.filter(user_course__in=crs)
    if len(lessons) == 0:
        context["lsn"] = 0
    else:
        student_additional = UserAdditional.objects.get(user=request.user)
        lessons.order_by('date')
        flag = False
        past_lessons = []
        future_lessons = []
        for l in lessons:
            end = l.date
            if student_additional.lesson_time:
                end += datetime.timedelta(minutes=60)
            else:
                end += datetime.timedelta(minutes=45)
            l.date_end = end
            l.save()
            if l.date <= datetime.datetime.now() <= end and not flag:
                context['cur_lsn'] = l
                if is_teacher:
                    context['video_chat'] = UserAdditional.objects.get(user=l.user_course.student).video_chat
                    chat = ChatRoom.objects.get(student=l.user_course.student)
                    context["chat"] = chat
                context['now_lsn'] = True
                flag = True
            elif end < datetime.datetime.now():
                if not l.is_completed:
                    student_additional.paid_lessons -= 1
                    student_additional.save()
                    l.is_completed = True
                    l.save()
                past_lessons.append(l)
            elif not l.is_completed:
                if len(future_lessons) < student_additional.paid_lessons:
                    if not flag:
                        flag = True
                        context['next_lsn'] = l.date
                    future_lessons.append(l)
        context['past_lsn'] = past_lessons
        context['future_lsn'] = future_lessons
        calendar = []
        day = []
        for i in range(len(lessons)):
            if i == 0:
                day.append(lessons[i])
            elif lessons[i].date.day == lessons[i-1].date.day:
                day.append(lessons[i])
            else:
                calendar.append(day)
                day = []
                day.append(lessons[i])
        calendar.append(day)
        context['calendar'] = calendar
        i = 0
        if student_additional.lesson_time:
            context['lsn_time'] = "60"
        else:
            context['lsn_time'] = "45"
        context['course'] = lessons[i].user_course.course_type
        context['teacher'] = lessons[i].user_course.teacher.user.first_name
        context["lsn"] = lessons
        try:
            context["ava"] = lessons[i].user_course.teacher.image.url
        except:
            context["ava"] = "Аватар"
        context["paid_lessons"] = student_additional.paid_lessons


    return render(request,'dashboard/dashboard-courses.html', context)


@login_required
def dashboard_homework(request):
    context = {}
    is_teacher = False
    if len(Teacher.objects.filter(user=request.user)) > 0:
        is_teacher = True
    context["is_teacher"] = is_teacher
    context['blog'] = Blog.objects.all()
    context['videos'] = VideoPractise.objects.all()
    context['video_categories'] = VideoCategory.objects.all()
    if is_teacher:
        crs = UserCourse.objects.filter(teacher=Teacher.objects.get(user=request.user))
    else:
        crs = UserCourse.objects.filter(student=request.user)
        context['video_chat'] = UserAdditional.objects.get(user=request.user).video_chat
        chat = ChatRoom.objects.get(student=request.user)
        context["chat"] = chat
    lessons = UserLesson.objects.filter(user_course__in=crs)
    if len(lessons) == 0:
        context["lsn"] = 0
    else:
        student_additional = UserAdditional.objects.get(user=request.user)
        lessons.order_by('date')
        flag = False
        past_lessons = []
        future_lessons = []
        for l in lessons:
            end = l.date
            if student_additional.lesson_time:
                end += datetime.timedelta(minutes=60)
            else:
                end += datetime.timedelta(minutes=45)
            l.date_end = end
            l.save()
            if l.date <= datetime.datetime.now() <= end and not flag:
                context['cur_lsn'] = l
                if is_teacher:
                    context['video_chat'] = UserAdditional.objects.get(user=l.user_course.student).video_chat
                    chat = ChatRoom.objects.get(student=l.user_course.student)
                    context["chat"] = chat
                context['now_lsn'] = True
                flag = True
            elif end < datetime.datetime.now():
                if not l.is_completed:
                    student_additional.paid_lessons -= 1
                    student_additional.save()
                    l.is_completed = True
                    l.save()
                past_lessons.append(l)
            elif not l.is_completed:
                if len(future_lessons) < student_additional.paid_lessons:
                    if not flag:
                        flag = True
                        context['next_lsn'] = l.date
                    future_lessons.append(l)
        context['past_lsn'] = past_lessons
        context['future_lsn'] = future_lessons
        calendar = []
        day = []
        for i in range(len(lessons)):
            if i == 0:
                day.append(lessons[i])
            elif lessons[i].date.day == lessons[i-1].date.day:
                day.append(lessons[i])
            else:
                calendar.append(day)
                day = []
                day.append(lessons[i])
        calendar.append(day)
        context['calendar'] = calendar
        i = 0
        if student_additional.lesson_time:
            context['lsn_time'] = "60"
        else:
            context['lsn_time'] = "45"
        context['course'] = lessons[i].user_course.course_type
        context['teacher'] = lessons[i].user_course.teacher.user.first_name
        context["lsn"] = lessons
        try:
            context["ava"] = lessons[i].user_course.teacher.image.url
        except:
            context["ava"] = "Аватар"
        context["paid_lessons"] = student_additional.paid_lessons


    return render(request,'dashboard/dashboard-homework.html', context)


@login_required
def dashboard_platform(request):
    context = {}
    is_teacher = False
    if len(Teacher.objects.filter(user=request.user)) > 0:
        is_teacher = True
    context["is_teacher"] = is_teacher
    context["email"] = request.user.email
    context['blog'] = Blog.objects.all()
    context['videos'] = VideoPractise.objects.all()
    context['video_categories'] = VideoCategory.objects.all()
    if is_teacher:
        crs = UserCourse.objects.filter(teacher=Teacher.objects.get(user=request.user))
    else:
        crs = UserCourse.objects.filter(student=request.user)
        context['video_chat'] = UserAdditional.objects.get(user=request.user).video_chat
        chat = ChatRoom.objects.get(student=request.user)
        context["chat"] = chat
    lessons = UserLesson.objects.filter(user_course__in=crs)
    if len(lessons) == 0:
        context["lsn"] = 0
    else:
        student_additional = UserAdditional.objects.get(user=request.user)
        lessons.order_by('date')
        flag = False
        past_lessons = []
        future_lessons = []
        for l in lessons:
            end = l.date
            if student_additional.lesson_time:
                end += datetime.timedelta(minutes=60)
            else:
                end += datetime.timedelta(minutes=45)
            l.date_end = end
            l.save()
            if l.date <= datetime.datetime.now() <= end and not flag:
                context['cur_lsn'] = l
                if is_teacher:
                    context['video_chat'] = UserAdditional.objects.get(user=l.user_course.student).video_chat
                    chat = ChatRoom.objects.get(student=l.user_course.student)
                    context["chat"] = chat
                context['now_lsn'] = True
                flag = True
            elif end < datetime.datetime.now():
                if not l.is_completed:
                    student_additional.paid_lessons -= 1
                    student_additional.save()
                    l.is_completed = True
                    l.save()
                past_lessons.append(l)
            elif not l.is_completed:
                if len(future_lessons) < student_additional.paid_lessons:
                    if not flag:
                        flag = True
                        context['next_lsn'] = l.date
                    future_lessons.append(l)
        context['past_lsn'] = past_lessons
        context['future_lsn'] = future_lessons
        calendar = []
        day = []
        for i in range(len(lessons)):
            if i == 0:
                day.append(lessons[i])
            elif lessons[i].date.day == lessons[i-1].date.day:
                day.append(lessons[i])
            else:
                calendar.append(day)
                day = []
                day.append(lessons[i])
        calendar.append(day)
        context['calendar'] = calendar
        i = 0
        if student_additional.lesson_time:
            context['lsn_time'] = "60"
        else:
            context['lsn_time'] = "45"
        context['course'] = lessons[i].user_course.course_type
        context['teacher'] = lessons[i].user_course.teacher.user.first_name
        context["lsn"] = lessons
        try:
            context["ava"] = lessons[i].user_course.teacher.image.url
        except:
            context["ava"] = "Аватар"
        context["paid_lessons"] = student_additional.paid_lessons


    return render(request,'dashboard/dashboard-platform.html', context)


@login_required
def dashboard_schedule(request):
    context = {}
    is_teacher = False
    if len(Teacher.objects.filter(user=request.user)) > 0:
        is_teacher = True
    context["is_teacher"] = is_teacher
    context['blog'] = Blog.objects.all()
    context['videos'] = VideoPractise.objects.all()
    context['video_categories'] = VideoCategory.objects.all()
    if is_teacher:
        crs = UserCourse.objects.filter(teacher=Teacher.objects.get(user=request.user))
    else:
        crs = UserCourse.objects.filter(student=request.user)
        context['video_chat'] = UserAdditional.objects.get(user=request.user).video_chat
        chat = ChatRoom.objects.get(student=request.user)
        context["chat"] = chat
    lessons = UserLesson.objects.filter(user_course__in=crs)
    if len(lessons) == 0:
        context["lsn"] = 0
    else:
        student_additional = UserAdditional.objects.get(user=request.user)
        lessons.order_by('date')
        flag = False
        past_lessons = []
        future_lessons = []
        for l in lessons:
            end = l.date
            if student_additional.lesson_time:
                end += datetime.timedelta(minutes=60)
            else:
                end += datetime.timedelta(minutes=45)
            l.date_end = end
            l.save()
            if l.date <= datetime.datetime.now() <= end and not flag:
                context['cur_lsn'] = l
                if is_teacher:
                    context['video_chat'] = UserAdditional.objects.get(user=l.user_course.student).video_chat
                    chat = ChatRoom.objects.get(student=l.user_course.student)
                    context["chat"] = chat
                context['now_lsn'] = True
                flag = True
            elif end < datetime.datetime.now():
                if not l.is_completed:
                    student_additional.paid_lessons -= 1
                    student_additional.save()
                    l.is_completed = True
                    l.save()
                past_lessons.append(l)
            elif not l.is_completed:
                if len(future_lessons) < student_additional.paid_lessons:
                    if not flag:
                        flag = True
                        context['next_lsn'] = l.date
                    future_lessons.append(l)
        context['past_lsn'] = past_lessons
        context['future_lsn'] = future_lessons
        calendar = []
        day = []
        for i in range(len(lessons)):
            if i == 0:
                day.append(lessons[i])
            elif lessons[i].date.day == lessons[i-1].date.day:
                day.append(lessons[i])
            else:
                calendar.append(day)
                day = []
                day.append(lessons[i])
        calendar.append(day)
        context['calendar'] = calendar
        i = 0
        if student_additional.lesson_time:
            context['lsn_time'] = "60"
        else:
            context['lsn_time'] = "45"
        context['course'] = lessons[i].user_course.course_type
        context['teacher'] = lessons[i].user_course.teacher.user.first_name
        context["lsn"] = lessons
        try:
            context["ava"] = lessons[i].user_course.teacher.image.url
        except:
            context["ava"] = "Аватар"
        context["paid_lessons"] = student_additional.paid_lessons


    return render(request,'dashboard/dashboard-schedule.html', context)


@login_required
def dashboard_tape(request):
    context = {}
    is_teacher = False
    if len(Teacher.objects.filter(user=request.user)) > 0:
        is_teacher = True
    context["is_teacher"] = is_teacher
    context['blog'] = Blog.objects.all()
    context['videos'] = VideoPractise.objects.all()
    context['video_categories'] = VideoCategory.objects.all()
    if is_teacher:
        crs = UserCourse.objects.filter(teacher=Teacher.objects.get(user=request.user))
    else:
        crs = UserCourse.objects.filter(student=request.user)
        context['video_chat'] = UserAdditional.objects.get(user=request.user).video_chat
        chat = ChatRoom.objects.get(student=request.user)
        context["chat"] = chat
    lessons = UserLesson.objects.filter(user_course__in=crs)
    if len(lessons) == 0:
        context["lsn"] = 0
    else:
        student_additional = UserAdditional.objects.get(user=request.user)
        lessons.order_by('date')
        flag = False
        past_lessons = []
        future_lessons = []
        for l in lessons:
            end = l.date
            if student_additional.lesson_time:
                end += datetime.timedelta(minutes=60)
            else:
                end += datetime.timedelta(minutes=45)
            l.date_end = end
            l.save()
            if l.date <= datetime.datetime.now() <= end and not flag:
                context['cur_lsn'] = l
                if is_teacher:
                    context['video_chat'] = UserAdditional.objects.get(user=l.user_course.student).video_chat
                    chat = ChatRoom.objects.get(student=l.user_course.student)
                    context["chat"] = chat
                context['now_lsn'] = True
                flag = True
            elif end < datetime.datetime.now():
                if not l.is_completed:
                    student_additional.paid_lessons -= 1
                    student_additional.save()
                    l.is_completed = True
                    l.save()
                past_lessons.append(l)
            elif not l.is_completed:
                if len(future_lessons) < student_additional.paid_lessons:
                    if not flag:
                        flag = True
                        context['next_lsn'] = l.date
                    future_lessons.append(l)
        context['past_lsn'] = past_lessons
        context['future_lsn'] = future_lessons
        calendar = []
        day = []
        for i in range(len(lessons)):
            if i == 0:
                day.append(lessons[i])
            elif lessons[i].date.day == lessons[i-1].date.day:
                day.append(lessons[i])
            else:
                calendar.append(day)
                day = []
                day.append(lessons[i])
        calendar.append(day)
        context['calendar'] = calendar
        i = 0
        if student_additional.lesson_time:
            context['lsn_time'] = "60"
        else:
            context['lsn_time'] = "45"
        context['course'] = lessons[i].user_course.course_type
        context['teacher'] = lessons[i].user_course.teacher.user.first_name
        context["lsn"] = lessons
        try:
            context["ava"] = lessons[i].user_course.teacher.image.url
        except:
            context["ava"] = "Аватар"
        context["paid_lessons"] = student_additional.paid_lessons


    return render(request,'dashboard/dashboard-tape.html', context)


def ajax_pay_lessons(request):
    if request.method == 'POST':
        p = UserAdditional.objects.get(user=request.user)
        cost = int(request.POST.get('cost'))
        if cost == 4300:
            p.paid_lessons += 5
            p.lesson_time = False
        elif cost == 8000:
            p.paid_lessons += 10
            p.lesson_time = False
        elif cost == 14800:
            p.paid_lessons += 20
            p.lesson_time = False
        elif cost == 19800:
            p.paid_lessons += 30
            p.lesson_time = False
        elif cost == 4600:
            p.paid_lessons += 5
            p.lesson_time = True
        elif cost == 8800:
            p.paid_lessons += 10
            p.lesson_time = True
        elif cost == 16400:
            p.paid_lessons += 20
            p.lesson_time = True
        elif cost == 22200:
            p.paid_lessons += 30
            p.lesson_time = True
        else:
            p.paid_lessons += 0
            p.lesson_time = True
        p.save()
    return HttpResponse('pay')


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
        return HttpResponseRedirect('/dashboard/lk')

def ajax_load_lessons(request, number):
    lsn = []
    l = UserLesson.objects.get(id=number)
    lsn.append(l.json())
    return HttpResponse(json.dumps(lsn))

def ajax_load_lessons_videos(request, number):
    vid = []
    for i in UserLesson.objects.get(id=number).lesson.get_lesson_videos():
        vid.append(i.json())
    return HttpResponse(json.dumps(vid))

def ajax_load_video(request, number):
    vid = []
    vid.append(Lesson_video.objects.get(id=number).json())
    return HttpResponse(json.dumps(vid))

def ajax_load_lessons_audios(request, number):
    aud = []
    for i in UserLesson.objects.get(id=number).lesson.get_lesson_audios():
        aud.append(i.json())
    return HttpResponse(json.dumps(aud))

@login_required
def price(request):
    return render(request,'price.html')

def courses(request):
    return render(request,'courses.html')

def blog(request, number):
    context = {}
    blog = Blog.objects.get(id=number)
    context['blog'] = blog
    return render(request, 'blog-single.html', context)

def blogs(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    return render(request, 'blogs.html', context)


def video(request,number):
    context = {}
    context['video'] = VideoPractise.objects.get(id=number)
    return render(request,'video.html', context)

def video_constructor(request,number):
    context = {}
    video = VideoPractise.objects.get(id=number)
    context['video'] = video
    constructors = VideoPractiseConstructor.objects.filter(video_practise=video)
    context['constructors'] = constructors
    return render(request,'video_constructor.html', context)

def video_listening(request,number):
    context = {}
    video = VideoPractise.objects.get(id=number)
    context['video'] = video
    listenings = VideoPractiseListening.objects.filter(video_practise=video)
    context['listenings'] = listenings
    return render(request,'video_listening.html', context)

def view_404(request, exception):
    return render(request, "errors/404.html")


def view_500(request):
    return render(request, "errors/500.html")


