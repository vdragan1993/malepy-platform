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
]
