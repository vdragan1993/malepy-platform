from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Enrollment, Assignment, Submission


class UserAdministration(UserAdmin):
    fieldsets = [
        ('Role', {'fields': ['user_role']}),
        (None, {'fields': ['username', 'password', 'email', 'first_name', 'last_name', 'date_joined', 'is_active',
                           'last_login']}),
        ('Student teams', {'fields': ['members']}),
    ]
    list_display = ('id', 'user_role', 'username', 'first_name', 'last_name', 'members')
    search_fields = ['username', 'first_name', 'last_name', 'members']


admin.site.register(User, UserAdministration)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year')
    search_fields = ['name', 'year']


admin.site.register(Course, CourseAdmin)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'enrolled')
    search_fields = ['user__username', 'course__name']


admin.site.register(Enrollment, EnrollmentAdmin)


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'name_en', 'starting', 'ending')
    search_fields = ['course__name', 'name_en', 'description_en']


admin.site.register(Assignment, AssignmentAdmin)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'assignment', 'created')
    search_fields = ['user__username', 'assignment__name_en']


admin.site.register(Submission, SubmissionAdmin)
