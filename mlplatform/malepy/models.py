from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """
    Model for Users, inheriting default Django User
    """
    user_role = models.IntegerField(null=False, blank=False, default=0)  # 0 = teacher, 1 = student
    members = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.username


class Course(models.Model):
    """
    Model for Course
    """
    name = models.CharField(max_length=50, null=False, blank=False)
    shortcut = models.CharField(max_length=10, null=False, blank=False)
    year = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    users = models.ManyToManyField(
        User,
        through='Enrollment',
    )

    def __str__(self):
        return self.name + " " + str(self.year)


class Enrollment(models.Model):
    """
    Model for User's enrollment in Courses
    """
    user = models.ForeignKey(User, null=False, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=False)
    enrolled = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " enrolled in " + self.course.shortcut


class Assignment(models.Model):
    """
    Model for Course Assignments
    """
    name = models.CharField(max_length=100, null=True, blank=True)
    name_en = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=2000, null=True, blank=True)
    description_en = models.CharField(max_length=2000, null=False, blank=False)
    training = models.CharField(max_length=200, null=True, blank=True)
    fake_testing = models.CharField(max_length=200, null=True, blank=True)
    testing = models.CharField(max_length=200, null=True, blank=True)
    starting = models.DateTimeField(null=True, blank=True)
    ending = models.DateTimeField(null=True, blank=True)
    folder = models.CharField(max_length=200, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.course.shortcut + "  -  " + self.name_en


class Submission(models.Model):
    """
    Model for Assignment's Submission
    """
    created = models.DateTimeField(auto_now=True, null=False, blank=False)
    file_name = models.CharField(max_length=200, null=False, blank=False)
    valid = models.BooleanField(null=False, blank=False, default=False)
    result = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    approved = models.BooleanField(null=False, blank=False, default=True)
    user = models.ForeignKey(User, null=False, blank=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.user.username + " for " + str(self.assignment) + " at " + str(self.created)
