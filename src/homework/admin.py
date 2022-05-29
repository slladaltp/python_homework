from django.contrib import admin
from django.utils.html import format_html

from homework.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'age', ]
    fields = ['first_name', 'last_name', 'age',
              'update_time', 'is_active', 'social_url', ]

    def full_name(self, instance):
        """
            Making custom column. Displaying a link if person has
            a social_url.
        """
        if instance.social_url:
            return format_html("<a href='{}'>{} {}<a/>",
                               instance.social_url, instance.first_name, instance.last_name)
        else:
            return f'{instance.first_name} {instance.last_name}'
