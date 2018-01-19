from django.conf.urls import url
from . import views

app_name = 'malepy'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sign/$', views.sign_in, name='sign'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
