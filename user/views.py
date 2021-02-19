from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    return HttpResponse(status=405)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('homepage')

    return render(
        request,
        'user/login.html',
        context={
            'form': form
        }
    )


def register(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    user_create_form = CustomUserCreationForm()
    if request.method == 'POST':
        user_create_form = CustomUserCreationForm(
            request.POST)
        if user_create_form.is_valid():
            user_create_form.save()
            return redirect('homepage')

    return render(
        request,
        template_name='user/register.html',
        context={
            'form': user_create_form
        }
    )
