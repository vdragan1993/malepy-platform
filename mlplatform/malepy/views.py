from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User, Enrollment, Course, Assignment, Submission, Report
from .forms import CourseForm, AssignmentForm, SubmissionForm
import datetime
from django.contrib.auth.decorators import user_passes_test
import shutil
from django.conf import settings
from django.utils import timezone
import os
import subprocess
from .utils import create_moss_report, extract_results, PlagiarismResult


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
    context = {"enrollments": enrollments}
    return render(request, 'malepy/dashboard.html', context=context)


"""
Test
"""


def is_teacher(user):
    return user.user_role == 0


def is_student(user):
    return user.user_role == 1


"""
Course views
"""


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def create_course_form(request):
    """
    Redirect to create new Course form
    """
    form = CourseForm()
    context = {"action": "Create", "model": "Course", "form": form}
    return render(request, 'malepy/actions.html', context=context)


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
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
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def update_course_form(request, course_id):
    """
    Redirect to update Course form
    """
    this_course = get_object_or_404(Course, pk=course_id)
    form = CourseForm(instance=this_course)
    context = {"action": "Update", "model": "Course", "form": form, "id": course_id}
    return render(request, 'malepy/actions.html', context=context)


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
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
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def delete_course(request, course_id):
    """
    Delete existing Course
    """
    this_course = get_object_or_404(Course, pk=course_id)
    this_course.delete()
    return redirect('malepy:dashboard')


"""
Assignment views
"""


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def create_assignment_form(request, course_id):
    """
    Redirect to create new Assignment form
    """
    this_course = get_object_or_404(Course, pk=course_id)
    form = AssignmentForm(initial={'course': this_course, 'starting': datetime.datetime.now(),
                                   'ending': datetime.datetime.now()})
    context = {"action": "Create", "model": "Assignment", "form": form}
    return render(request, 'malepy/actions.html', context=context)


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def create_assignment(request):
    """
    Creating new Assignment
    """
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            new_assignment = form.save()
            return HttpResponseRedirect(reverse('malepy:assignment', args=(new_assignment.id, )))
        else:
            context = {"action": "Create", "model": "Assignment", "form": form}
            return render(request, 'malepy/actions.html', context=context)


@login_required(login_url='/')
def assignment(request, assignment_id):
    """
    Display Assignment page
    """
    this_assignment = get_object_or_404(Assignment, pk=assignment_id)
    my_submissions = Submission.objects.filter(user=request.user, assignment__id=assignment_id).order_by('-created')
    if this_assignment.sorting == 'Asc':
        assignment_submissions = Submission.objects.filter(assignment__id=assignment_id).order_by('result')
    else:
        assignment_submissions = Submission.objects.filter(assignment__id=assignment_id).order_by('-result')
    leaderboard = []
    leaderboard_users = []
    for submission in assignment_submissions:
        if submission.user.username not in leaderboard_users and submission.valid:
            leaderboard.append(submission)
            leaderboard_users.append(submission.user.username)
    form = SubmissionForm()
    context = {"assignment": this_assignment, "form": form,
               "display_submit": this_assignment.starting < timezone.now() < this_assignment.ending,
               "my_submissions": my_submissions, 'leaderboard': leaderboard}
    return render(request, 'malepy/assignment.html', context=context)


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def update_assignment_form(request, assignment_id):
    """
    Redirect to update Assignment form
    """
    this_assignment = get_object_or_404(Assignment, pk=assignment_id)
    form = AssignmentForm(instance=this_assignment)
    context = {"action": "Update", "model": "Assignment", "form": form, "id": assignment_id}
    return render(request, 'malepy/actions.html', context=context)


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def update_assignment(request, assignment_id):
    """
    Update existing Assignment
    """
    if request.method == 'POST':
        this_assignment = get_object_or_404(Assignment, pk=assignment_id)
        form = AssignmentForm(request.POST, request.FILES, instance=this_assignment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('malepy:assignment', args=(assignment_id, )))
        else:
            context = {"action": "Update", "model": "Assignment", "form": form, "id": assignment_id}
            return render(request, 'malepy/actions.html', context=context)


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def delete_assignment(request, assignment_id):
    """
    Delete existing Assignment
    """
    this_assignment = get_object_or_404(Assignment, pk=assignment_id)
    redirect_id = this_assignment.course.id
    delete_folder = settings.MEDIA_URL + this_assignment.folder
    this_assignment.delete()
    try:
        shutil.rmtree(delete_folder)
    except:
        pass
    return HttpResponseRedirect(reverse('malepy:course', args=(redirect_id, )))


@login_required(login_url='/')
@user_passes_test(is_student, redirect_field_name='/dashboard')
def make_submission(request, assignment_id):
    """
    Make submission to an Assignment
    """
    if request.method == 'POST':
        this_assignment = get_object_or_404(Assignment, pk=assignment_id)
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            new_submission = Submission.objects.create(
                submitted_file=request.FILES['submitted_file'],
                user=request.user,
                assignment=this_assignment
            )
            new_submission.save()
            # execute script
            command_file = settings.MEDIA_URL + str(new_submission.submitted_file)
            command_train = settings.MEDIA_URL + str(new_submission.assignment.training)
            command_test = settings.MEDIA_URL + str(new_submission.assignment.testing)
            command = "python " + command_file + " " + command_train + " " + command_test
            # call process
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output_lines = process.stdout.readlines()
            if len(output_lines) > 0:
                try:
                    new_submission.result = float(output_lines[-1])
                    new_submission.valid = True
                    new_submission.save()
                except:
                    new_submission.valid = False
                    new_submission.approved = False
                    new_submission.save()
            else:
                new_submission.valid = False
                new_submission.approved = False
                new_submission.save()

            return HttpResponseRedirect(reverse('malepy:assignment', args=(assignment_id, )))
        else:
            return HttpResponseRedirect(reverse('malepy:assignment', args=(assignment_id, )))


