from rest_framework import routers

from homework.views import PersonViewSet, GroupViewSet, SubjectViewSet

router = routers.DefaultRouter()
router.register(r'person', PersonViewSet)
router.register(r'group', GroupViewSet)
router.register(r'subject', SubjectViewSet)
