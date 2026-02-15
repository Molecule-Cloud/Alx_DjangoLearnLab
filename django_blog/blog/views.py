from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'blog/base.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

def home(request):
    return render(request, 'blog/base.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.name}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user # Get the curret user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)

        user.save()

        messages.success(request, 'Profile updated')
        return redirect('profile')
    return render(request, 'blog/profle.html', {'user': request.user})