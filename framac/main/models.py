from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True)


class Directory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True)
    creation_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    availability_flag = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    parent_directory = models.ForeignKey('Directory', on_delete=models.CASCADE, blank=True)


class File(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True)
    creation_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    availability_flag = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, blank=True)


class StatusData(models.Model):
    status_data = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

class FileSection(models.Model):
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=150, blank=True)
    creation_date = models.DateField()
    SECTION_CATEGORY_CHOICES = [
        ('1', 'procedure'),
        ('2', 'property'),
        ('3', 'lemma'),
        ('4', 'assertion'),
        ('5', 'invariant'),
        ('6', 'precondition'),
        ('7', 'postcondition'),
    ]
    section_category = models.CharField(max_length=1, choices=SECTION_CATEGORY_CHOICES)
    SECTION_STATUS_CHOICES = [
        ('1', 'proved'),
        ('2', 'invalid'),
        ('3', 'counterexample'),
        ('4', 'unchecked'),
    ]
    section_status = models.CharField(max_length=1, choices=SECTION_STATUS_CHOICES)
    status_data = models.ForeignKey(StatusData, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    parent_file_section = models.ForeignKey('FileSection', on_delete=models.CASCADE)