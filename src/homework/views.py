from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DetailView

from .email import send
from .models import Subject, Person


def home(request):
    return render(request, 'home.html')


@method_decorator(login_required, name='dispatch')
class SubjectSelect(ListView):
    """ Creates page for viewing info about subjects. """

    model = Subject
    template_name = "subject_list.html"


@method_decorator(login_required, name='dispatch')
class SubjectUpdate(UpdateView):
    """ Creates page for updating info about subject. """

    model = Subject
    fields = ["name", "description", "hours_in_week"]
    template_name = "sub_update.html"
    success_url = reverse_lazy("subjects_list")


@method_decorator(login_required, name='dispatch')
class TeacherSelect(ListView):
    """ Creates page for viewing info about teachers. """

    model = Person
    template_name = "teacher_list.html"


@method_decorator(login_required, name='dispatch')
class TeacherUpdate(UpdateView):
    """ Creates page for updating info about teacher. """

    model = Person
    fields = ["first_name", "last_name", "age", "person_type",
              "update_time", "is_active"]
    template_name = "teacher_update.html"
    success_url = reverse_lazy("teachers_list")


@method_decorator(login_required, name='dispatch')
class StudentSelect(ListView):
    """ Creates page for viewing list of students. """

    model = Person
    template_name = "student_list.html"


@method_decorator(login_required, name='dispatch')
class StudentDetail(DetailView):
    """ Creates page for viewing details about student. """

    model = Person
    template_name = 'student_detail.html'


def email_send(request):
    send(
        "Reset password",
        "admin@ban-adept.ru",
        "reset_password",
    )
    return render(request, 'email_send.html')


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponse(f'Hello, {user.username}')
        else:
            return HttpResponse("Incorrect username or password.")


def logging_out(request):
    logout(request)
    return redirect(reverse("login"))
