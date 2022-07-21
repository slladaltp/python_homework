import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from django.test import Client, TestCase
from mock import patch

from homework.models import Course, Person


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Person, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    courses = course_factory(_quantity=10)
    first_course = Course.objects.first()
    response = client.get(f'/group/{courses[0].id}/')
    assert response.status_code == 200
    assert response.data['id'] == first_course.id
    assert response.data['name'] == first_course.name


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    course_factory(_quantity=20)
    all_courses = Course.objects.all()
    response = client.get('/group/')
    assert response.status_code == 200
    assert len(response.data) == len(all_courses)


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/group/', {"id": courses[0].id})
    assert response.status_code == 200
    for item in response.data:
        assert item['id'] == courses[0].id


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/group/', {"name": courses[0].name})
    assert response.status_code == 200
    for item in response.data:
        assert item['name'] == courses[0].name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/group/', {'name': 'First course', 'students': []})
    assert response.status_code == 201
    assert Course.objects.count() == count+1


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.patch(f'/group/{courses[0].id}/', {'name': 'Updated name'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_course(client,course_factory):
    courses = course_factory(_quantity=5)
    count = Course.objects.count()
    response = client.delete(f'/group/{courses[0].id}/')
    assert response.status_code == 204
    assert Course.objects.count() == count-1


class SimpleTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    @patch('api.views.requests')
    def test_mocked_test_case_should_succeed(self, mock_request):
        """
        This is a simple testcase using mock feature.
        1 - Decorate the method with path (app_path.views.module).
        2 - Reference the mock in test method as param (mock_test).
        3 - Define a value of the return of method (sub method or property) to mock.
        4 - Call the mocked method and compare.
        """
        mock_request.get.content.return_value = '{origin: "62.16.29.131"}'
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{origin: "62.16.29.131"}')