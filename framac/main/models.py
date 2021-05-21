from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Selected(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_file = models.IntegerField(default=0)
    selected_directory = models.IntegerField(default=0)


class Directory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True)
    creation_date = models.DateField(default=date.today)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    availability_flag = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    parent_directory = models.ForeignKey('Directory', on_delete=models.CASCADE, blank=True, null=True)


class File(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True)
    creation_date = models.DateField(default=date.today)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    availability_flag = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=10000, default="")
    prover = models.CharField(max_length=100, default="")
    vc = models.CharField(max_length=100, default="")


class StatusData(models.Model):
    status_data = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    availability_flag = models.BooleanField(default=True)


class FileSection(models.Model):
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=150, blank=True)
    creation_date = models.DateField(default=date.today)
    section_category = models.CharField(max_length=20, default="")
    section_status = models.CharField(max_length=20, default="")
    status_data = models.ForeignKey(StatusData, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    parent_file_section = models.ForeignKey('FileSection', on_delete=models.CASCADE, blank=True, null=True)
    availability_flag = models.BooleanField(default=True)
    code = models.CharField(max_length=10000, default="")
