from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from .models import *
from .forms import UploadFileForm
from django.http import JsonResponse
from .utility_functions import *


def homeView(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    selectedFile, selectedDirectory = getSelected(request.user)
    directories = []
    count = 0
    for directory in Directory.objects.all():
        if directory.owner == request.user:
            if directory.availability_flag:
                directories.append((count, directory, [b for b in [(i, a) for i, a in enumerate(File.objects.filter(directory=directory.id))] if b[1].availability_flag]))
            count += 1

    uploadFileForm = UploadFileForm()
    focusOnElements = []
    result = ""
    prover = ""
    vc = 'type guard verification conditions: for example -wp-prop="-@invariant"'
    code = ""
    try:
        prover = directories[selectedDirectory][2][selectedFile][1].prover
        vc = directories[selectedDirectory][2][selectedFile][1].vc
        file = directories[selectedDirectory][2][selectedFile][1]
        code = file.code
    except:
        pass

    return render(request, "index.html", {"directories": directories, "selectedDirectory": selectedDirectory,
                                          "selectedFile": selectedFile, "code": code,
                                          "focusOnElements": focusOnElements, "lenDirectory": len(directories),
                                          "result": result, "vc": vc, "prover": prover, "uploadFileForm": uploadFileForm,
                                          "default": "default", "css": "../../static/style.css", "logged": 'yes'})

def newFile(request):
    if request.method == 'POST':
        directory = Directory.objects.filter(owner=request.user)[int(request.POST['selectedDirectory'])]
        newFile = File.objects.create(name=request.POST['name'], owner=request.user, directory=directory)
        number = str(len(File.objects.filter(directory=directory.id)) - 1)
        return JsonResponse({"id": request.POST['selectedDirectory'] + "_" + number})


def newDirectory(request):
    if request.method == 'POST':
        newDirectory = Directory.objects.create(name=request.POST['name'], owner=request.user)
        number = str(len(Directory.objects.filter(owner=request.user)) - 1)
        return JsonResponse({"id": number})


def delete(request):
    owner = request.user
    selectedFile, selectedDirectory = getSelected(request.user)
    if request.method == 'POST':
        directory = Directory.objects.filter(owner=owner)[selectedDirectory]
        files = File.objects.filter(directory=directory.id)
        if len(files) == 0:
            directory.availability_flag = False
            directory.save()
            return JsonResponse({"whatWasDeleted": "directory"})
        else:
            files[selectedFile].availability_flag = False
            files[selectedFile].save()
            return JsonResponse({"whatWasDeleted": "file"})


def prover(request):
    if request.method == 'POST':
        selectedFile, selectedDirectory = getSelected(request.user)
        file = getFile(selectedDirectory, selectedFile, request.user)
        file.prover = request.POST["prover"]
        file.save()
        return JsonResponse({})


def vcs(request):
    if request.method == 'POST':
        selectedFile, selectedDirectory = getSelected(request.user)
        file = getFile(selectedDirectory, selectedFile, request.user)
        file.vc = request.POST["vc"]
        file.save()
        return JsonResponse({})

def compile(request):
    if request.method == 'POST':
        selectedFile, selectedDirectory = getSelected(request.user)
        file = getFile(selectedDirectory, selectedFile, request.user)
        file.code = request.POST["code"]
        file.save()
        return JsonResponse({"result": doResult(file), "focusOnElements": doFocusOnElements(file)})

def select(request):
    if request.method == 'POST':
        if "_" in request.POST["selected"]:
            selectedDirectory, selectedFile = [int (i) for i in request.POST["selected"].split("_")]
            selected = Selected.objects.filter(owner=request.user)[0]
            selected.selected_file = selectedFile
            selected.selected_directory = selectedDirectory
            selected.save()
            file = getFile(selectedDirectory, selectedFile, request.user)
            return JsonResponse({"code": file.code, "id": ""})
        else:
            selectedDirectory = int(request.POST["selected"])
            selected = Selected.objects.filter(owner=request.user)[0]
            selected.selected_file = 0
            selected.selected_directory = selectedDirectory
            selected.save()
            try:
                code = getFile(selectedDirectory, 0, request.user).code
                id = "#" + request.POST["selected"] + "_0"
            except:
                code = ""
                id = ""
            return JsonResponse({"code": code, "id": id})

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            selectedFile, selectedDirectory = getSelected(request.user)
            directory = Directory.objects.filter(owner=request.user)[selectedDirectory]
            newFile = File.objects.create(name=request.FILES['file'].name[:-2], owner=request.user, directory=directory, code=request.FILES['file'].read().decode('utf-8'))
            number = str(len(File.objects.filter(directory=directory.id)) - 1)
            return JsonResponse({"name": request.FILES['file'].name, "id": str(selectedDirectory) + "_" + number, "dir": str(selectedDirectory)})


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'index.html', {'logged': 'INVALID CREDENTIALS'})
    else:
        return render(request, 'index.html', {'logged': 'no'})

def logout(request):
    auth.logout(request)
    return redirect('/login')