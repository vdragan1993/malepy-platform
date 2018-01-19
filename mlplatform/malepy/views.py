from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User, Enrollment


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
                auth_login(request, user)
                return redirect('malepy:dashboard')
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


@login_required(login_url='/')
def dashboard(request):
    """
    User dashboard
    """
    this_user = get_object_or_404(User, pk=request.user.id)
    enrollments = Enrollment.objects.filter(user=this_user).order_by('-enrolled')
    if this_user.members:
        context = {"enrollments": enrollments, "members": this_user.members.split(',')}
    else:
        context = {"enrollments": enrollments}

    return render(request, 'malepy/dashboard.html', context=context)
