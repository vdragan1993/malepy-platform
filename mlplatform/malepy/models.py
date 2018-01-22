from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.conf import settings


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
        return self.user.username + " enrolled in " + str(self.course)


def assignment_data_set_directory(instance, filename):
    """
    Assignment File storage helper
    """
    return instance.folder + '/' + filename


class Assignment(models.Model):
    """
    Model for Course Assignments
    """
    SORTING_CHOICES = (
        ('Asc', 'Asc'),
        ('Desc', 'Desc')
    )

    name = models.CharField(max_length=100, null=True, blank=True)
    name_en = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=2000, null=True, blank=True)
    description_en = models.CharField(max_length=2000, null=False, blank=False)
    folder = models.CharField(max_length=100, null=False, blank=False, default='undecided')
    training = models.FileField(null=True, blank=True, upload_to=assignment_data_set_directory)
    fake_testing = models.FileField(null=True, blank=True, upload_to=assignment_data_set_directory)
    testing = models.FileField(null=True, blank=True, upload_to=assignment_data_set_directory)
    starting = models.DateTimeField(null=True, blank=True)
    ending = models.DateTimeField(null=True, blank=True)
    measurement = models.CharField(max_length=50, null=False, blank=False, default='Accuracy')
    sorting = models.CharField(max_length=4, null=False, blank=False, default='Asc', choices=SORTING_CHOICES)
    threshold = models.FloatField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return str(self.course) + "  -  " + self.name_en

    def training_set_name(self):
        if self.training:
            return str(self.training.path).split('/')
        else:
            return ['None']

    def training_set_url(self):
        return '/' + settings.MEDIA_URL + str(self.training)

    def fake_testing_set_name(self):
        if self.fake_testing:
            return str(self.fake_testing.path).split('/')
        else:
            return ['None']

    def fake_testing_url(self):
        return '/' + settings.MEDIA_URL + str(self.fake_testing)

    def testing_set_name(self):
        if self.testing:
            return str(self.testing.path).split('/')
        else:
            return ['None']

    def testing_url(self):
        return '/' + settings.MEDIA_URL + str(self.testing)


def submitted_file_name(instance, filename):
    """
    Auto assigned name for submitted file
    """
    created_date = str(instance.created.day) + str(instance.created.month) + str(instance.created.year) + '_' + \
                   str(instance.created.hour) + str(instance.created.minute) + str(instance.created.second)
    return instance.assignment.folder + '/' + instance.user.username + '_' + created_date + '_' + filename


class Submission(models.Model):
    """
    Model for Assignment's Submission
    """
    created = models.DateTimeField(auto_now=True, null=False, blank=False)
    submitted_file = models.FileField(null=False, blank=False, upload_to=submitted_file_name, default='my_file')
    valid = models.BooleanField(null=False, blank=False, default=False)
    result = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    approved = models.BooleanField(null=False, blank=False, default=True)
    user = models.ForeignKey(User, null=False, blank=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.user.username + " for " + str(self.assignment) + " at " + str(self.created)
