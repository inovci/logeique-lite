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

# ---------------------------------------------------------------Auths views---------------------------------------------------------

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

def aut_login(request):
    return render(
            request,
            'register/aut_login.html'
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
                #user = User.objects.create_user(username=username, email=email, password=password)
                #user.save()

                if status == 'landlord':
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    landlord = Landlord.objects.create(
                        user=user,
                        contact=username
                    )
                    landlord.save()
                elif status == 'client':
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    client  = Client.objects.create(
                        user=user,
                        contact=username
                    )
                    client.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                if user_login:
                    auth.login(request, user_login)
                    return redirect('my_auths:aut_login')

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
    user = request.user
    
    try:
        user.landlord
        status = user.landlord.statuLogeique
        return render(
            request,
            'space/space.html',
            locals()
        )
    except:
        user.client
        status = user.client.statuLogeique
        return redirect('spaces:home')

# --------------------------------------------------------Landlord views-----------------------------------------------------------------

@login_required(login_url='my_auths:login')
def landlordClients(request):
    return render(
        request,
        'space/landlord/clients.html'
    )

@login_required(login_url='my_auths:login')
def landlordMaisons(request):
    maisons = Maison.objects.all()
    if request.method == 'POST':
        status = request.POST['status']
        landlord = Landlord.objects.get(user=request.user)

        if status == 'location':
            maison = Maison.objects.create(
                ville=request.POST['ville'],
                quartier=request.POST['quartier'],
                loyer=int(request.POST['loyer']),
                cotion=int(request.POST['cotion']),
                type_maison=request.POST['type_maison'],
                nombre_piece=int(request.POST['nombre_piece']),
                en_location=True,
                photos=request.FILES['photo'],
                landlord=landlord
            )
            maison.save()
            return redirect("my_auths:landlordMaisons")
        elif status == 'vente':
            maison = Maison.objects.create(
                ville=request.POST['ville'],
                quartier=request.POST['quartier'],
                loyer=int(request.POST['loyer']),
                cotion=int(request.POST['cotion']),
                type_maison=request.POST['type_maison'],
                nombre_piece=int(request.POST['nombre_piece']),
                en_vente=True,
                photos=request.FILES['photo'],
                landlord=landlord
            )
            maison.save()
            return redirect("my_auths:landlordMaisons")
        elif status == 'loc_ven':
            maison = Maison.objects.create(
                ville=request.POST['ville'],
                quartier=request.POST['quartier'],
                loyer=int(request.POST['loyer']),
                cotion=int(request.POST['cotion']),
                type_maison=request.POST['type_maison'],
                nombre_piece=int(request.POST['nombre_piece']),
                en_location=True,
                en_vente=True,
                photos=request.FILES['photo'],
                landlord=landlord
            )
            maison.save()
            return redirect("my_auths:landlordMaisons")
    return render(
        request,
        'space/landlord/maisons.html',
        locals()
    )

@login_required(login_url='my_auths:login')
def deleteMaison(request, id):
    landlord = Landlord.objects.get(user=request.user)
    try:
        maison = Maison.objects.get(id=id, landlord=landlord)
        maison.delete()
        del_house = True
        return redirect("my_auths:landlordMaisons")
    except:
        del_house = False
        return redirect("my_auths:landlordMaisons")
