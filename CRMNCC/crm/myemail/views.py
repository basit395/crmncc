from django.shortcuts import render
from crm.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail

# Create your views here.
#DataFlair #Send Email
def subscribe(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        subject = 'Welcome to NCC CRM'
        message = 'Hope you are enjoying your CRM account'
        recepient = str(sub['Email'].value())
        send_mail(subject,
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'myemail/success.html', {'recepient': recepient})
    return render(request, 'myemail/index.html', {'form':sub})