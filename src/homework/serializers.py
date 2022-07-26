from homework.models import Person, Subject, Group
from rest_framework import serializers


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'age', 'person_type', 'create_time',
                  'update_time', 'is_active', 'social_url', 'group'
                  ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['number', 'students_amount', 'name', 'course', 'create_time']


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'hours_in_week', 'teacher', 'create_time']
