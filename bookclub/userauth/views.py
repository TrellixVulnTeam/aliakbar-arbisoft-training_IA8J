from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from userauth.forms import UserCreateForm, UserProfileForm, UserLoginForm


def index(request):
    error_message = ''
    if request.user.is_authenticated:
        return redirect('books:index')
    else:
        user_form = UserLoginForm(data=request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = user.username
                return redirect('books:index')
            else:
                error_message = "username/password MISMATCHED!"
        else:
            user_form = UserLoginForm()
    return render(request, 'userauth/index.html', {'user_form': user_form, 'error_message': error_message})


def signup(request):
    user_form = UserCreateForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        password = user.password
        user.set_password(password)
        user.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        login(request, user)
        return redirect('books:index')
    else:
        user_form = UserCreateForm()
        profile_form = UserProfileForm()
    return render(request, 'userauth/signup.html', {'user_form': user_form, 'profile_form': profile_form})


def logout_user(request):
    logout(request)
    return redirect('userauth:index')
