from django.shortcuts import render
from .forms import SignupForm,resetForm
from django.contrib.auth import authenticate,login
from .models import Profile
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.contrib.auth.models import User
from django.http import HttpResponse
import random


def signup(request):
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            username = authenticate(username=username,password=password)
            login(request,user)
            return redirect('accounts/profile')
    else:
        form = SignupForm()

    context = {'form':form}
    return render(request, 'registration/signup.html',context)

def profile(request):
    profile = Profile.objects.get(user=request.user)
    context = {'profile':profile}
    return render(request, 'accounts/profile.html',context)


def profile_edit(request):
    pass


def reset(request):

    if request.method=='POST':
        form = resetForm(request.POST)
        if form.is_valid():

            myemail = form.cleaned_data['myemail']
            print(myemail)

            list1 = [1,2,3,4,5,6,7,8,9]
            list2 = ['A','B','C','D','E','F','G','H','J','K']
            list3 = ['q','w','r','g','h','j','y','t','r','e']
            list4 = ['!','@','#','%','&']
            print(list4)
            pas1  = str(list1[random.randrange(len(list1))])
            pas2 = random.choice(list2)
            pas3  = random.choice(list3)
            pas4 = random.choice(list4)
            pas5  = str(random.choice(list1))
            pas6 = random.choice(list2)
            pas7  = random.choice(list3)
            pas8 = random.choice(list4)
            myuser = User.objects.filter(email=myemail).first()

            if myuser is not None :
                print(myuser)
                mynewpassword = pas1 + pas2 + pas3 + pas4 + pas5 + pas6 + pas7 + pas8
                myuser.set_password(mynewpassword)
                myuser.save()
                subject = 'Password Reset'
                body = 'Your new password is ' + mynewpassword
                print('My Paaword',mynewpassword)
                with get_connection(
                host='mail.minaexc.com.sa',
                port=587,
                username='a.abdulbasit@minaexc.com.sa',
                password='abufaisal@mina',
                use_tls=True
                ) as connection:

                    EmailMessage(subject, body, 'a.abdulbasit@minaexc.com.sa', [myemail],
                                 connection=connection).send()

                msg = 'New Password is sent, Please check your email'
                context = {'msg':msg}
                return render(request, 'registration/reset.html',context)
            else:
                msg = 'Your Email is not registered'
                context = {'msg':msg}
                return render(request, 'registration/reset.html',context)


    else:

        form = resetForm()

        context = {'form':form}
        return render(request, 'registration/reset_form.html',context)





