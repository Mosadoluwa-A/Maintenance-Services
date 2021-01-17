from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Client, Team
from .forms import ClientForm, TeamForm


# This function is for the index page and it also handles the Contact form
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
            # It was raising a validation error until the correct order in the Forms.py was put
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


# This function basically handles the about page
def about(request):
    team = Team.objects.all()
    return render(request, 'topazz/about.html', {'team': team})


# The login_required function is to protect the routes until authentication is complete
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
            # form = TeamForm(request.POST, request.FILES)
            files = request.FILES
            image = files.get("image")
            name = request.POST['name']
            description = request.POST['description']
            role = request.POST['role']
            Team.objects.create(name=name, description=description, role=role, image=image)
            # new_member = form.save(commit=False)
            # new_member.image = image
            # new_member.save()
            messages.success(request, 'You have successfully added a member')
            return redirect(home)
        except ValueError:
            print(request.POST['name'])
            print(request.POST['role'])
            print(request.POST['description'])
            print(request.FILES.get("image"))
            messages.error(request, 'The data is not correct')
            return render(request, 'topazz/team-form.html')

        # form = TeamForm(request.POST)
        # files = request.FILES
        # image = files.get("image")
        # new_member = form.save(commit=False)
        # new_member.image = image
        # new_member.save()
        # messages.success(request, 'You have successfully added a member')
        # return redirect(home)


def login_user(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect(home)
    elif request.method == "GET":
        return render(request, 'topazz/login.html')

    # This Block of code didn't work I guess the order was not correct
    # if request.method == "GET":
    #     return render(request, 'topazz/login.html')
    # elif request.user.is_authenticated:
    #     messages.success(request, "You are already logged in")
    #     return redirect(home)
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, "Sorry username and passwords did not match")
            return render(request, 'topazz/login.html')
        else:
            login(request, user)
            messages.success(request, "Login Success")
            return redirect(home)


def logout_user(request):
    if request.method == "POST":
        logout(request)
    return redirect(login_user)