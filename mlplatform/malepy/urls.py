from django.conf.urls import url
from . import views

app_name = 'malepy'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sign/$', views.sign_in, name='sign'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^create_course_from/$', views.create_course_form, name='create_course_form'),
    url(r'^create_course/$', views.create_course, name='create_course'),
    url(r'^course/(?P<course_id>[0-9]+)/$', views.course, name='course'),
    url(r'^update_course_form/(?P<course_id>[0-9]+)/$', views.update_course_form, name='update_course_form'),
    url(r'^update_course/(?P<course_id>[0-9]+)/$', views.update_course, name='update_course'),
    url(r'^delete_course/(?P<course_id>[0-9]+)/$', views.delete_course, name='delete_course'),
    url(r'^create_assignment_form/(?P<course_id>[0-9]+)/$', views.create_assignment_form, name='create_assignment_form'),
    url(r'^create_assignment/$', views.create_assignment, name='create_assignment'),
    url(r'^assignment/(?P<assignment_id>[0-9]+)/$', views.assignment, name='assignment'),
    url(r'^update_assignment_form/(?P<assignment_id>[0-9]+)/$', views.update_assignment_form, name='update_assignment_form'),
    url(r'^update_assignment/(?P<assignment_id>[0-9]+)/$', views.update_assignment, name='update_assignment'),
    url(r'^delete_assignment/(?P<assignment_id>[0-9]+)/$', views.delete_assignment, name='delete_assignment'),
    url(r'^make_submission/(?P<assignment_id>[0-9]+)/$', views.make_submission, name='make_submission'),
    url(r'^submission/(?P<submission_id>[0-9]+)/$', views.submission, name='submission'),
    url(r'^delete_submission/(?P<submission_id>[0-9]+)/$', views.delete_submission, name='delete_submission'),
    url(r'^history/(?P<user_id>[0-9]+)/$', views.history, name='history'),
    url(r'^toggle_submission_approvement/(?P<submission_id>[0-9]+)/$', views.toggle_submission_approvement, name='toggle_submission_approvement'),
    url(r'^generate_moss_report/(?P<assignment_id>[0-9]+)/$', views.generate_moss_report, name='generate_moss_report'),
    url(r'^report/(?P<report_id>[0-9]+)/$', views.report, name='report'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^delete_report/(?P<report_id>[0-9]+)/$', views.delete_report, name='delete_report'),
]
