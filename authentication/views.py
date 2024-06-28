from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegisterForm

# def login(request):
#     context = {'page_title': 'Login'}
#     return render(request, 'authentication/login.html', context=context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin-dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    context = {'page_title': 'Login'}
    return render(request, 'authentication/login.html', context=context)


def register(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        # form = UserCreationForm()
        form = UserRegisterForm()
    context = {'page_title': 'Register', 'form': form}
    return render(request, 'authentication/register.html', context=context)