from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


def index(request):
    """
    Homepage
    """
    return render(request, 'malepy/index.html')


def sign_in(request):
    """
    Display Sign In form
    """
    return render(request, 'malepy/sign_in.html')


def login(request):
    """
    User login
    """
    if request.method == 'POST':
        # extract data
        username = request.POST.get('username')
        password = request.POST.get('password')
        # check for user
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                print("Vidi sta je i uloguj ga")
            else:
                context = {"message": "User account is not activated"}
                return render(request, 'malepy/sign_in.html', context=context)
        else:
            context = {"message": "Wrong Username or Password"}
            return render(request, 'malepy/sign_in.html', context=context)


def logout(request):
    """
    User logout
    """
    auth_logout(request)
    return HttpResponseRedirect(reverse('malepy:index'))
