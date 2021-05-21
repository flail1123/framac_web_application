"""framac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import homeView, login, logout, newFile, prover, vcs, compile, delete, select, newDirectory, upload

urlpatterns = [
    path('', homeView, name='emptyHome'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('select', select, name='select'),
    path('delete', delete, name='delete'),
    path('prover', prover, name='prover'),
    path('vcs', vcs, name='vcs'),
    path('compile', compile, name='compile'),
    path('newFile', newFile, name='newFile'),
    path('upload', upload, name='upload'),
    path('newDirectory', newDirectory, name='newDirectory'),
    path('admin/', admin.site.urls),
]
