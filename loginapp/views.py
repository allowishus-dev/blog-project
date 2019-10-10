from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import UserProfile
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.signing import Signer
import uuid

def login(request):
    if User.is_authenticated:
        dj_logout(request)
    if request.method == 'POST':
        user = authenticate(request, 
            username=request.POST['user'], 
            password=request.POST['password'])
        if user:
            dj_login(request, user)
            return HttpResponseRedirect(reverse('articles:list'))
        else:
            context = {'error':'Authentication failed. You may need to activate your user'}
            return render(request, 'loginapp/login.html', context)

    return render(request, 'loginapp/login.html')

@login_required   
def logout(request):
    dj_logout(request)
    return HttpResponseRedirect(reverse('loginapp:login'))

def signup(request):
    if User.is_authenticated:
        dj_logout(request)

    context = {}
    if request.method == 'POST':       

        context['error'] = 'Must enter password'
        
        missing = []
        username = request.POST['user']
        if username == "":
            missing.append('username')
        email = request.POST['email']
        if email == "":
            missing.append('email')
        first_name = request.POST['firstname']
        if first_name == "":
            missing.append('first name')            
        last_name = request.POST['lastname']
        if last_name == "":
            missing.append('last name')
        password = request.POST['password']
        if password == "":
            missing.append('password')
        confirm_password = request.POST['confirm_password']
        if confirm_password == "":
            missing.append('confirm password')

        if len(missing) > 0:
            context['error'] = "Must enter " + missing[0]
            for i in range(1, len(missing)-1):
                context['error'] += ", " + missing[i]
            context['error'] += " & " + missing[len(missing)-1]

            return render(request, 'loginapp/signup.html', context)

        context = {}

        if password == confirm_password:
            if not User.objects.filter(username=username):
                user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    first_name=first_name, 
                    last_name=last_name,
                    password=password,
                    is_active=False)
                signer = Signer()
                key = signer.sign(email + ":" + username + ":" + str(uuid.uuid4())).split(':')[3]
                userProfile = UserProfile()
                userProfile.user = user
                userProfile.key = key
                
                if 'profile-image-file' in request.FILES:                    
                    uploaded_image = request.FILES['profile-image-file']
                else:
                    uploaded_image = static('loginapp/profile_pic.png')

                userProfile.profile_image = uploaded_image
                userProfile.save()

                # send email with uuid for activation
                # send_mail(
                #     'Activation of your user for ToDo',
                #     'Click this link to activate your user <a href="localhost:8000/accounts/activate?username={{username}}&activation_key={{activation_key}}',
                #     'allowishus.nexus@gmail.com',
                #     ['{{email}}'],
                #     fail_silently=False,
                # )

                context['success'] = 'User created. You were sent a email to help you activate your user'

                # return HttpResponseRedirect(reverse('loginapp:login'))       
                return render(request, 'loginapp/login.html', context)
            else:
                context['error'] = 'User already exist'
        else:
            context['error'] = 'Password and confirmation did not match'
    
    return render(request, 'loginapp/signup.html', context)

def activate(request):
    # localhost:8000/accounts/activate?username=jens&activation_key=BVzzrhj1xJW7XFrfTpRLjBvWUDI
    context = {}
    if request.method == 'GET':
        username = request.GET['username']

        if User.objects.filter(username=username):
            user = User.objects.get(username=username)
            if user.is_active == False:

                userProfile = user.userprofile
                if userProfile.key == request.GET['activation_key']:
                    user.is_active = True
                    user.save()
    
                    userProfile.key = ""
                    userProfile.save()

                    context['success'] = 'User is activated. You can log in now'

                else:
                    context['error'] = 'User activation failed' # activation key didn't match
            else:
                context['error'] = 'User has already been activated'
        else:
            context['error'] = 'User activation failed' # no such user

    return render(request, 'loginapp/login.html', context)

def forgot_password(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['user']
        
        if username != "":          
            if User.objects.filter(username=username):
                user = User.objects.get(username=username)
                if user.is_active:
                    # store signed key in UserKey
                    # key = str(uuid.uuid4())
                    signer = Signer(salt='blabla')
                    key = signer.sign(user.email + ":" + user.username + ":" + str(uuid.uuid4())).split(':')[3]
                    userProfile = user.userprofile
                    userProfile.key = key
                    userProfile.save()

                    # send email with uuid for reset
                    # send_mail(
                    #     'Activation of your user for ToDo',
                    #     'Click this link to reset your password <a href="localhost:8000/accounts/password_reset?username={{username}}&reset_key={{activation_key}}',
                    #     'allowishus.nexus@gmail.com',
                    #     ['{{email}}'],
                    #     fail_silently=False,
                    # )

                    context['success'] = 'You were sent a email to help you reset your password'

                else:
                    context['error'] = 'You need to activate your user'
            else:
                context['error'] = 'Password reset failed'
        else:
            context['error'] = 'Must enter username'
            
    return render(request, 'loginapp/forgot_password.html', context)

def password_reset(request):
    # localhost:8000/accounts/password_reset?username=jens&reset_key=0a68dfcf-2c5e-487e-8df3-f052d4c326fc
    context = {}
    if request.method == 'GET':
        username = request.GET['username']
        key = key=request.GET['reset_key']

        if User.objects.filter(username=username):
            user = User.objects.get(username=username)
            userProfile = user.userprofile
            if userProfile.key == key:
                userProfile.key = ""
                userProfile.save()
                dj_login(request, user)
        else:
            context['error'] = 'User activation failed' # activation key didn't match

    return render(request, 'loginapp/password_reset.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        if new_password == "" or confirm_password == "":
            context = {'error':'Password and confirmation cannot be empty'}
            return render(request, 'loginapp/change_password.html', context)
        if new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            
            dj_login(request, user)
            return HttpResponseRedirect(reverse('articles:list'))
        else:
            context = {'error':'Password and confirmation did not match'}
            return render(request, 'loginapp/change_password.html', context)

    return render(request, 'loginapp/change_password.html')