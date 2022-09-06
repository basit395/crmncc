from django import template
from django.contrib.auth.models import User


register = template.Library()


@register.simple_tag

def check_email(a):

    my_user = User.objects.get(username__iexact=a)

    if my_user.email:
        if my_user.email.endswith('ncc-ksa.net'):
            return ''
        else:
            return 'Your registered email is ' + my_user.email + '.Please provide your company email ends with ncc-ksa.net. '
    else:
        return 'Please provide the company email ensd with ncc-ksa.net'
