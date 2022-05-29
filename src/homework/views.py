from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView

from .email import send
from .models import Subject, Person


def home(request):
    return render(request, 'home.html')


class SubjectSelect(ListView):
    """ Creates page for viewing info about subjects. """

    model = Subject
    template_name = "subject_list.html"


class SubjectUpdate(UpdateView):
    """ Creates page for updating info about subject. """

    model = Subject
    fields = ["name", "description", "hours_in_week"]
    template_name = "sub_update.html"
    success_url = reverse_lazy("subjects_list")


class TeacherSelect(ListView):
    """ Creates page for viewing info about teachers. """

    model = Person
    template_name = "teacher_list.html"


class TeacherUpdate(UpdateView):
    """ Creates page for updating info about teacher. """

    model = Person
    fields = ["first_name", "last_name", "age", "person_type",
              "update_time", "is_active"]
    template_name = "teacher_update.html"
    success_url = reverse_lazy("teachers_list")


class StudentSelect(ListView):
    """ Creates page for viewing list of students. """

    model = Person
    template_name = "student_list.html"


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
