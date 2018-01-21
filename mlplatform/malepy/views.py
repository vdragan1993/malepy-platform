from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User, Enrollment, Course, Assignment
from .forms import CourseForm


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


"""
Course views
"""


@login_required(login_url='/')
def create_course_form(request):
    """
    Redirect to create new Course form
    """
    form = CourseForm()
    context = {"action": "Create", "model": "Course", "form": form}
    return render(request, 'malepy/actions.html', context=context)


@login_required(login_url='/')
def create_course(request):
    """
    Creating new Course
    """
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # save new course
            new_course = form.save()
            # enrol user to the new course
            new_enrolment = Enrollment.objects.create(user=request.user, course=new_course)
            new_enrolment.save()
            # redirect to dashboard
            return HttpResponseRedirect(reverse('malepy:course', args=(new_course.id, )))
        else:
            context = {"action": "Create", "model": "Course", "form": form}
            return render(request, 'malepy/actions.html', context=context)


@login_required(login_url='/')
def course(request, course_id):
    """
    Display Course page
    """
    this_course = get_object_or_404(Course, pk=course_id)
    assignments = Assignment.objects.filter(course=this_course).order_by('-ending')
    enrollments = Enrollment.objects.filter(course=this_course).order_by('enrolled')
    students = []
    for enrollment in enrollments:
        if enrollment.user.user_role:
            students.append(enrollment.user)
    context = {"course": this_course, "assignments": assignments, "students": students}
    return render(request, 'malepy/course.html', context=context)


@login_required(login_url='/')
def update_course_form(request, course_id):
    """
    Redirect to update Course form
    """
    this_course = get_object_or_404(Course, pk=course_id)
    form = CourseForm(instance=this_course)
    context = {"action": "Update", "model": "Course", "form": form, "id": course_id}
    return render(request, 'malepy/actions.html', context=context)


@login_required(login_url='/')
def update_course(request, course_id):
    """
    Update existing Course
    """
    if request.method == 'POST':
        this_course = get_object_or_404(Course, pk=course_id)
        form = CourseForm(request.POST, instance=this_course)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('malepy:course', args=(course_id, )))
        else:
            context = {"action": "Update", "model": "Course", "form": form, "id": course_id}
            return render(request, 'malepy/actions.html', context=context)


@login_required(login_url='/')
def delete_course(request, course_id):
    """
    Delete existing Course
    """
    this_course = get_object_or_404(Course, pk=course_id)
    this_course.delete()
    return redirect('malepy:dashboard')
