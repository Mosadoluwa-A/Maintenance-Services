from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Client, Team
from .forms import ClientForm, TeamForm


def main(request):
    if request.method == "GET":
        return render(request, 'topazz/index.html')
    else:
        email = request.POST['email']
        check_mail = Client.objects.filter(email=email)
        if check_mail:
            messages.error(request, 'You have already contacted us')
            return redirect(main)
        else:
            form = ClientForm(request.POST)
            name = request.POST['name']
            gender = request.POST['gender']
            email = request.POST['email']
            phone_no = request.POST['phone_no']
            services = request.POST['services']
            newclient = form.save(commit=False)
            newclient.name = name
            newclient.gender = gender
            newclient.email = email
            newclient.phone_no = phone_no
            newclient.services = services
            newclient.save()
            messages.success(request, 'Thank you for contacting us')
            return redirect(main)


def about(request):
    team = Team.objects.all()
    return render(request, 'topazz/about.html', {'team': team})


@login_required(login_url='/login')
def home(request):
    clients = Client.objects.all()
    return render(request, 'topazz/home.html', {'clients': clients})


@login_required(login_url='/login')
def add_team(request):
    if request.method == "GET":
        return render(request, 'topazz/team-form.html')
    else:
        try:
            files = request.FILES
            image = files.get('image')
            form = TeamForm(request.POST)
            new_member = form.save(commit=False)
            new_member.image = image
            new_member.save()
        except ValueError:
            print(request.POST['name'])
            print(request.POST['role'])
            print(request.POST['description'])
            messages.error(request, 'The data is not correct')
            return render(request, 'topazz/team-form.html')


def login_user(request):
    if request.method == "GET":
        return render(request, 'topazz/login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, "Sorry username and passwords did not match")
            return render(request, 'users/index.html')
        else:
            login(request, user)
            messages.success(request, "Login Success")
            return redirect(home)


def logout_user(request):
    if request.method == "POST":
        logout(request)
    return redirect(login_user)