from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from homework.router import router
from homework.views import (StudentDetail, StudentSelect, SubjectSelect,
                       SubjectUpdate, TeacherSelect, TeacherUpdate, activate,
                       email_send, home, logging_out, register, sign_in)


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('home/', home),
    path('email_send', email_send),

    path('api/', include(router.urls)),


    path('subjects', SubjectSelect.as_view(), name="subjects_list"),
    path('sub_update/<int:pk>', SubjectUpdate.as_view(), name='subjects_update'),

    path('teachers', TeacherSelect.as_view(), name="teachers_list"),
    path('teacher_update/<int:pk>', TeacherUpdate.as_view(), name='teachers_update'),

    path('students', StudentSelect.as_view(), name="student_list"),
    path('student_detail/<int:pk>', StudentDetail.as_view(), name="student_detail"),

    path('login', sign_in, name='login'),
    path('logout', logging_out, name='logout'),

    path('signup', register, name='signup'),
    path('verify_account/<str:uid>/<str:token>', activate, name='verify_account'),
]
