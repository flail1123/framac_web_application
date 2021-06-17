import datetime
from django.contrib.auth.models import User
from .models import *
from datetime import *
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from .views import *
import json
from .utility_functions import getFile

class QuestionModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="hmmm", password="sadghbnviluas23421")
        self.selected = Selected.objects.create(owner=self.user)
        self.directory = Directory.objects.create(owner=self.user, name="new_directory")
        self.file = File.objects.create(owner=self.user, name="new_file", directory=self.directory)
        self.statusData = StatusData.objects.create(user=self.user, status_data="Valid")
        self.fileSection = FileSection.objects.create(name="new_file_section", file=self.file, status_data=self.statusData)
        self.request_factory = RequestFactory()

    def test_user(self):
        assert self.user.username == "hmmm"
        assert self.user.password == "sadghbnviluas23421"
    
    def test_selected(self):
        assert self.selected.owner == self.user
        assert self.selected.selected_directory == 0
        assert self.selected.selected_file == 0

    def test_directory(self):
        assert self.directory.owner == self.user
        assert self.directory.name == "new_directory"
        assert self.directory.creation_date == date.today()
        assert self.directory.availability_flag == True
        assert self.directory.parent_directory == None
    
    def test_file(self):
        assert self.file.name == "new_file"
        assert self.file.owner == self.user 
        assert self.file.directory == self.directory
        assert self.file.creation_date == date.today()
        assert self.file.availability_flag == True
        assert self.file.prover == ""
        assert self.file.vc == ""
        assert self.file.code == ""

    def test_status_data(self):
        assert self.statusData.user == self.user
        assert self.statusData.status_data == "Valid"
        assert self.statusData.availability_flag == True

    def test_file_section(self):
        assert self.fileSection.name == "new_file_section"
        assert self.fileSection.file == self.file
        assert self.fileSection.status_data == self.statusData 
        assert self.fileSection.availability_flag == True
        assert self.fileSection.creation_date == date.today()

    def test_new_file_view(self):
        request = self.request_factory.post(reverse('newFile'), {"selectedDirectory": self.selected.selected_directory, "name": "newFile2"})
        request.user = self.user
        response = newFile(request)
        dictionary = json.loads(response.content.decode('utf-8'))
        assert dictionary["id"] == "0_1"
        assert len(File.objects.filter(owner=self.user, directory=self.directory)) == 2
        file = File.objects.filter(owner=self.user, directory=self.directory)[1]
        assert file.name == "newFile2"
        assert file.directory == self.directory
    
    def test_new_directory_view(self):
        request = self.request_factory.post(reverse('newDirectory'), {"name": "newDirectory2"})
        request.user = self.user
        response = newDirectory(request)
        dictionary = json.loads(response.content.decode('utf-8'))
        assert dictionary["id"] == "1"
        assert len(Directory.objects.filter(owner=self.user)) == 2
        directory = Directory.objects.filter(owner=self.user)[1]
        assert directory.name == "newDirectory2"

    def test_delete_view(self):
        request = self.request_factory.post(reverse('delete'), {"name": "newDirectory2"})
        request.user = self.user
        response = delete(request)
        dictionary = json.loads(response.content.decode('utf-8'))
        assert dictionary["whatWasDeleted"] == "file"

        response = delete(request)
        dictionary = json.loads(response.content.decode('utf-8'))
        assert dictionary["whatWasDeleted"] == "directory"

    def test_prover(self):
        request = self.request_factory.post(reverse('prover'), {"prover": "newProver"})
        request.user = self.user
        response = prover(request)
        dictionary = json.loads(response.content.decode('utf-8'))
        assert dictionary == {}
        file = getFile(self.selected.selected_directory, self.selected.selected_file, self.user)
        assert file.prover == "newProver" 

    def test_vcs(self):
        request = self.request_factory.post(reverse('vcs'), {"vc": "newVC"})
        request.user = self.user
        response = vcs(request)
        dictionary = json.loads(response.content.decode('utf-8'))
        assert dictionary == {}
        file = getFile(self.selected.selected_directory, self.selected.selected_file, self.user)
        assert file.vc == "newVC" 

    def test_compile_view(self):
        file = getFile(self.selected.selected_directory, self.selected.selected_file, self.user)
        with open('test_framac_file.c', "r") as f:
            request = self.request_factory.post(reverse('compile'), {"code": f.read()})
            request.user = self.user
            response = compile(request)
            dictionary = json.loads(response.content.decode('utf-8'))
    
    def test_select_view(self):
        request = self.request_factory.post(reverse('select'), {"selected": "0_0"})
        request.user = self.user
        response = select(request)
        dictionary = json.loads(response.content.decode('utf-8'))
        file = getFile(self.selected.selected_directory, self.selected.selected_file, self.user)
        assert dictionary["code"] == file.code
        assert dictionary["id"] == ""


        request = self.request_factory.post(reverse('select'), {"selected": "0"})
        request.user = self.user
        response = select(request)
        dictionary = json.loads(response.content.decode('utf-8'))
        file = getFile(self.selected.selected_directory, self.selected.selected_file, self.user)
        assert dictionary["code"] == file.code


    def test_login_view(self):
        request = self.request_factory.post(reverse('login'), {})
        request.user = self.user
        response = login(request)
        assert response.status_code == 302

        
        request = self.request_factory.post(reverse('login'), {})
        request.user = User.objects.create(username="not_logged_in", password="user")
        response = login(request)
        assert response.status_code == 302


    def test_home_view(self):
        request = self.request_factory.post("/", {})
        request.user = self.user
        response = homeView(request)
        assert response.status_code == 200
        assert response.content.decode('utf-8')[:16] == "\n<!DOCTYPE html>"

    def test_upload(self):
        with open('plik.c') as fp:
            request = self.request_factory.post(reverse('upload'), {"file": fp})
            request.user = self.user
            response = upload(request)
            dictionary = json.loads(response.content.decode('utf-8'))
            assert dictionary["name"] == "plik.c"
            assert dictionary["id"] == "0_1"
            assert dictionary["dir"] == "0"



# https://docs.djangoproject.com/en/3.1/topics/testing/overview/
# django.test.TestCase vs unittest.TestCase.

# https://docs.djangoproject.com/pl/3.1/intro/tutorial06/
# static files

# https://docs.djangoproject.com/pl/3.1/intro/tutorial07/
# python manage.py createsuperuser

# import os
# output = os.system("frama-c -wp-prover alt-ergo -wp -wp-print example.c")

# standardowe podejście
# https://frama-c.com/2020/11/04/docker-images.html
# POST localhost:9091/runprogram
# + https://flask.palletsprojects.com/en/1.1.x/