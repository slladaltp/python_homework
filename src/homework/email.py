from django.conf import settings

from django.template import loader
from django.core.mail import send_mail


def send(subject, to_email,  template_name, ):
    """
     Отправка письма на заданный адресс.
    """
    html_template = loader.get_template(f"{template_name}.html")
    html_message = html_template.render()

    txt_template = loader.get_template(f"{template_name}.txt")
    txt_message = txt_template.render()

    send_mail(
        subject=subject,
        message=txt_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        html_message=html_message,
    )
