from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from homework.models import Person, Subject, Group

USER_MODEL = get_user_model()


class PersonViewTestCase(APITestCase):
    def setUp(self):
        user = USER_MODEL()
        user.username = 'test_user'
        user.email = 'test_user_email'
        user.set_password('password')
        user.save()

        self.client.login(
            username='test_user',
            password='password',
        )

        self.person = Person.objects.create(
            first_name='test_first_name', last_name='test_last_name',
            age=0, person_type='test_person_type',
            create_time='2006-10-25', update_time='2006-10-25',
            is_active=True, social_url=''
            )

    def test_person_get_endpoint(self):
        response = self.client.get(
            reverse('person-list')
        )

        self.assertDictEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "first_name": "test_first_name",
                        "last_name": "test_last_name",
                        "age": 0,
                        "person_type": "test_person_type",
                        "create_time": "2006-10-25",
                        "update_time": "2006-10-25",
                        "is_active": True,
                        "social_url": '',
                        "group": None
                    }
                ]
            }

        )

    def test_person_create_endpoint(self):
        self.client.post(
            reverse('person-list'),
            data={
                "first_name": "first_name",
                "last_name": "last_name",
                "age": "0",
                "person_type": "person_type",
                "create_time": "2006-10-25",
                "update_time": "2006-10-25",
                "is_active": "True",
                "social_url": ''
            }
        )

        self.assertEqual(Person.objects.count(), 2)

    def test_person_delete_endpoint(self):
        self.client.delete(
            reverse('person-detail', kwargs={'pk': self.person.pk})
        )
        self.assertEqual(Person.objects.count(), 0)

    def test_person_update_endpoint(self):
        self.client.put(
            reverse('person-detail', kwargs={'pk': self.person.pk}),
            data={
                "first_name": "Test user name",
                "last_name": "Test last name",
                "age": "1",
                "person_type": "person_type",
                "create_time": "2006-10-24",
                "update_time": "2006-10-24",
                "is_active": "False",
                "social_url": ''
            }
        )
        person = Person.objects.first()

        self.assertEqual(
            person.first_name,
            "Test user name"
        )
        self.assertEqual(
            person.last_name,
            "Test last name"
        )
        self.assertEqual(
            person.age,
            1
        )


class SubjectViewTestCase(APITestCase):
    def setUp(self):
        user = USER_MODEL()
        user.username = 'test_user'
        user.email = 'test_user_email'
        user.set_password('password')
        user.save()

        self.client.login(
            username='test_user',
            password='password',
        )

        self.subject = Subject.objects.create(
            name='test_name', description='test_description',
            hours_in_week=0, create_time='2022-06-17T14:16:23.331744Z'
        )

    def test_subject_get_endpoint(self):
        response = self.client.get(
            reverse('subject-list')
        )

        self.assertDictEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "name": "test_name",
                        "description": "test_description",
                        "hours_in_week": 0,
                        "teacher": None,
                        "create_time": "2022-06-17T14:16:23.331744Z"
                    }
                ]
            }
        )

    def test_subject_create_endpoint(self):
        self.client.post(
            reverse('subject-list'),
            data={
                "name": 'test_name',
                "description": "test_description",
                "hours_in_week": "0",
                "create_time": "2022-06-17T14:16:23.331744Z",
            }
        )
        self.assertEqual(Subject.objects.count(), 2)

    def test_subject_delete_endpoint(self):
        self.client.delete(
            reverse('subject-detail', kwargs={'pk': self.subject.pk})
        )
        self.assertEqual(Subject.objects.count(), 0)

    def test_subject_update_endpoint(self):
        self.client.put(
            reverse('subject-detail', kwargs={'pk': self.subject.pk}),
            data={
                "name": 'test sub name',
                "description": "test subject description",
                "hours_in_week": "2",
                "create_time": "2022-07-17T14:16:23.331744Z",
            }
        )
        subject = Subject.objects.first()

        self.assertEqual(
            subject.name,
            "test sub name"
        )
        self.assertEqual(
            subject.description,
            "test subject description"
        )


class GroupViewTestCase(APITestCase):
    def setUp(self):
        user = USER_MODEL()
        user.username = 'test_user'
        user.email = 'test_user_email'
        user.set_password('password')
        user.save()

        self.client.login(
            username='test_user',
            password='password',
        )

        self.group = Group.objects.create(
            number=0, students_amount=0, name='test_name',
            create_time='2022-06-17T17:21:00Z'
        )

    def test_group_get_endpoint(self):
        response = self.client.get(
            reverse('group-list')
        )

        self.assertDictEqual(
            response.json(),

            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "number": 0,
                        "students_amount": 0,
                        "name": "test_name",
                        "course": None,
                        "create_time": "2022-06-17T17:21:00Z"
                    }
                ]
            }
        )

    def test_group_create_endpoint(self):
        self.client.post(
            reverse('group-list'),
            data={
                "number": "0",
                "students_amount": "0",
                "name": 'test_name',
                "create_time": "2022-06-17T17:21:00Z",
            }
        )
        self.assertEqual(Group.objects.count(), 2)

    def test_group_delete_endpoint(self):
        self.client.delete(
            reverse('group-detail', kwargs={'pk': self.group.pk})
        )
        self.assertEqual(Group.objects.count(), 0)

    def test_group_update_endpoint(self):
        self.client.put(
            reverse('group-detail', kwargs={'pk': self.group.pk}),
            data={
                "number": "1",
                "students_amount": "1",
                "name": 'test name',
                "create_time": "2022-07-17T17:21:00Z",
            }
        )
        group = Group.objects.last()

        self.assertEqual(
            group.number,
            1
        )
        self.assertEqual(
            group.students_amount,
            1
        )
        self.assertEqual(
            group.name,
            'test name'
        )