@login_required(login_url='/')
def submission(request, submission_id):
    """
    Submission Display page
    """
    this_submission = get_object_or_404(Submission, pk=submission_id)
    display_download = True
    if request.user.user_role:
        if request.user.id != this_submission.user.id and timezone.now() < this_submission.assignment.ending:
            display_download = False
    context = {"submission": this_submission, "display_download": display_download,
               "display_delete": timezone.now() < this_submission.assignment.ending}
    return render(request, 'malepy/submission.html', context=context)


@login_required(login_url='/')
@user_passes_test(is_student, redirect_field_name='/dashboard')
def delete_submission(request, submission_id):
    """
    Delete Submission
    """
    this_submission = get_object_or_404(Submission, pk=submission_id)
    if request.user.id != this_submission.user.id:
        return redirect('malepy:dashobard')

    redirect_id = this_submission.assignment.id
    delete_file = settings.MEDIA_URL + str(this_submission.submitted_file)
    this_submission.delete()
    try:
        os.remove(delete_file)
    except:
        pass
    return HttpResponseRedirect(reverse('malepy:assignment', args=(redirect_id, )))


@login_required(login_url='/')
def history(request, user_id):
    """
    User Submissions
    """
    this_user = get_object_or_404(User, pk=user_id)
    submissions = Submission.objects.filter(user=this_user).order_by('-created')
    context = {"display_user": this_user, "submissions": submissions}
    return render(request, 'malepy/history.html', context=context)


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def toggle_submission_approvement(request, submission_id):
    """
    Toggle Submission's approvement
    """
    this_submission = get_object_or_404(Submission, pk=submission_id)
    if this_submission.approved:
        this_submission.approved = False
    else:
        this_submission.approved = True
    this_submission.save()
    return HttpResponseRedirect(reverse('malepy:submission', args=(submission_id, )))


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def generate_moss_report(request, assignment_id):
    """
    Generate MOSS report for Assignment
    """
    this_assignment = get_object_or_404(Assignment, pk=assignment_id)
    if this_assignment.sorting == 'ASC':
        assignment_submissions = Submission.objects.filter(assignment__id=assignment_id).order_by('result')
    else:
        assignment_submissions = Submission.objects.filter(assignment__id=assignment_id).order_by('-result')
    leaderboard = []
    leaderboard_users = []
    for submission in assignment_submissions:
        if submission.user.username not in leaderboard_users and submission.valid:
            leaderboard.append(submission)
            leaderboard_users.append(submission.user.username)
    # files to check
    files = []
    for submission in leaderboard:
        files.append(settings.MEDIA_URL + str(submission.submitted_file))
    folder = settings.MEDIA_URL + this_assignment.folder + "/"
    detected, file_path = create_moss_report(files, folder)
    new_report = Report.objects.create(
        report_file=file_path,
        plagiarism=detected,
        assignment=this_assignment
    )
    new_report.save()
    return HttpResponseRedirect(reverse('malepy:report', args=(new_report.id, )))


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def report(request, report_id):
    """
    Display MOSS Report page
    """
    this_report = get_object_or_404(Report, pk=report_id)
    if this_report.plagiarism:
        plagiarisms = extract_results(str(this_report.report_file))
        this_plagiarisms = []
        for plagiarism in plagiarisms:
            position = -1 * (len(settings.MEDIA_URL.split("/")) - 1)
            file_1_parts = plagiarism.file_1.split("/")[position:]
            file_2_parts = plagiarism.file_2.split("/")[position:]
            submission1 = Submission.objects.get(submitted_file='/'.join(file_1_parts))
            submission2 = Submission.objects.get(submitted_file='/'.join(file_2_parts))
            this_plagiarisms.append(PlagiarismResult(submission1, plagiarism.percentage_1, submission2,
                                                 plagiarism.percentage_2, plagiarism.lines))
        context = {"report": this_report, "plagiarisms": this_plagiarisms}
    else:
        context = {"report": this_report}
    return render(request, 'malepy/report.html', context=context)


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def reports(request):
    """
    Display MOSS Report history
    """
    this_user = get_object_or_404(User, pk=request.user.id)
    enrollments = Enrollment.objects.filter(user=this_user).order_by('-enrolled')
    course_ids = []
    for enrollment in enrollments:
        course_ids.append(enrollment.course.id)
    this_reports = Report.objects.filter(assignment__course__id__in=course_ids).order_by('-created')
    context = {"reports": this_reports}
    return render(request, 'malepy/reports.html', context=context)


@login_required(login_url='/')
@user_passes_test(is_teacher, redirect_field_name='/dashboard')
def delete_report(request, report_id):
    """
    Delete MOSS Report
    """
    this_report = get_object_or_404(Report, pk=report_id)
    delete_file = str(this_report.report_file)
    this_report.delete()
    try:
        os.remove(delete_file)
    except:
        pass
    return redirect('malepy:reports')
