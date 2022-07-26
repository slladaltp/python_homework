from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import DetailView, ListView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter

from .email import send
from .models import Person, Subject, Group
from .serializers import PersonSerializer, GroupSerializer, SubjectSerializer

USER_MODEL = get_user_model()


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
        "eliza.tripolskaya21@gmail.com",
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


def register(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = USER_MODEL.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False,
        )

        send(
            subject="Verify your account!",
            to_email=email,
            template_name="email_verification",
            context={
                "username": username,
                "verify_url": reverse("verify_account", kwargs={
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user)
                }),
                "request": request,
            }
        )
        return HttpResponse(f'Hello, {user.username}. Check your email for verification letter. ')


def activate(request, uid, token):
    try:
        user = USER_MODEL.objects.get(pk=urlsafe_base64_decode(uid))
    except (TypeError, ValueError, OverflowError, USER_MODEL.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)
        return redirect(reverse('student_list'))

    return HttpResponse("Invalid link.")


class PersonViewSet(viewsets.ModelViewSet):
    """
        Person ViewSet which allow list, create, retrieve, update and delete methods.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['first_name']
    ordering_fields = ['update_time']


class GroupViewSet(viewsets.ModelViewSet):
    """
        GroupViewSet which allow list, create, retrieve, update and delete methods.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name']
    ordering_fields = ['create_time']


class SubjectViewSet(viewsets.ModelViewSet):
    """
     SubjectViewSet which allow list, create, retrieve, update and delete methods.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name']
    ordering_fields = ['create_time']
