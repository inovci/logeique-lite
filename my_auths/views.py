from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from .models import Profile, Post, LikePost, FollowersCount
from .models import *
from itertools import chain
import random

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('my_auths:space')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('my_auths:login')

    else:
        return render(
            request,
            'login/login.html'
        )

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        passwordv = request.POST['passwordv']
        status = request.POST['status']
        print(status)

        if password == passwordv:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email déjà utilisé !')
                return redirect('my_auths:register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Contact déjà utilisé !')
                return redirect('my_auths:register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                if user_login:
                    auth.login(request, user_login)
                    return redirect('my_auths:login')

                #create a Profile object for the new user
                """
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
                """
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('my_auths:register')
        
    else:
        return render(
            request,
            'register/register.html'
        )

@login_required(login_url='my_auths:login')
def logout(request):
    auth.logout(request)
    return redirect('spaces:home')

@login_required(login_url='my_auths:login')
def user_space(request):
    return render(
        request,
        'space/space.html'
    )
