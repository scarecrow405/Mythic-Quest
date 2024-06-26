from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from profiles.forms import SignupForm, UserLoginForm, UserProfileEditForm
from profiles.models import UserProfile


def signup_user(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user.set_password(password)  # Set the password
            user.save()

            user = authenticate(username=username, password=password)
            login(request, user)
            UserProfile.objects.create(user=user, username=username, email=email)

            return redirect("create_character")
    else:
        form = SignupForm()
    
    context = {
        'form': form,
    }
    return render(request, 'profiles/signup.html', context)


def signin_user(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("create_character")
            else:
                context = {"error": "Invalid username or password, please try again!"}
                return render(request, "profiles/signin.html", context)
        else:
            error_type_usr_or_pass = "Invalid username or password, please try again!"

            messages.success(request, error_type_usr_or_pass)
            return render(request, "profiles/signin.html", {})
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'profiles/signin.html', context)


@login_required()
def signout_user(request):
    logout(request)
    return redirect("signin")


@login_required()
def user_profile_edit(request):
    profile = request.user.userprofile
    user = request.user

    if request.method == "POST":
        form = UserProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']

            user.save()
            form.save()
    else:
        form = UserProfileEditForm(instance=profile)

    username = profile.username
    email = profile.email
    about = profile.about
    profile_image = profile.profile_image

    context = {
        "form": form,
        "username": username,
        "email": email,
        "about": about,
        "profile_image": profile_image
    }

    return render(request, "profiles/profile_edit.html", context)


@login_required()
def user_profile_delete(request):
    profile = request.user.userprofile
    user = request.user

    if request.method == "POST":
        return redirect("confirm_profile_delete")

    form = UserProfileEditForm(instance=profile)

    username = profile.username
    email = profile.email
    about = profile.about
    profile_image = profile.profile_image

    context = {
        "form": form,
        "username": username,
        "email": email,
        "about": about,
        "profile_image": profile_image
    }

    return render(request, "profiles/profile_delete.html", context)


@login_required()
def confirm_profile_delete(request):
    profile = request.user.userprofile
    user = request.user

    if request.method == "POST":
        profile.delete()
        user.is_active = False
        user.save()
        return redirect("signup")
    return render(request, "profiles/confirm_profile_delete.html")
